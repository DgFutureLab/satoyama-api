from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import flapp
import app
# flapp.config.from_object(os.environ['APP_SETTINGS'])
app.conf.config_development(flapp)

from satoyama.models import *
from satoyama.database import Base

# models = satoyama.database.get_defined_models()

# for model in models:
# 	migrate = Migrate(flapp, model)
# 	manager = Manager(flapp)

migrate = Migrate(flapp, Base)
manager = Manager(flapp)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
