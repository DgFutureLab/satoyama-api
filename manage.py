from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import flapp, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(flapp, db)
manager = Manager(flapp)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
