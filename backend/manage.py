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
    # import datetime
    # 
    # userRepo = UserRepository()
    # usuario = userRepo.findByUsername('felipempf')
    # print(usuario)
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
    
    # carolPerson = personRepo.findByCpf('18434621924')
    # if carolPerson:
    #     carolPerson = dict(carolPerson)
    #     carolPerson['emails'] = ['carolinasilva@gmail.com', 'carolsilva@outlook.com']
    #     carolPerson['contacts'] = [dict(ddd='84', num='998665596')]
    #     carolPerson = personRepo.update(carolPerson['id'], carolPerson)


if __name__ == '__main__':
    manager.run()