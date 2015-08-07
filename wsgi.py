import argparse

from app import conf
from app import flapp as application
from satoyama.definitions import ENVIRONMENTS

def run_webserver(name, env):
	conf.configure_flapp(env)
	application.logger.debug('Running webserver with config: %s'%application.config)
	application.run()


if __name__ == "__main__":
	run_webserver('webserver', 'development')
