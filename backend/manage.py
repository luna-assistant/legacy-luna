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
from luna.server.models import User, Person
from luna.server.repositories import UserRepository, PersonRepository


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
            userRepo.create(new_user)

            person = {}
            person['name'] = user['name']
            person['cpf'] = user['cpf']
            person['birth'] = datetime.datetime(1993, 2, 1)
            person['emails'] = [user['username']]
            person['contacts'] = [{
                'ddd': user['contact'][0:2],
                'num': user['contact'][2:]
            }]
            # person = Person(person)
            personRepo.create(person)

    # usuario = userRepo.findByUsername('felipempf')
    # personRepo = PersonRepository()
    #
    # carol = User(username='carolina', password='mudar@123')
    # carol = userRepo.create(carol)
    #
    # carolPerson = Person(name='Carolina da Silva', cpf='18434621924', birth=datetime.datetime(1993, 3, 2))
    # carolPerson = personRepo.create(carolPerson)
    # carolPerson.address = 'Av. Senador Cunha, 122'
    # carolPerson.complement = 'Bloco H Ap. 201'
    # carolPerson.postal_code = '59000000'
    # carolPerson.neighborhood = 'Vinheiros'
    # carolPerson = personRepo.update(carolPerson.id, carolPerson)
    #
    # carolPerson = personRepo.findByCpf('18434621924')
    # if carolPerson:
    #     carolPerson = dict(carolPerson)
    #     carolPerson['emails'] = ['carolinasilva@gmail.com', 'carolsilva@outlook.com']
    #     carolPerson['contacts'] = [dict(ddd='84', num='998665596')]
    #     carolPerson = personRepo.update(carolPerson['id'], carolPerson)


if __name__ == '__main__':
    manager.run()
