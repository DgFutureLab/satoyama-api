import unittest
import app
import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
import json
import os
from test_helpers import ApiTester

class NodeResourceTests(unittest.TestCase, ApiTester):

	def setUp(self):
		app.conf.config_test_env(flapp)
		app.database.recreate()
		
	################################################################################
	### Tests for node REST URLs [GET, POST] /node
	################################################################################

	def test_GET_existing_node_by_id(self):
	 	Node.create() # create the node that we want to get
	 	url = flapp.get_url('node', node_id = 1)
	 	# url = "http://localhost:8081/node"
	 	print url
	 	r = requests.get(url, data = {'node_id' : 1})
	 	api_response = self.assert_all_ok(r)

	def test_GET_nonexisting_node_by_id(self):
		url = flapp.get_url('node')
		r = requests.get(url, data = {'node_id' : 100000000})
		self.assert_all_ok(r, expect_success = False)	
 
	def test_POST_node(self):
		url = flapp.get_url('node')
		r = requests.post(url, data = {'alias' : 'mynode'})
		api_response = self.assert_all_ok(r)
		

# 	################################################################################
# 	### Tests for /node/all
# 	################################################################################

	def test_GET_all_nodes_response_status(self):
		"""
		Tests that GET /node/all gives a valid HTTP 200 response
		"""
		for i in range(100): Node.create(alias = i)
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = r.ok

	def test_GET_all_nodes_response_content_is_correct(self):
		"""
		Test that GET /node/all gives a JSON response that has no errors in it, and that an ApiResponse object can be instantiated from the response body.
		"""
		for i in range(10): Node.create(alias = i)
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = self.assert_all_ok(r)

	def test_GET_all_nodes_response_content_matches_spec(self):
		"""
		Test that GET /node/all gives a JSON response that conforms to the Api specifications (e.g. returns a JSON serialized ApiResponse object that
			can be loaded as a ApiResponse object)
		
		"""
		for i in range(10): Node.create(alias = i)

		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = self.assert_all_ok(r)
		for obj in api_response.objects:
			assert obj.has_key('id')
