# luna/server/models.py


# import datetime

from luna.server import app, bcrypt


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
