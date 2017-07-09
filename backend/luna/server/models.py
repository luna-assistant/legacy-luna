# luna/server/models.py

from luna.server import repositories


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
        return repositories.UserRepository().allByRole(self.id)

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
        return repositories.PersonRepository().findByUser(self.id)

    @property
    def roles(self):
        return repositories.RoleRepository().allByUser(self.id)

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
    def user(self):
        return repositories.UserRepository().find(self.user_id)
    
    @property
    def first_name(self):
        if self.name is None:
            return None
        return self.name.split(' ', 1)[0]

    @property
    def emails(self):
        return repositories.EmailRepository().allByPerson(self.id)

    @property
    def contacts(self):
        return repositories.ContactRepository().allByPerson(self.id)

    @property
    def associated(self):
        return repositories.PeopleAssociatedRepository().allByPerson(self.id)

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
        return '<PersonAssociated {}->{}>'.format(self.person_id, self.associated_id)


class ModuleType(Model):

    table = 'module_types'
    columns = [
        'id',
        'name',
        'icon',
        'description'
    ]
    
    @property
    def informations(self):
        return repositories.InformationRepository().allByModuleType(self.id)
        
    @property
    def commands(self):
        return repositories.CommandRepository().allByModuleType(self.id)

    def __repr__(self):
        return '<ModuleType {}>'.format(self.name)


class InformationType(Model):
    DIGITAL_OUT = 1
    ANALOGIC_OUT = 2
    DIGITAL_IN = 3
    ANALOGIC_IN = 4
    PARAMETER = 5

    table = 'information_types'
    columns = [
        'id',
        'description',
    ]

    def __repr__(self):
        return '<InformationType {}>'.format(self.description)


class Information(Model):

    table = 'informations'
    columns = [
        'id',
        'name',
        'identifier',
        'description',
        'module_type_id',
        'information_type_id'
    ]
    
    @property
    def information_type(self):
        return repositories.InformationTypeRepository().find(self.information_type_id)

    def __repr__(self):
        return '<Information {}>'.format(self.name)


class CommandType(Model):
    ACTION = 1
    PARAMETER = 2
    READING = 3

    table = 'command_types'
    columns = [
        'id',
        'description',
    ]
    
    def __repr__(self):
        return '<CommandType {}>'.format(self.description)


class Command(Model):

    table = 'commands'
    columns = [
        'id',
        'name',
        'identifier',
        'description',
        'module_type_id',
        'command_type_id'
    ]
    
    @property
    def command_type(self):
        return repositories.CommandTypeRepository().find(self.command_type_id)

    def __repr__(self):
        return '<Command {}>'.format(self.name)
