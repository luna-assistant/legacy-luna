import datetime
import time
from luna.server import app, db, bcrypt, models, hashids
from luna.server.helpers import QueryBuilder
from hashids import Hashids

class BaseRepository(object):

    use_soft_delete = False

    @property
    def model(self):
        return models.Model

    def create(self, values):
        if isinstance(values, self.model):
            values = dict(values)

        values['created_at'] = datetime.datetime.now()

        query = QueryBuilder(self.model.table, self.model.columns[1:])\
            .insert()\
            .returning([self.model.primary_key])\
            .sql()

        cursor = db.execute_sql(
            query,
            [values.get(c, None) for c in self.model.columns[1:]]
        )

        return self.find(cursor.fetchone()[0])

    def update(self, pk, values):
        if isinstance(values, self.model):
            values = dict(values)

        values['updated_at'] = datetime.datetime.now()

        query = QueryBuilder(self.model.table, self.model.columns[1:])\
            .update()\
            .where(self.model.primary_key)\
            .sql()

        db.execute_sql(
            query,
            (*[values.get(c, None) for c in self.model.columns[1:]], pk)
        )

        return self.find(pk, True)

    def delete(self, pk):
        query = QueryBuilder(self.model.table)\
            .delete()\
            .where(self.model.primary_key)\
            .sql()

        db.execute_sql(query, (pk,))

    def soft_delete(self, pk):
        obj = self.find(pk, True)
        obj.deleted_at = datetime.datetime.now()
        self.update(pk, obj)

    def find(self, pk, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where(self.model.primary_key)\
            .limit(1)

        if self.use_soft_delete and not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (pk,))
        return self.as_object(cursor)

    def all(self, with_trash=False, order_by=[('id',)]):
        query = QueryBuilder(self.model.table, self.model.columns)
        
        for o in order_by:
            query = query.order_by(*o)

        if self.use_soft_delete and not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()
        cursor = db.execute_sql(query)
        return self.as_iterator(cursor)

    def as_iterator(self, cursor, model=None):
        if model is None:
            model = self.model
        return (model(**dict(zip(model.columns, r))) for r in cursor)

    def as_object(self, cursor, model=None):
        if cursor.rowcount == 0:
            return None
        if model is None:
            model = self.model
        return model(**dict(zip(model.columns, cursor.fetchone())))


