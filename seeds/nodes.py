import satoyama
from satoyama.models import *
from uuid import uuid4
from random import random, randint
from numpy.random import uniform

def notest(func):
	setattr(func, 'notest', True)
	return func

class NodeSeeder():

	@staticmethod
	def seed_empty_node(**kwargs):
		return Node.create()

	
	@staticmethod
	@notest
	def seed_node(node_type, **kwargs):
		assert node_type in satoyama.definitions.node_types
		return getattr(NodeSeeder, 'seed_' + node_type + '_node')(**kwargs)

	@staticmethod
	def seed_ricefield_node(n_readings = 0, **node_args):
		"""
		Create a new ricefield node.
		:param n_readings: (default 0) The number of readings with random values that will be generated for each sensor in the node.
		"""
		if node_args.has_key('site'):
			site = node_args['site']
		elif node_args.has_key('site_id'):
			site = Site.query.filter_by(id = node_args['site_id']).first()
		else:
			site = None
		
		if node_args.has_key('latitude'):
			latitude = node_args['latitude']
		else:
			latitude = uniform(35.143, 35.144)
		
		if node_args.has_key('longitude'):
			longitude = node_args['longitude']
		else:
			longitude = uniform(139.988, 139.989)

		if node_args.has_key('alias'):
			alias = node_args['alias']
		else:
			alias = "ricefield_node_%s"%uuid4().hex

		node = Node.create(alias = alias, latitude = latitude, longitude = longitude, site = site)

		st_temp = SensorType('temperature', 'C')
		st_dist = SensorType('distance', 'cm')
		st_hum = SensorType('humidity', '%')

		Sensor.create(sensortype = st_temp, node = node, alias = 'temperature')
		Sensor.create(sensortype = st_dist, node = node, alias = 'distance')
		Sensor.create(sensortype = st_hum, node = node, alias = 'humidity')

		for sensor in node.sensors:
			for r in range(n_readings):
				Reading.create(sensor = sensor, value = random())
		return node


	
