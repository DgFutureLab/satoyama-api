import satoyama
from satoyama.models import *
from uuid import uuid4
from random import random, randint

class NodeSeeder():

	@staticmethod
	def seed_empty_node():
		return Node.create()


	@staticmethod
	def seed_ricefield_node(max_readings_per_node = 5, **kwargs):
		if kwargs.has_key('site'):
			site = kwargs['site']
		else:
			site = None

		node = Node.create(alias = "chibi_temp_dist_%s"%uuid4().hex, latitude = 35.143951, longitude = 139.988560, site = site)

		st_temp = SensorType('temperature', 'C')
		st_dist = SensorType('distance', 'cm')
		st_hum = SensorType('humidity', '%')

		Sensor.create(sensortype = st_temp, node = node, alias = 'temperature')
		Sensor.create(sensortype = st_dist, node = node, alias = 'distance')
		Sensor.create(sensortype = st_hum, node = node, alias = 'humidity')

		for sensor in node.sensors:
			for r in range(0, randint(0, max_readings_per_node)):
				Reading.create(sensor = sensor, value = random())
		return node


	
