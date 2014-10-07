import unittest
import app
import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
import json
from test_helpers import ApiTester
from uuid import uuid4



class TestSpecialCalls(unittest.TestCase, ApiTester):



	def setup(self):
		app.database.recreate()


	def test_node_all(self):
		for i in range(100): Node.create(alias = i)
		
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = self.assert_all_ok(r)
		# for i in range(100):
		# assert api_response.objects[i].alias in range(100)
		# assert len(api_response.objects) == 100
