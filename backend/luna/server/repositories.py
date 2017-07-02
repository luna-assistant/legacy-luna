import datetime
from luna.server import app, db, bcrypt, models


class BaseRepository(object):

    primary_key = 'id'
    use_soft_delete = False

    @property
    def model(self):
        return models.Model

    def create(self, values):
        if isinstance(values, self.model):
            values = dict(values)

        values['created_at'] = datetime.datetime.now()

        query = '''
        INSERT INTO {} ({})
        VALUES ({})
        RETURNING {}
        '''.format(self.table,
                   ', '.join(self.model.columns[1:]),
                   ', '.join(['%s' for c in self.model.columns[1:]]),
                   self.primary_key)

        cursor = db.execute_sql(
            query,
            [values.get(c, None) for c in self.model.columns[1:]]
        )

        return self.find(cursor.fetchone()[0])

    def update(self, pk, values):
        if isinstance(values, self.model):
            values = dict(values)

        values['updated_at'] = datetime.datetime.now()

        query = '''
        UPDATE {}
        SET {}
        WHERE {} = %s
        '''.format(self.table,
                   ', '.join(['{} = %s'.format(c)
                              for c in self.model.columns[1:]]),
                   self.primary_key)

        db.execute_sql(
            query,
            (*[values.get(c, None) for c in self.model.columns[1:]], pk)
        )

        return self.find(pk, True)

    def delete(self, pk):
        query = '''
        DELETE FROM {}
        WHERE {} = %s
        '''.format(self.table, self.primary_key)

        db.execute_sql(query, (pk,))

    def soft_delete(self, pk):
        obj = self.find(pk, True)
        obj.deleted_at = datetime.datetime.now()
        self.update(pk, obj)

    def find(self, pk, with_trash=False):
        query = '''
        SELECT {}
        FROM {}
        WHERE {} = %s {}
        LIMIT 1
        '''.format(', '.format(self.model.columns),
                   self.table,
                   self.primary_key,
                   'AND deleted_at IS NULL' if self.use_soft_delete and with_trash else '')

        cursor = db.execute_sql(query, (pk,))
        if cursor.rowcount == 0:
            return None
        return self.model(**dict(zip(self.model.columns, cursor.fetchone())))

    def all(self, with_trash=False):
        query = '''
        SELECT {}
        FROM {}
        '''.format(', '.join(self.model.columns), self.table)

        if self.use_soft_delete and with_trash:
            query += ' WHERE deleted_at IS NULL'

        cursor = db.execute_sql(query)
        return (self.model(**dict(zip(self.model.columns, r))) for r in cursor)


class UserRepository(BaseRepository):

    table = 'users'

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
        query = '''
        SELECT {}
        FROM users
        WHERE username = %s
        LIMIT 1
        '''.format(', '.join(self.model.columns))

        cursor = db.execute_sql(query, (username,))
        return models.User(**dict(zip(self.model.columns, cursor.fetchone()))) if cursor.rowcount > 0 else None


class PersonRepository(BaseRepository):

    table = 'people'
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

    def findByCpf(self, cpf, with_trash=False):
        query = '''
        SELECT {}
        FROM people
        WHERE cpf = %s {}
        LIMIT 1
        '''.format(', '.join(self.model.columns),
                   'AND deleted_at IS NULL' if not with_trash else '')

        cursor = db.execute_sql(query, (cpf,))
        if cursor.rowcount == 0:
            return None
        return models.Person(**dict(zip(self.model.columns, cursor.fetchone())))


class EmailRepository(BaseRepository):
    table = 'emails'

    @property
    def model(self):
        return models.Email

    def deleteByPerson(self, person_id):
        query = '''
        DELETE FROM emails
        WHERE person_id = %s
        '''
        db.execute_sql(query, (person_id,))

    def allByPerson(self, person_id):
        query = '''
        SELECT email
        FROM emails
        WHERE person_id = %s
        '''
        cursor = db.execute_sql(query, (person_id,))
        return (r[0] for r in cursor)


class ContactRepository(BaseRepository):
    table = 'contacts'

    @property
    def model(self):
        return models.Contact

    def deleteByPerson(self, person_id):
        query = '''
        DELETE FROM contacts
        WHERE person_id = %s
        '''
        db.execute_sql(query, (person_id,))

    def allByPerson(self, person_id):
        query = '''
        SELECT ddd, num
        FROM contacts
        WHERE person_id = %s
        '''
        cursor = db.execute_sql(query, (person_id,))
        return (dict(ddd=r[0], num=r[1]) for r in cursor)


class CityRepository(BaseRepository):
    table = 'cities'

    @property
    def model(self):
        return models.City
