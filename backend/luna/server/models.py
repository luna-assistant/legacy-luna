# luna/server/models.py

from luna.server.repositories import EmailRepository, ContactRepository, \
    PeopleAssociatedRepository, PersonRepository, UserRepository, RoleRepository


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
        return UserRepository().allByRole(self.id)

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class UserHasRole(Model):

    table = 'user_has_roles'
    primary_key = ('user_id', 'role_id')

    columns = [
        'user_id',
        'role_id'
    ]

    def __repr__(self):
        return '<UserHasRole {}.{}>'.format(self.user_id, self.role_id)


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
        return PersonRepository().findByUser(self.id)

    @property
    def roles(self):
        return RoleRepository().allByUser(self.id)

    def has_role(self, role_id):
        return (role_id in (role.id for role in self.roles))

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

    @property
    def associated(self):
        return PeopleAssociatedRepository().allByPerson(self.id)

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


class PersonAssociated(Model):

    table = 'people_associated'

    columns = [
        'id',
        'person_id',
        'associated_id'
    ]

    def __repr__(self):
        return '<PersonAssociated {}-{}>'.format(self.person_id, self.associated_id)
