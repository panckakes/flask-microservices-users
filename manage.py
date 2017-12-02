# manage.py


import unittest
import coverage

from flask_script import Manager

from project import create_app, db
from project.api.models import User, Bluetooth


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()


app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
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
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='michael', email="michael@realpython.com"))
    db.session.add(User(username='michaelherman', email="michael@mherman.org"))
    db.session.add(Bluetooth(name='michaels_iphone', address="00:11:22:33:FF:EE"))
    db.session.add(Bluetooth(name='michaels_other_iphone', address="04:64:22:DE:AC:EE"))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
