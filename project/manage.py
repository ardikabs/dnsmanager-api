import os
import unittest
from server import make_server
from server.app import db
from server.main.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = make_server("default")
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def recreatedb():
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('server/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manager.command
def seeding():
    RecordTypeModel.seeding()

@manager.command
def run():
    app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    manager.run()