import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import yaml
import inspect
import os
from definitions import ENVIRONMENTS

Base = declarative_base()

# default_db_uri = {
# 		'test' : 'postgresql://halfdan:halfdan@localhost/tekrice_test',
# 		'dev' :	'postgresql://halfdan:halfdan@localhost/tekrice_dev',
# 		'prod' : 'postgresql://halfdan:halfdan@localhost/tekrice_prod'
# 			}



# CURRENT_ENVIRONMENT = 'dev'



class DBManager(object):

	def __init__(self, env):
		self.set_database_environment(env)

	def set_database_environment(self, env):
		assert env in ENVIRONMENTS
		self.env = env
		self.set_databases()
		self.__confdb__()

	def set_databases(self):
		dbconfig_path = 'db_config.yml'
		# dbconfig_path = '%s/db_config.yml'%'/'.join(__file__.split('/')[:-2])
		with open(dbconfig_path) as f:
			f = f.read()
			try:
				dbconfig = yaml.load(f)
			except Exception:
				print 'Could not parse db_config.yaml. Did you follow the instructions in the README? :)'
				sys.exit(1)

		username = dbconfig[self.env]['username']
		password = dbconfig[self.env]['password']
		dbname = dbconfig[self.env]['dbname']
		dbhost = dbconfig[self.env]['dbhost']
		self.dburi = 'postgresql://%s:%s@%s/%s'%(username, password, dbhost, dbname)

	def __confdb__(self):
		self.engine = create_engine(self.dburi, convert_unicode = True)
		self.session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
		Base.query = self.session.query_property()

	def nuke_db(self):
		import models
		self.session.close()
		Base.metadata.drop_all(bind=self.engine)

	def init_db(self):
		import models
	    # import all modules here that might define models so that
	    # they will be registered properly on the metadata.  Otherwise
	    # you will have to import them first before calling init_db()
		Base.metadata.create_all(bind=self.engine)

	def recreate(self):
		self.nuke_db()
		self.init_db()

	def get_db_URI(self):
		return self.dburi

manager = DBManager('development')

# engine = create_engine('postgresql://halfdan:halfdan@localhost/tekrice_dev', convert_unicode = True)
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()



# Base = declarative_base()
# engine = create_engine(db_uri[CURRENT_ENVIRONMENT], convert_unicode = True)
# session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# def get_base():
# 	import models
# 	engine = get_engine()
# 	session = get_session(engine)
	
# 	Base.query = session.query_property()
# 	Base.metadata.bind = engine
# 	return Base


# def get_db_URI():
# 	return db_uri[CURRENT_ENVIRONMENT]


# def nuke_db():
# 	# assert isinstance(engine )
# 	import models
# 	get_session(get_engine()).close()
# 	get_base().metadata.drop_all(bind=get_engine())

# def init_db():
# 	import models
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
# 	get_base().query = get_session().query_property()
# 	get_base().metadata.create_all(bind=get_engine())

# def recreate():
# 	nuke_db()
# 	init_db()


# def get_engine():
# 	engine = create_engine(db_uri[CURRENT_ENVIRONMENT], convert_unicode = True)
# 	return engine


# def get_session(engine):
# 	session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
# 	# session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 	get_base().query = session.query_property()
# 	# setattr(Base, 'query', session.query_property())
# 	return session


def get_defined_models():
	import models
	import sqlalchemy
	members = dict(inspect.getmembers(models))
	members.pop('Base')
	models = list()
	for name, member in members.items():
		if isinstance(member, sqlalchemy.ext.declarative.api.DeclarativeMeta):
			models.append(member)
	return models