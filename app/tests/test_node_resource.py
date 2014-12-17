import requests
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from app.apihelpers import ApiResponseHelper, UrlHelper
from satoyama.models import Node




class NodeResourceTests(DBTestBase):

	#	###############################################################################
	#	### Tests for node REST URLs [GET, POST] /node
	#	###############################################################################


	def test_GET_existing_node_by_id(self):
	 	node = NodeSeeder.seed_empty_node()
	 	url = UrlHelper.get_url(flapp, 'node', node.id)
	 	response = requests.get(url)
	 	assert response.ok
	 	api_response = ApiResponseHelper.assert_api_response(response)
	 	assert api_response.objects[0] == node.json()
	 	

	def test_GET_node_by_id_fails_when_node_id_is_not_int(self):
		node_id = 'NOT AN INTEGER'
	 	url = UrlHelper.get_url(flapp, 'node', node_id)
	 	response = requests.get(url)
	 	assert not response.ok

	def test_GET_nonexisting_node_by_id(self):
		url = UrlHelper.get_url(flapp, 'node', '123123123')
		response = requests.get(url)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)	

 
	def test_POST_create_node_with_existing_site(self):
		site = SiteSeeder.seed_empty_site()
		url = UrlHelper.get_url(flapp, 'node')
		data = {'alias':'mynode', 'site_id': site.id, 'latitude' : 13.2, 'longitude': 23.2}
		response = requests.post(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		node = Node.query.first().json()
		assert node == api_response.first()
		
	def test_POST_create_node_with_nonexisting_site(self):
		url = UrlHelper.get_url(flapp, 'node')
		data = {'alias':'mynode', 'site_id': 1111111111, 'latitude' : 13.2, 'longitude': 23.2}
		response = requests.post(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		node = Node.query.first().json()
		assert node == api_response.first()
		

	# 	################################################################################
	# # 	### Tests for /node/all
	# #	################################################################################


	def test_GET_nodes_HTTP_response_status(self):
		"""
		Tests that GET /node/all gives a valid HTTP 200 response
		"""
		NodeSeeder.seed_ricefield_node()
		url = UrlHelper.get_url(flapp, 'nodes')
		response = requests.get(url)
		assert response.ok

	def test_GET_nodes_ApiResponse_status(self):
		"""
		Test that GET /node/all gives a JSON response that has no errors in it, and that an ApiResponse object can be instantiated from the response body.
		"""
		for i in range(5): NodeSeeder.seed_ricefield_node(n_readings = 3)
		url = UrlHelper.get_url(flapp, 'node', 'all')
		r = requests.get(url)
		api_response = ApiResponseHelper.assert_api_response(r)
		assert api_response.ok
		nodes = map(lambda n: n.json(), Node.query.all())
		assert sorted(nodes) == sorted(api_response.objects)






