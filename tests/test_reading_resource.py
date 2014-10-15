import unittest
import app
import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
import json
import os
from test_helpers import ApiTester
from random import random

class ReadingResourceTests(unittest.TestCase, ApiTester):

	def setUp(self):
		app.conf.config_test_env(flapp)
		app.database.recreate()

	
	def seed_network_with_readings(self):		


		nodes = [Node.create(alias = i) for i in range(2)]
		sensortype = SensorType.create(name = 'Robot sonar', unit = 'm')
		for node in nodes:
			node.sensors = [Sensor.create(node = node, sensortype = sensortype) for i in range(2)]
			for sensor in node.sensors:
				for r in range(0, randint(0, 10)):
					Reading.create(sensor = sensor, value = random())

	#	###############################################################################
	#	### Tests for reading GET /reading/node_:id/distance
	#   ### TODO: http://127.0.0.1/reading?node_id=1&sensor_
	#	###############################################################################

	# def test_GET_reading_by_nodeid_and_sensorid(self):
	# 	readings = Reading.query.all()
	# 	for reading in readings:
	# 		sensor = Sensor.query.filter_by(id = reading.sensor_id)
	# 		url = flapp.get_url('reading', 'node_%s'%sensor.node_id, 'sensor_%s'%sensor.id)
	# 		print url





	
