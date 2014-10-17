import unittest
import app
import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
import json
import os
from test_helpers import ApiTester
from random import random, randint
import re
import seeds

class ReadingResourceTests(unittest.TestCase, ApiTester):

	def setUp(self):
		app.conf.config_test_env(flapp)
		app.database.recreate()

	def tearDown(self):
		app.flapp.db_session.remove()

	def seed_network_with_one_node_one_sensor_one_reading(self):		
		node = Node.create()
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		sensor = Sensor.create(node = node, sensortype = sensortype, alias="distance")
		reading = Reading.create(sensor = sensor, value = 2)

	#	###############################################################################
	#	### Tests for reading GET /reading/node_:id/distance
	#			  http://127.0.0.1/node/:node_id/sensor/:sensor_id?from_date=&to_date=
			      # http://127.0.0.1/node/:node_id 

	#   ### TODO: http://127.0.0.1/reading?node_id=1&sensor_id
	#	###############################################################################

	def test_GET_reading_by_nodeid_and_sensorid(self):
		self.seed_network_with_one_node_one_sensor_one_reading()
		url = flapp.get_url('reading', 'node_1', 'distance')
		r = requests.get(url)
		assert r.ok
		api_response = self.get_api_response(r)
		assert api_response.ok

	def test_that_when_the_user_does_a_get_request_to_a_reading_it_will_get_single_reading(self):
		"""
		Make ten readings for a sensor, and make sure that we only get one reading back
		"""
		seeds.networks.seed_singlenode_network(n_readings = 10)
		url = flapp.get_url('reading', 'node_1', 'distance')
		r = requests.get(url)
		
		api_response = self.get_api_response(r)
		print api_response.objects
		assert len(api_response.objects) == 1 ### This call should only return a single reading
		assert api_response.objects[0].has_key('value')