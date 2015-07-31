from app import debug
import config, helpers, models, database
import yaml
import os

debug(os.path.split(__file__)[0] + '/nodetypes.yml')

with open(os.path.split(__file__)[0] + '/nodetypes.yml') as f: 
	nodetypes = yaml.load(f)

# database.set_database_environment('dev')
# engine = database.get_engine()
# session = database.get_session(engine)
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
