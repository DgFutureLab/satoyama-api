import argparse
from app import flapp, conf
from seeds.sites import SiteSeeder
from multiprocessing import Process

def run_webserver(name, env):
	conf.configure_flapp(env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	flapp.run(port = flapp.config['PORT'])


def run_simulation(site_id):
	print '*******************************   Simulating site %s'%site_id
	p = Process(target = SiteSeeder.simulate_ricefield_site, args = (site_id,))
	p.start()

import time, pytest
def run_tests():
	time.sleep(2)
	print 'RUNNING TTEEEEEEEEEEEEEEESTS!!!'
	pytest.main()

parser = argparse.ArgumentParser()
parser.add_argument('--env', choices = ('test', 'dev', 'prod'), required = True, help = 'Specify environment, which determines which database to use.')
parser.add_argument('--simulation_site', '-s', help = 'Specify the site to simulate. The site must already exist.')
args = parser.parse_args()
environment = args.env
site_id = args.simulation_site

print 'SSIIIIIIIIIIIIIITE'
print site_id

if __name__ == "__main__":
	# run_simulation(site_id)

	# Process(target = run_webserver, args = ('webserver', environment, )).start()
	# Process(target = run_tests).start()
	run_webserver('webserver', environment)
