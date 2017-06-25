# luna/server/models.py

from luna.server.repositories import EmailRepository, ContactRepository


class User(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)
        self.deleted_at = kwargs.get('deleted_at', None)

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

    def __iter__(self):
        yield('id', self.id)
        yield('username', self.username)
        yield('password', self.password)
        yield('created_at', self.created_at)
        yield('updated_at', self.updated_at)
        yield('deleted_at', self.deleted_at)


class Person(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.name = kwargs.get('name', None)
        self.cpf = kwargs.get('cpf', None)
        self.facebook = kwargs.get('facebook', None)
        self.twitter = kwargs.get('twitter', None)
        self.birth = kwargs.get('birth', None)
        self.address = kwargs.get('address', None)
        self.complement = kwargs.get('complement', None)
        self.postal_code = kwargs.get('postal_code', None)
        self.neighborhood = kwargs.get('neighborhood', None)
        self.city_id = kwargs.get('city_id', None)
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)
        self.deleted_at = kwargs.get('deleted_at', None)
    
    def emails(self):
        return EmailRepository.allByPerson(self.id)
    
    def contacts(self):
        return ContactRepository.allByPerson(self.id)

    def __repr__(self):
        return '<Person {}>'.format(self.cpf)

    def __iter__(self):
        yield('id', self.id)
        yield('name', self.name)
        yield('cpf', self.cpf)
        yield('facebook', self.facebook)
        yield('twitter', self.twitter)
        yield('birth', self.birth)
        yield('address', self.address)
        yield('complement', self.complement)
        yield('postal_code', self.postal_code)
        yield('neighborhood', self.neighborhood)
        yield('city_id', self.city_id)
        yield('created_at', self.created_at)
        yield('updated_at', self.updated_at)
        yield('deleted_at', self.deleted_at)
