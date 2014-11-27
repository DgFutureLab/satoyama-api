import argparse
from app import flapp, conf, socketio
# import os
# from threading import Thread
from seeds.sites import SiteSeeder
from multiprocessing import Process

def run_webserver(name, env):
	conf.configure_flapp(env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	socketio.run(flapp, port = flapp.config['PORT'])

# import subprocess

def run_simulation(site_id):
	print '*******************************   Simulating site %s'%site_id
	p = Process(target = SiteSeeder.simulate_ricefield_site, args = (site_id,))
	p.start()


parser = argparse.ArgumentParser()
parser.add_argument('--env', choices = ('test', 'dev', 'prod'), required = True, help = 'Specify environment, which determines which database to use.')
parser.add_argument('--simulation_site', '-s', default = 2, help = 'Specify the site to simulate. The site must already exist.')
args = parser.parse_args()
environment = args.env
site_id = args.simulation_site



if __name__ == "__main__":
	run_simulation(site_id)
	run_webserver('webserver', environment)
