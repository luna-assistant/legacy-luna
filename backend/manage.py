# manage.py


import os
import unittest
import coverage

from flask_script import Manager

COV = coverage.coverage(
    branch=True,
    include='luna/*',
    omit=[
        'luna/tests/*',
        'luna/server/config.py',
        'luna/server/*/__init__.py'
    ]
)
COV.start()

from luna.server import app
from luna.server.models import User, Person, Role, Module, ModuleType, Command, Information
from luna.server.repositories import UserRepository, PersonRepository, UserHasRoleRepository, \
    ModuleTypeRepository,  ModuleRepository, InformationRepository, CommandRepository


manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('luna/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('luna/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates the db tables."""
    import glob

    migrations = glob.glob('migrations/*.sql')

    for migration in migrations:
        os.system('psql -h {} -d {} -U {} -a -f {}'.format(
            app.config.get('DB_HOST'),
            app.config.get('DB_DATABASE'),
            app.config.get('DB_USERNAME'),
            migration))


@manager.command
def drop_db():
    """Drops the db tables."""
    # db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    # db.session.add(User(email='ad@min.com', password='admin', admin=True))
    # db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    import datetime

    userRepo = UserRepository()
    personRepo = PersonRepository()
    userHasRoleRepo = UserHasRoleRepository()

    users = [
        { 'username': 'admin@luna.com', 'name': 'Admin', 'cpf': '11111111111', 'contact':'84912345678' },
        { 'username': 'chicobentojr@luna.com', 'name': 'Francisco Bento', 'cpf': '27280861253', 'contact':'84985296341' },
        { 'username': 'dayannemorato@luna.com', 'name': 'Dayanne Morato', 'cpf': '58864170103', 'contact':'84915978426' },
        { 'username': 'diellyviana@luna.com', 'name': 'Dielly Viana', 'cpf': '14321367719', 'contact':'84996548521' },
        { 'username': 'felipemfp@luna.com', 'name': 'Felipe Pontes', 'cpf': '74275088824', 'contact':'84925896321' },
        { 'username': 'felipebarbosa@luna.com', 'name': 'Felipe Barbosa', 'cpf': '28946848600', 'contact':'84912547896' },
        { 'username': 'yuriscosta@luna.com', 'name': 'Yuri Costa', 'cpf': '25621871219', 'contact':'84912455689' },
    ]

    for user in users:
        new_user = userRepo.findByUsername(user['username'])
        if not new_user:
            new_user = User(username=user['username'], password='mudar@123')
            new_user = userRepo.create(new_user)

            if user['username'] == 'admin@luna.com':
                userHasRoleRepo.create(dict(user_id=new_user.id, role_id=Role.ADMIN))
            else:
                userHasRoleRepo.create(dict(user_id=new_user.id, role_id=Role.COMMON))

            person = {}
            person['name'] = user['name']
            person['cpf'] = user['cpf']
            person['birth'] = datetime.datetime(1993, 2, 1)
            person['emails'] = [user['username']]
            person['contacts'] = [{
                'ddd': user['contact'][0:2],
                'num': user['contact'][2:]
            }]
            person['user_id'] = new_user.id
            personRepo.create(person)

    module_repository = ModuleRepository()
    module_type_repository = ModuleTypeRepository()
    information_repository = InformationRepository()
    command_repository = CommandRepository()

    module_types = [
        { 'name': 'Iluminação',  'description': 'Módulo de Iluminação para ambientes que precisem de claridão.', 'icon': 'idea', 'is_active': True },
        { 'name': 'Segurança',  'description': 'Módulo de segurança para travamento de portas.', 'icon': 'lock', 'is_active': True },
        { 'name': 'Torneira',  'description': 'Módulo de controle de fluxo de líquido através de torneiras.', 'icon': 'theme', 'is_active': True },
    ]

    commands = [
        { 'name': 'Ativar', 'identifier': 101, 'description': 'Ativar o módulo.', 'command_type_id': 1},
        { 'name': 'Desativar', 'identifier': 102, 'description': 'Desativar o módulo.', 'command_type_id': 1},
    ]

    informations = [
        { 'name': 'Status', 'identifier': 1, 'description': 'Verificar o status do módulo.', 'information_type_id': 1}
    ]

    module_quantity = 5

    for module_type in module_types:
        new_type = module_type_repository.findByName(module_type['name'])
        if not new_type:
            new_type = ModuleType(**module_type)
            new_type = module_type_repository.create(new_type)

            for command in commands:
                command['module_type_id'] = new_type.id
                command_repository.create(command)

            for information in informations:
                information['module_type_id'] = new_type.id
                information_repository.create(information)

            for x in range(module_quantity):
                module_repository.create(dict(module_type_id=new_type.id))


if __name__ == '__main__':
    manager.run()
