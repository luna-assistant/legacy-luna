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
        
        query = 'INSERT INTO users ('+', '.join(self.__columns__[1:])+') VALUES (%s, %s, %s, %s, %s) RETURNING id'
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
            'SELECT ' + ', '.join(self.__columns__) + ' FROM users WHERE id = %s LIMIT 1',
            (id,))
        return models.User(**dict(zip(self.__columns__, cursor.fetchone())))

    def findByField(self, field, value):
        cursor = db.execute_sql(
            'SELECT ' + ', '.join(self.__columns__) + ' FROM users WHERE %s = %s',
            (AsIs(field), value,))
        return (models.User(**dict(zip(self.__columns__, record))) for record in cursor)

    def all(self):
        cursor = db.execute_sql('SELECT ' + ', '.join(self.__columns__) + ' FROM users')
        return (models.User(**dict(zip(self.__columns__, record))) for record in cursor)
