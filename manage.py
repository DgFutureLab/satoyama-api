from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import argparse
from satoyama.database import manager as db_manager
from app import flapp

from satoyama.models import *
from satoyama.database import Base



# parser = argparse.ArgumentParser()
# parser.add_argument('--env', choices = ('test', 'dev', 'prod'), required = True, help = 'Specify environment, which determines which database to use.')
# args = parser.parse_args()
# environment = args.env
# db_manager.set_environment(environment)

migrate = Migrate(flapp, Base)
migration_manager = Manager(flapp)

# class Print(Command):

#         def run(self):
#             print "hello"

# def test():
# 	print 'HUUUUUUUUUUUUU'



# migration_manager.add_command('test', Print)
migration_manager.add_command('db', MigrateCommand)
# 




if __name__ == '__main__':

	

	migration_manager.run()