import datetime
from luna.server import app, db, bcrypt, models
from luna.server.helpers import QueryBuilder


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
        if cursor.rowcount == 0:
            return None
        return self.model(**dict(zip(self.model.columns, cursor.fetchone())))

    def all(self, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)

        if self.use_soft_delete and not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query)
        return (self.model(**dict(zip(self.model.columns, r))) for r in cursor)


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
        return models.User(**dict(zip(self.model.columns, cursor.fetchone()))) if cursor.rowcount > 0 else None


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

    def findByUserId(self, user_id, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('user_id')\
            .limit(1)

        if not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (user_id,))
        if cursor.rowcount == 0:
            return None
        return models.Person(**dict(zip(self.model.columns, cursor.fetchone())))

    def findByCpf(self, cpf, with_trash=False):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('cpf')\
            .limit(1)

        if not with_trash:
            query = query.where('deleted_at', 'IS', 'NULL')

        query = query.sql()

        cursor = db.execute_sql(query, (cpf,))
        if cursor.rowcount == 0:
            return None
        return models.Person(**dict(zip(
            self.model.columns, cursor.fetchone()
        )))

    def findByUserId(self, user_id, with_trash=False):
        query = '''
        SELECT {}
        FROM {}
        WHERE user_id = %s {}
        LIMIT 1
        '''.format(', '.join(self.model.columns),
                   self.model.table,
                   'AND deleted_at IS NULL' if not with_trash else '')

        cursor = db.execute_sql(query, (user_id,))
        if cursor.rowcount == 0:
            return None
        return models.Person(**dict(zip(self.model.columns, cursor.fetchone())))


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
        if cursor.rowcount == 0:
            return None
        return (models.Email(**dict(zip(self.model.columns, r))) for r in cursor)


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
        if cursor.rowcount == 0:
            return None
        return (models.Contact(**dict(zip(self.model.columns, r))) for r in cursor)


class PeopleAssociatedRepository(BaseRepository):
    @property
    def model(self):
        return models.PersonAssociated

    def deleteByPerson(self, person_id):
        query = QueryBuilder(self.model.table).delete().where('person_id').sql()
        db.execute_sql(query, (person_id,))

    def deleteAssociation(self, person_id, associated_id):
        query = QueryBuilder(self.model.table).delete().where('person_id').where('associated_id').sql()
        db.execute_sql(query, (person_id, associated_id))

    def allByPerson(self, person_id):
        query = '''
        SELECT p.*
        FROM people p
        INNER JOIN people_associated pa on pa.associated_id = p.id
        WHERE pa.person_id = %s
        '''
        cursor = db.execute_sql(query, (person_id,))
        return (models.Person(**dict(zip(models.Person.columns, r))) for r in cursor)


class CityRepository(BaseRepository):

    @property
    def model(self):
        return models.City

    def allByFederativeUnit(self, federative_unit_id):
        query = QueryBuilder(self.model.table, self.model.columns)\
            .where('federative_unit_id')\
            .sql()
        cursor = db.execute_sql(query, (federative_unit_id,))
        return (self.model(**dict(zip(self.model.columns, r))) for r in cursor)


class FederativeUnitRepository(BaseRepository):

    @property
    def model(self):
        return models.FederativeUnit
