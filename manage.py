from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db, Book, User

migrate = Migrate(app, db)
# migrate will be used to handle the migrations for the project

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()