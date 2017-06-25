import datetime
from luna.server import app, db, bcrypt, models
from psycopg2.extensions import AsIs


class UserRepository(object):

    __columns__ = [
        'id',
        'username',
        'password',
        'created_at',
        'updated_at',
        'deleted_at'
    ]

    def create(self, values):
        if isinstance(values, models.User):
            values = dict(values)

        values['password'] = bcrypt.generate_password_hash(
            values['password'], app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        values['created_at'] = datetime.datetime.now()

        query = 'INSERT INTO users (' + ', '.join(
            self.__columns__[1:]) + ') VALUES (%s, %s, %s, %s, %s) RETURNING id'
        tvalues = [values.get(c, None) for c in self.__columns__[1:]]

        cursor = db.execute_sql(
            query,
            tvalues
        )

        return self.find(cursor.fetchone()[0])

    def update(self, id, values, update_password=False):
        if isinstance(values, models.User):
            values = dict(values)

        values['updated_at'] = datetime.datetime.now()

        if update_password:
            values['password'] = bcrypt.generate_password_hash(
                values['password'], app.config.get('BCRYPT_LOG_ROUNDS')
            ).decode('utf-8')

        query = '''
        UPDATE users
        SET
            username = %s,
            password = %s,
            created_at = %s,
            updated_at = %s,
            deleted_at = %s
        WHERE
            id = %s
        '''

        db.execute_sql(
            query,
            (*[values.get(c, None) for c in self.__columns__[1:]], id,)
        )

        return self.find(id)

    def delete(self, id):
        db.execute_sql('DELETE FROM users WHERE id = %s', (id,))

    def find(self, id):
        cursor = db.execute_sql(
            'SELECT ' + ', '.join(self.__columns__) +
            ' FROM users WHERE id = %s LIMIT 1',
            (id,))
        return models.User(**dict(zip(self.__columns__, cursor.fetchone()))) if cursor.rowcount > 0 else None

    def findByUsername(self, username):
        cursor = db.execute_sql(
            'SELECT ' + ', '.join(self.__columns__) +
            ' FROM users WHERE username = %s LIMIT 1',
            (username,))
        return models.User(**dict(zip(self.__columns__, cursor.fetchone()))) if cursor.rowcount > 0 else None

    def all(self):
        cursor = db.execute_sql(
            'SELECT ' + ', '.join(self.__columns__) + ' FROM users')
        return (models.User(**dict(zip(self.__columns__, record))) for record in cursor)


class PersonRepository(object):

    columns = [
        'id',
        'name',
        'cpf',
        'facebook',
        'twitter',
        'birth',
        'address',
        'complement',
        'postal_code',
        'neighborhood',
        'city_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]

    def create(self, values):
        if isinstance(values, models.Person):
            values = dict(values)

        values['created_at'] = datetime.datetime.now()

        query = '''
        INSERT INTO people ({})
        VALUES ({})
        RETURNING id
        '''.format(', '.join(self.columns[1:]),
                   ', '.join(['%s' for c in self.columns[1:]]))

        cursor = db.execute_sql(
            query,
            [values.get(c, None) for c in self.columns[1:]]
        )
        
        person = self.find(cursor.fetchone()[0], True)
        
        if 'emails' in values:
            emailRepo = EmailRepository()
            emailRepo.deleteByPerson(person.id)
            for value in values['emails']:
                emailRepo.create(dict(person_id=person.id, email=value))
        
        if 'contacts' in values:
            contactRepo = ContactRepository()
            contactRepo.deleteByPerson(person.id)
            for value in values['contacts']:
                contactRepo.create(dict(
                    person_id=person.id,
                    ddd=value['ddd'],
                    num=value['num']
                ))

        return person

    def update(self, id, values):
        if isinstance(values, models.Person):
            values = dict(values)

        values['updated_at'] = datetime.datetime.now()

        query = '''
        UPDATE people
        SET {}
        WHERE id = %s
        '''.format(', '.join(['{} = %s'.format(c) for c in self.columns[1:]]))

        db.execute_sql(
            query,
            (*[values.get(c, None) for c in self.columns[1:]], id)
        )
        
        if 'emails' in values:
            emailRepo = EmailRepository()
            emailRepo.deleteByPerson(id)
            for value in values['emails']:
                emailRepo.create(dict(person_id=id, email=value))
        
        if 'contacts' in values:
            contactRepo = ContactRepository()
            contactRepo.deleteByPerson(id)
            for value in values['contacts']:
                contactRepo.create(dict(
                    person_id=id,
                    ddd=value['ddd'],
                    num=value['num']
                ))

        return self.find(id, True)

    def delete(self, id):
        person = self.find(id, True)
        person.deleted_at = datetime.datetime.now()
        self.update(id, person)

    def find(self, id, with_trash=False):
        query = '''
        SELECT {}
        FROM people
        WHERE id = %s {}
        LIMIT 1
        '''.format(', '.join(self.columns),
                   'AND deleted_at IS NULL' if not with_trash else '')
        cursor = db.execute_sql(query, (id,))
        return models.Person(**dict(zip(self.columns, cursor.fetchone()))) if cursor.rowcount > 0 else None
    
    def findByCpf(self, cpf, with_trash=False):
        query = '''
        SELECT {}
        FROM people
        WHERE cpf = %s {}
        LIMIT 1
        '''.format(', '.join(self.columns),
                   'AND deleted_at IS NULL' if not with_trash else '')
        cursor = db.execute_sql(query, (cpf,))
        return models.Person(**dict(zip(self.columns, cursor.fetchone()))) if cursor.rowcount > 0 else None

    def all(self, with_trash=False):
        query = '''
        SELECT {}
        FROM people
        {}
        '''.format(', '.join(self.columns),
                   'WHERE deleted_at IS NULL' if not with_trash else '')
        cursor = db.execute_sql(query)
        return (models.Person(**dict(zip(self.columns, r))) for r in cursor)


class EmailRepository(object):

    def create(self, values):
        query = '''
        INSERT INTO emails (person_id, email)
        VALUES (%s, %s)
        '''
        db.execute_sql(query, (values['person_id'],
                               values['email']))

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


class ContactRepository(object):

    def create(self, values):
        query = '''
        INSERT INTO contacts (person_id, ddd, num)
        VALUES (%s, %s, %s)
        '''
        db.execute_sql(query, (
            values['person_id'],
            values['ddd'],
            values['num']
        ))

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
