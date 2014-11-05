import satoyama
from satoyama.models import *
from uuid import uuid4
from random import random, randint
from numpy.random import uniform


class NodeSeeder():

	@staticmethod
	def seed_empty_node():
		return Node.create()


	@staticmethod
	def seed_ricefield_node(n_readings = 0, **node_args):
		if node_args.has_key('site'):
			site = node_args['site']
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


	
