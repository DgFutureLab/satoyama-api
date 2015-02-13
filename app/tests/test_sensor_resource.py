from seeds.nodes import NodeSeeder
from app import flapp
import requests
from satoyama.tests.dbtestbase import DBTestBase
from app.apihelpers import UrlHelper, ApiResponseHelper
from satoyama.models import SensorType

# class SensorResourceTests(DBTestBase):
	
	# def test_GET_existing_sensor_by_id(self):
	# 	"""
	# 	Creates a ricefield node and tests that all three sensors can be accessed via the API
	# 	"""
	# 	node = NodeSeeder.seed_ricefield_node(n_readings = 1)
	# 	for sensor in node.sensors:
	# 		# pprint(sensor.json())
	# 		url = UrlHelper.get_url(flapp, 'sensor', sensor.id)
	#  		response = requests.get(url)
	#  		assert response.ok
	#  		api_response = ApiResponseHelper.assert_api_response(response)
	#  		assert api_response.first() == sensor.json(), 'First item in the api response was supposed to be sensor 1, but it was not'


	# def test_GET_nonexisting_sensor_by_id(self):
	#  	"""
	#  	Tries to GET a nonexising sensor
	#  	"""
	#  	url = UrlHelper.get_url(flapp, 'sensor', 1111111111)
	#  	response = requests.get(url)
	#  	assert response.ok
	#  	api_response = ApiResponseHelper.assert_api_response(response, expect_success = False)
	#  	assert len(api_response.objects) == 0, 'The sensor does not exist, so the api should not return any objects'


	# def test_POST_sensor_with_node_and_sensortype_success(self):
	# 	st = SensorType.create(name = 'sonar', unit = 'cm')
	# 	node = NodeSeeder.seed_node('empty')
	# 	url = UrlHelper.get_url(flapp, 'sensor')
	# 	data = {'alias' : 'myawesomesensor', 'sensortype' : st.name, 'node_id' : node.id}
	# 	response = requests.post(url, data = data)
	# 	assert response.ok
	# 	api_response = ApiResponseHelper.assert_api_response(response, expect_success = True)
	# 	assert api_response.first()['alias'] == 'myawesomesensor'
	# 	assert api_response.first()['latest_reading'] == ''


	# def test_POST_sensor_without_node_or_sensortype_failure(self):
	# 	url = UrlHelper.get_url(flapp, 'sensor')
	# 	data = {'alias' : 'myawesomesensor'}
	# 	response = requests.post(url, data = data)
	# 	assert response.ok
	# 	ApiResponseHelper.assert_api_response(response, expect_success = False)
