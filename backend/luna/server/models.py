# luna/server/models.py

from luna.server.repositories import EmailRepository, ContactRepository


class Model(object):

    columns = []

    def __init__(self, **kwargs):
        for c in self.columns:
            setattr(self, c, kwargs.get(c, None))

    def __iter__(self):
        for c in self.columns:
            yield (c, getattr(self, c, None))


class User(Model):

    columns = [
        'id',
        'username',
        'password',
        'created_at',
        'updated_at',
        'deleted_at'
    ]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Person(Model):

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

    def emails(self):
        return EmailRepository.allByPerson(self.id)

    def contacts(self):
        return ContactRepository.allByPerson(self.id)

    def __repr__(self):
        return '<Person {}>'.format(self.cpf)


class Email(Model):

    columns = [
        'id',
        'person_id',
        'email'
    ]

    def __repr__(self):
        return '<Email {}>'.format(self.email)


class Contact(Model):

    columns = [
        'id',
        'person_id',
        'ddd',
        'num'
    ]

    def __repr__(self):
        return '<Contact ({}) {}>'.format(self.ddd, self.num)


class City(Model):

    columns = [
        'id',
        'federative_unit_id',
        'name',
    ]

    def __repr__(self):
        return '<City {}>'.format(self.name)
