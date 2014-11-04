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
	def seed_ricefield_node(n_nodes = 3, **kwargs):
		if kwargs.has_key('site'):
			site = kwargs['site']
		else:
			site = None
		
		if kwargs.has_key('latitude'):
			latitude = kwargs['latitude']
		else:
			latitude = uniform(35.143, 35.144)
		
		if kwargs.has_key('longitude'):
			longitude = kwargs['longitude']
		else:
			longitude = uniform(139.988, 139.989)


		node = Node.create(alias = "chibi_temp_dist_%s"%uuid4().hex, latitude = latitude, longitude = longitude, site = site)

		st_temp = SensorType('temperature', 'C')
		st_dist = SensorType('distance', 'cm')
		st_hum = SensorType('humidity', '%')

		Sensor.create(sensortype = st_temp, node = node, alias = 'temperature')
		Sensor.create(sensortype = st_dist, node = node, alias = 'distance')
		Sensor.create(sensortype = st_hum, node = node, alias = 'humidity')

		for sensor in node.sensors:
			for r in range(n_nodes):
				Reading.create(sensor = sensor, value = random())
		return node


	
