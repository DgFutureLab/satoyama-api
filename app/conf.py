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
			'HOST' : 'http://127.0.0.1',
			'PORT' : 8081,
			'LOGLEVEL' : 'DEBUG',
			'ENVIRONMENT' : 'TEST',
}

APP_DEV_SETTINGS = {
			'DEBUG' : True,
			'PROPAGATE_EXCEPTIONS' : False,
			'HOST' : 'http://127.0.0.1',
			'PORT' : 8080,
			'LOGLEVEL' : 'DEBUG',
			'ENVIRONMENT' : 'DEVELOPMENT',
}

APP_PROD_SETTINGS = {
			'DEBUG' : True,
			'PROPAGATE_EXCEPTIONS' : False,
			'HOST' : 'http://107.170.251.142',
			'PORT' : 80,
			'LOGLEVEL' : 'WARNING',
			'ENVIRONMENT' : 'PRODUCTION',
}


def configure_flapp(env):
	flapp.config.update(shared_config)

	if env == 'test':
		flapp.config.update(APP_TEST_SETTINGS)
		limiter.enabled = False

	elif env == 'dev':
		flapp.config.update(APP_DEV_SETTINGS)
	elif env == 'production':
		flapp.config.update(APP_PROD_SETTINGS)

	configure_database(env)


def configure_database(env):
	manager.set_environment(env)
	flapp.config.update({'SQLALCHEMY_DATABASE_URI' : manager.get_db_URI()})
	setattr(flapp, 'engine', manager.engine)
	setattr(flapp, 'db_session', manager.session)
	

