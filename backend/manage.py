import os
import unittest
from app.main.service.account_service import save_new_account

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db
from app.main.model.account import Account

app = create_app(os.getenv('LAN_BACKEND_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    data = {'email': 'lan-admin@leadmove.com',
            'first_name':'admin',
            'last_name':'super',
            'role': 'admin',
            'password':'012358'
            }
    save_new_account(data=data)
@manager.command
def run():
    app.run(ssl_context=('conf/cert.pem', 'conf/key.pem'),host='0.0.0.0')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
