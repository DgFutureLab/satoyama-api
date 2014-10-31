import uuid
from satoyama.models import *
from nodes import NodeSeeder
from random import random


def seed_singlenode_network(n_readings = 10):
	node = Node.create(alias = uuid.uuid4().hex)
	st = SensorType('Sonar', 'cm')
	sensor = Sensor.create(node = node, sensortype = st, alias = 'distance')
	for i in range(n_readings):
		Reading.create(sensor = sensor, value = random())

	return node


def seed_singlenode_site(n_readings = 5):
	node = seed_singlenode_network(n_readings)
	site = Site.create(alias = uuid.uuid4().hex, nodes = [node])
	return site


class SiteSeeder():
	@staticmethod
	def seed_ricefield_site(n_nodes = 1, max_readings_per_node = 5):
		site = Site.create(alias = 'site_%s'%uuid.uuid4().hex)
		nodes = [NodeSeeder.seed_ricefield_node(site = site) for i in range(n_nodes)]
		return nodes