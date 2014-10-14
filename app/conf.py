from satoyama.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

### Settings necessary to use the app in the console
### Note that enrivonment settings override module settings.
module_config = {
	'LOGLEVEL': 'DEBUG'
}

### Settings shared between environments
shared_config = {
	
	'CSRF_ENABLED': True,
	'SECRET_KEY': 'you-will-never-guess'
}

def configure_flapp(flapp, env):
	if env == 'test':
		config_test_env(flapp)
	elif env == 'dev':
		config_development(flapp)
	elif env == 'production':
		config_production(flapp)
	Base.query = flapp.db_session.query_property()

def config_production(flapp, **kwargs):
	flapp.config.update(shared_config)
	flapp.config.update(
			DEBUG = False,
			PROPAGATE_EXCEPTIONS = False,
			HOST = 'http://107.170.251.142',
			PORT = 80,
			SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/tekrice_prod",
			LOGLEVEL = 'WARNING',
			ENVIRONMENT = 'PRODUCTION',	
		)
	flapp.config.update(**kwargs)
	setattr(flapp, 'engine', create_engine(flapp.config['SQLALCHEMY_DATABASE_URI'], convert_unicode = True))
	setattr(flapp, 'db_session', scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=getattr(flapp, 'engine'))))


def config_development(flapp, **kwargs):
	flapp.config.update(shared_config)
	flapp.config.update(
			DEBUG = True,
			PROPAGATE_EXCEPTIONS = True,
			HOST = 'http://127.0.0.1',
			PORT = 8080,
			SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/tekrice_dev",
			LOGLEVEL = 'DEBUG',
			ENVIRONMENT = 'DEVELOPMENT'
		)
	flapp.config.update(**kwargs)
	setattr(flapp, 'engine', create_engine(flapp.config['SQLALCHEMY_DATABASE_URI'], convert_unicode = True))
	setattr(flapp, 'db_session', scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=getattr(flapp, 'engine'))))

def config_test_env(flapp, **kwargs):
	flapp.config.update(shared_config)
	flapp.config.update(
			DEBUG = True,
			PROPAGATE_EXCEPTIONS = False,
			HOST = 'http://127.0.0.1',
			PORT = 8081,
			SQLALCHEMY_DATABASE_URI = "postgresql://halfdan:halfdan@localhost/tekrice_test",
			LOGLEVEL = 'DEBUG',
			ENVIRONMENT = 'TEST'
		)
	flapp.config.update(**kwargs)
	setattr(flapp, 'engine', create_engine(flapp.config['SQLALCHEMY_DATABASE_URI'], convert_unicode = True))
	setattr(flapp, 'db_session', scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=getattr(flapp, 'engine'))))
