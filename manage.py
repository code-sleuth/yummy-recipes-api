from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import set_app, db

app = set_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    tests = unittest.TestLoader().discover('./tests', pattern='unit*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == "__main__":
    manager.run()
