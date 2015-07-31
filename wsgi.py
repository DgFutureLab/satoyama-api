import argparse
from app import flapp, conf
from satoyama.definitions import ENVIRONMENTS

def run_webserver(name, env):
	conf.configure_flapp(env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	flapp.run()


if __name__ == "__main__":
	run_webserver('webserver', 'development')