class UserRepository(BaseRepository):

    @property
    def model(self):
        return models.User
    
    def create(self, values):
        if isinstance(values, models.User):
            values = dict(values)

        values['password'] = bcrypt.generate_password_hash(
            values['password'], app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')

        return super(UserRepository, self).create(values)

    def update(self, pk, values, update_password=False):
        if isinstance(values, models.User):
            values = dict(values)

        if update_password:
            values['password'] = bcrypt.generate_password_hash(
                values['password'], app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode('utf-8')

        return super(UserRepository, self).update(pk, values)

    def findByUsername(self, username):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('username')\
            .limit(1)\
            .sql()
        cursor = db.execute_sql(query, (username,))
        return self.as_object(cursor)

    def allByRole(self, role_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .join('user_has_roles')\
            .on('user_id', '=', 'id')\
            .on('role_id')\
            .sql()

        cursor = db.execute_sql(query, (role_id,))
        return self.as_iterator(cursor)


class PersonRepository(BaseRepository):

    use_soft_delete = True

    def __init__(self):
        self.emailRepo = EmailRepository()
        self.contactRepo = ContactRepository()

    @property
    def model(self):
        return models.Person

    def create(self, values):
        person = super(PersonRepository, self).create(values)

        if 'emails' in values:
            self.emailRepo.deleteByPerson(person.id)
            for value in values['emails']:
                self.emailRepo.create(dict(person_id=person.id, email=value))

        if 'contacts' in values:
            self.contactRepo.deleteByPerson(person.id)
            for value in values['contacts']:
                self.contactRepo.create(dict(
                    person_id=person.id,
                    ddd=value['ddd'],
                    num=value['num']
                ))

        return person

    def update(self, pk, values):
        person = super(PersonRepository, self).update(pk, values)

        if 'emails' in values:
            self.emailRepo.deleteByPerson(person.id)
            for value in values['emails']:
                self.emailRepo.create(dict(person_id=person.id, email=value))

        if 'contacts' in values:
            self.contactRepo.deleteByPerson(person.id)
            for value in values['contacts']:
                self.contactRepo.create(dict(
                    person_id=person.id,
                    ddd=value['ddd'],
                    num=value['num']
                ))

        return person

    def findByUser(self, user_id, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('user_id')\
            .limit(1)

        if not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (user_id,))
        return self.as_object(cursor)

    def findByCpf(self, cpf, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('cpf')\
            .limit(1)

        if not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (cpf,))
        return self.as_object(cursor)


class EmailRepository(BaseRepository):

    @property
    def model(self):
        return models.Email

    def deleteByPerson(self, person_id):
        query = QueryBuilder(self.model.table)\
            .delete()\
            .where('person_id')\
            .sql()
        db.execute_sql(query, (person_id,))

    def allByPerson(self, person_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('person_id')\
            .sql()
        cursor = db.execute_sql(query, (person_id,))
        return self.as_iterator(cursor)


class ContactRepository(BaseRepository):

    @property
    def model(self):
        return models.Contact

    def deleteByPerson(self, person_id):
        query = QueryBuilder(self.model.table)\
            .delete()\
            .where('person_id')\
            .sql()
        db.execute_sql(query, (person_id,))

    def allByPerson(self, person_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('person_id')\
            .sql()
        cursor = db.execute_sql(query, (person_id,))
        return self.as_iterator(cursor)


class PeopleAssociatedRepository(BaseRepository):

    @property
    def model(self):
        return models.PersonAssociated

    def deleteByPerson(self, person_id):
        query = QueryBuilder(self.model.table).delete().where(
            'person_id').sql()
        db.execute_sql(query, (person_id,))

    def deleteAssociation(self, person_id, associated_id):
        query = QueryBuilder(self.model.table).delete().where(
            'person_id').where('associated_id').sql()
        db.execute_sql(query, (person_id, associated_id))

    def allByPerson(self, person_id):
        query = QueryBuilder(models.Person.table, models.Person.columns)\
            .join(self.model.table)\
            .on('person_id')\
            .on('associated_id', '=', 'id')\
            .sql()

        cursor = db.execute_sql(query, (person_id,))
        return self.as_iterator(cursor, models.Person)


class CityRepository(BaseRepository):

    @property
    def model(self):
        return models.City

    def allByFederativeUnit(self, federative_unit_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('federative_unit_id')\
            .sql()
        cursor = db.execute_sql(query, (federative_unit_id,))
        return self.as_iterator(cursor)


class FederativeUnitRepository(BaseRepository):

    @property
    def model(self):
        return models.FederativeUnit


class UserHasRoleRepository():

    def create(self, values):
        query = QueryBuilder('user_has_roles', ['user_id', 'role_id'])\
            .insert()\
            .returning(['user_id', 'role_id'])\
            .sql()
        cursor = db.execute_sql(query, (values['user_id'], values['role_id']))
        return models.UserHasRole(**dict(
            zip(models.UserHasRole.columns, cursor.fetchone())
        ))

    def delete(self, values):
        query = QueryBuilder('user_has_roles')\
            .delete()\
            .where('user_id')\
            .where('role_id')\
            .sql()
        db.execute_sql(query, (values['user_id'], values['role_id']))


class RoleRepository(BaseRepository):

    @property
    def model(self):
        return models.Role

    def allByUser(self, user_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .join('user_has_roles')\
            .on('role_id', '=', 'id')\
            .on('user_id')\
            .sql()

        cursor = db.execute_sql(query, (user_id,))
        return self.as_iterator(cursor)


class ModuleRepository(BaseRepository):

    @property
    def model(self):
        return models.Module

    def create(self, values):
        timestamp = int(time.time())
        values.identifier = str(timestamp)
        values.is_active = True
        module = super(ModuleRepository, self).create(values)
        module.identifier = hashids.encode(module.id, module.module_type_id, timestamp)
        return self.update(module.id, module)

    def findByIdentifier(self, identifier, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('identifier')\
            .limit(1)

        if not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (identifier,))
        return self.as_object(cursor)


class ModuleTypeRepository(BaseRepository):

    @property
    def model(self):
        return models.ModuleType


class InformationTypeRepository(BaseRepository):

    @property
    def model(self):
        return models.InformationType


class CommandTypeRepository(BaseRepository):

    @property
    def model(self):
        return models.CommandType


class InformationRepository(BaseRepository):

    @property
    def model(self):
        return models.Information

    def allByModuleType(self, module_type_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('module_type_id')\
            .sql()
        cursor = db.execute_sql(query, (module_type_id,))
        return self.as_iterator(cursor)

    def deleteByModuleType(self, module_type_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .delete()\
            .where('module_type_id')\
            .sql()
        db.execute_sql(query, (module_type_id,))


class CommandRepository(BaseRepository):

    @property
    def model(self):
        return models.Command

    def allByModuleType(self, module_type_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('module_type_id')\
            .sql()
        cursor = db.execute_sql(query, (module_type_id,))
        return self.as_iterator(cursor)

    def deleteByModuleType(self, module_type_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .delete()\
            .where('module_type_id')\
            .sql()
        db.execute_sql(query, (module_type_id,))
