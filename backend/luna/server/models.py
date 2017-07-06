# luna/server/models.py

from luna.server.repositories import PersonRepository, EmailRepository, ContactRepository


class Model(object):

    primary_key = 'id'
    columns = []

    def __init__(self, **kwargs):
        for c in self.columns:
            setattr(self, c, kwargs.get(c, None))

    def __iter__(self):
        for c in self.columns:
            yield (c, getattr(self, c, None))


class Role(Model):

    ADMIN = 1
    COMMON = 2
    ASSOCIATED = 3

    table = 'roles'

    columns = [
        'id',
        'name',
        'display_name'
    ]

    @property
    def users(self):
        return []

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(Model):

    table = 'users'

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

    @property
    def person(self):
        return PersonRepository().findByUserId(self.id)

    @property
    def roles(self):
        return []

    def has_role(self, role_id):
        return False

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Person(Model):

    table = 'people'

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
        'user_id',
        'city_id',
        'created_at',
        'updated_at',
        'deleted_at'
    ]

    @property
    def first_name(self):
        if self.name is None:
            return None
        return self.name.split(' ', 1)[0]

    @property
    def emails(self):
        return EmailRepository().allByPerson(self.id)

    @property
    def contacts(self):
        return ContactRepository().allByPerson(self.id)

    def __repr__(self):
        return '<Person {}>'.format(self.cpf)


class Email(Model):

    table = 'emails'

    columns = [
        'id',
        'person_id',
        'email'
    ]

    def __repr__(self):
        return '<Email {}>'.format(self.email)


class Contact(Model):

    table = 'contacts'

    columns = [
        'id',
        'person_id',
        'ddd',
        'num'
    ]

    def __repr__(self):
        return '<Contact ({}) {}>'.format(self.ddd, self.num)


class FederativeUnit(Model):

    table = 'federative_units'

    columns = [
        'id',
        'country_id',
        'name',
        'abbr'
    ]

    def __repr__(self):
        return '<FederativeUnit {}>'.format(self.name)


class City(Model):

    table = 'cities'

    columns = [
        'id',
        'federative_unit_id',
        'name',
    ]

    def __repr__(self):
        return '<City {}>'.format(self.name)
