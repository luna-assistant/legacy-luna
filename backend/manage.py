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
from luna.server.models import User
from luna.server.repositories import UserRepository


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
    userRepository = UserRepository()
    
    felipe = next(userRepository.findByField('username', 'pontes'))
    
    if felipe:
        felipe.username = 'felipemfp'
        felipe.password = 'mudar@123'
        userRepository.update(felipe.id, felipe, update_password=True)
    
    # felipe = User(username='felipemfp', password='senha')
    # felipe = userRepository.create(felipe)
    
    # felipe.username = 'pontes'
    # felipe = userRepository.update(felipe.id, felipe)    


if __name__ == '__main__':
    manager.run()