import uuid
import satoyama
from satoyama.models import *

from nodes import NodeSeeder
from random import random
from datetime import datetime
from multiprocessing import Process
from numpy.random import shuffle
import time

def notest(func):
	setattr(func, 'notest', True)
	return func



class SiteSeeder():
	@staticmethod
	def seed_empty_site(site_alias = None):
		return Site.create(alias = site_alias)

	@staticmethod
	def seed_ricefield_site(site_alias = None, n_nodes = 1, n_readings = 5, **kwargs):
		if not site_alias: 
			site_alias = 'site_%s'%uuid.uuid4().hex
		site = Site.create(alias = site_alias)
		nodes = [NodeSeeder.seed_ricefield_node(n_readings = n_readings, site = site, **kwargs) for i in range(n_nodes)]
		return site

	@staticmethod
	@notest
	def simulate_ricefield_site(site_id, n_nodes = 100, site_alias = None):
		site = Site.query.filter_by(id = site_id).first()
		if not site:
			if n_nodes and site_alias:
				site = Site.create(alias = site_alias)
				for n in xrange(n_nodes):
					NodeSeeder.seed_ricefield_node(n_readings = 0, site = site)
			else:
				print 'No site with the supplied site_id was found. In this case you must supply values for both n_nodes and site_alias. Returning None'
				return

		def run_simulation(site):
			total_sensors = sum([len(node.sensors) for node in site.nodes])
			wait = 3600.0 / total_sensors
			node_ids = map(lambda node: node.id, site.nodes)
			shuffle(node_ids)
			print 'Simulating site %s with nodes %s'%(site.id, node_ids)
			while True:
				for node_id in node_ids:
					node = Node.query.filter_by(id = node_id).first()
					for sensor in node.sensors:
						r = Reading.create(sensor = sensor, value = random() * 100, timestamp = datetime.now())
						print 'Created reading %s at site %s, node %s'%(r, site.id, node.id)
						time.sleep(wait)

		run_simulation(site)
		# Process(target = run_simulation, args = (site, )).start()




