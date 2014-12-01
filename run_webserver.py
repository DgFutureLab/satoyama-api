import argparse
from app import flapp, conf
from satoyama.definitions import ENVIRONMENTS

def run_webserver(name, env):
	conf.configure_flapp(env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	flapp.run(port = flapp.config['PORT'])


parser = argparse.ArgumentParser()
parser.add_argument('--env', choices = ENVIRONMENTS, required = True, help = 'Specify environment, which determines which database to use.')
parser.add_argument('--simulation_site', '-s', help = 'Specify the site to simulate. The site must already exist.')
args = parser.parse_args()
environment = args.env
site_id = args.simulation_site

if __name__ == "__main__":
	run_webserver('webserver', environment)
