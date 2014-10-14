import argparse
from app import flapp, conf, socketio
import os

def run_webserver(env):
	conf.configure_flapp(flapp, env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	socketio.run(flapp, port = flapp.config['PORT'])

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--env', choices = ('test', 'dev', 'prod'), required = True, help = 'Specify environment, which determines which database to use.')
	args = parser.parse_args()
	environment = args.env
	run_webserver(environment)
	
