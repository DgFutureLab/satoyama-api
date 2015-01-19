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
	def seed_new_node(node_type):
		assert node_type in satoyama.nodetypes.keys(), 'Node type "%s" does not exist on this server'%node_type

	
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

		

		node_type = NodeType.query.filter(NodeType.name == 'ricefield').first()
		if not node_type: node_type = NodeType.create(name = 'ricefield')

		node = Node.create(node_type = node_type, alias = alias, latitude = latitude, longitude = longitude, site = site)

		st_temp = SensorType.query.filter(SensorType.unit == 'C' and SensorType.name == 'temperature').first()
		if not st_temp: st_temp = SensorType.create(unit = 'C', name = 'temperature')
		st_dist = SensorType.query.filter(SensorType.unit == 'cm' and SensorType.name == 'distance').first()
		if not st_dist: st_dist = SensorType.create(unit = 'cm', name = 'distance')
		st_humidity = SensorType.query.filter(SensorType.unit == '%' and SensorType.name == 'humidity').first()
		if not st_humidity: st_humidity = SensorType.create(unit = '%', name = 'humidity')
		st_voltage = SensorType.query.filter(SensorType.unit == 'V' and SensorType.name == 'voltage').first()
		if not st_voltage: st_voltage = SensorType.create(unit = 'V', name = 'voltage')

		Sensor.create(sensortype = st_temp, node = node, alias = 'temperature')
		Sensor.create(sensortype = st_dist, node = node, alias = 'distance')
		Sensor.create(sensortype = st_humidity, node = node, alias = 'humidity')
		Sensor.create(sensortype = st_voltage, node = node, alias = 'vbat')

		for sensor in node.sensors:
			for r in range(n_readings):
				Reading.create(sensor = sensor, value = random())
		return node


	
