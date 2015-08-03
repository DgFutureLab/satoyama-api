import config, helpers, models, database, definitions
import yaml
import os


with open(os.path.split(__file__)[0] + '/nodetypes.yml') as f: 
	nodetypes = yaml.load(f)

# database.set_database_environment('dev')
# engine = database.get_engine()
# session = database.get_session(engine)
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
