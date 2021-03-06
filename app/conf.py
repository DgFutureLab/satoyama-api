from satoyama.database import manager

from app import flapp, limiter
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

APP_TEST_SETTINGS = {
			'DEBUG' : True,
			'PROPAGATE_EXCEPTIONS' : False,
			'PORT' : 8081,
			'LOGLEVEL' : 'DEBUG',
			'ENVIRONMENT' : 'TEST',
}

APP_DEV_SETTINGS = {
			'DEBUG' : True,
			'PROPAGATE_EXCEPTIONS' : False,
			'PORT' : 8080,
			'LOGLEVEL' : 'DEBUG',
			'ENVIRONMENT' : 'DEVELOPMENT',
}

APP_PROD_SETTINGS = {
			'DEBUG' : True,
			'PROPAGATE_EXCEPTIONS' : False,
			'PORT' : 8081,
			'LOGLEVEL' : 'WARNING',
			'ENVIRONMENT' : 'PRODUCTION',
}


def configure_flapp(env):
	flapp.config.update(shared_config)

	if env == 'test':
		flapp.config.update(APP_TEST_SETTINGS)
		limiter.enabled = False

	elif env == 'development':
		flapp.config.update(APP_DEV_SETTINGS)
	elif env == 'production':
		flapp.config.update(APP_PROD_SETTINGS)
	else:
		assert False, 'Please specify a valid environment'

	__configure_database(env)



def __configure_database(env):
	manager.set_database_environment(env)
	flapp.config.update({'SQLALCHEMY_DATABASE_URI' : manager.get_db_URI()})
	setattr(flapp, 'engine', manager.engine)
	setattr(flapp, 'db_session', manager.session)
	

