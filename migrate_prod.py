from app import flapp, conf
from satoyama.database import manager as db_manager
conf.configure_flapp('production')

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import argparse


from satoyama.models import *
from satoyama.database import Base

migrate = Migrate(flapp, Base)
migration_manager = Manager(flapp)
migration_manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	migration_manager.run()