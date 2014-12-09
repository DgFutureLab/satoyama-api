import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from helpers import ApiResponseHelper

class NodeResourceTests(DBTestBase):

	#	###############################################################################
	#	### Tests for node REST URLs [GET, POST] /node
	#	###############################################################################


	def test_GET_existing_node_by_id(self):
	 	Node.create() # create the node that we want to GET
	 	url = flapp.get_url('node', node_id = 1)
	 	response = requests.get(url, data = {'node_id' : 1})
	 	ApiResponseHelper.assert_all_ok(response)

	def test_GET_nonexisting_node_by_id(self):
		url = flapp.get_url('node')
		r = requests.get(url, data = {'node_id' : 100000000})
		ApiResponseHelper.assert_all_ok(r, expect_success = False)	
 
	def test_POST_create_node(self):
		url = flapp.get_url('node')
		r = requests.post(url, data = {'alias' : 'mynode'})
		ApiResponseHelper.assert_all_ok(r)
		

	# 	################################################################################
	# 	### Tests for /node/all
	#	################################################################################


	def test_GET_all_nodes_HTTP_response_status(self):
		"""
		Tests that GET /node/all gives a valid HTTP 200 response
		"""
		NodeSeeder.seed_ricefield_node()
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		assert r.ok

	def test_GET_all_nodes_ApiResponse_status(self):
		"""
		Test that GET /node/all gives a JSON response that has no errors in it, and that an ApiResponse object can be instantiated from the response body.
		"""
		NodeSeeder.seed_ricefield_node(n_readings = 3)
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = self.assert_all_ok(r)
		# assert api_response.ok

	def test_GET_all_nodes_response_content_matches_spec(self):
		"""
		Test that GET /node/all gives a JSON response that corresponds to the spec:

		{"query": {}, "errors": [], "objects": [{"alias": alias, "latitude": null, "sensors": [], "type": "", "id": id}]}
		"""
		SiteSeeder.seed_ricefield_site(n_nodes = 3)
		url = flapp.get_url('node', 'all')
		r = requests.get(url)
		api_response = self.assert_all_ok(r)
		assert len(api_response.objects) == 3
		assert len(api_response.errors) == 0

		for obj in api_response.objects:
			assert obj.has_key('id')
		for obj in api_response.objects:
			assert obj.has_key('latitude')
		for obj in api_response.objects:
			assert obj.has_key('longitude')
		for obj in api_response.objects:
			assert obj.has_key('sensors')

		for obj in api_response.objects:
			sensors = obj['sensors']
			for sensor in sensors:
				assert sensor.has_key('latest_reading')

	# def test_generic_consistency_database_json_response(self):
	# 	nodes_before = [Node.create(alias = i) for i in range(10)]
	# 	# Get JSON response
	# 	wipe database
	# 	nodes_after = create database objects from json response
	# 	assert nodes_before.json() == nodes_after.json()
