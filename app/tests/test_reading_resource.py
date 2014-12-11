import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
import seeds
from seeds.nodes import NodeSeeder
from app.apihelpers import ApiResponseHelper, UrlHelper

class ReadingResourceTests(DBTestBase):


	#	###############################################################################
	#	### Tests for reading GET /reading/node_:id/distance
	#			  http://127.0.0.1/node/:node_id/sensor/:sensor_id?from_date=&to_date=
			      # http://127.0.0.1/node/:node_id 

	#   ### TODO: http://127.0.0.1/reading?node_id=1&sensor_id
	#	###############################################################################

	def test_GET_existing_reading_by_id_success(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		reading = Reading.create(sensor = sensor, value = 17)
		url = UrlHelper.get_url(flapp, 'reading', 1)
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert api_response.first() == reading.json()
		# assert api_response.first()['']
	
	def test_GET_reading_by_sensorid_success(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		reading = Reading.create(sensor = sensor, value = 17)
		data = {'sensor_id' : sensor.id}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert api_response.first() == reading.json()

	def test_GET_reading_by_nodeid_and_sensoralias_success(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		reading = Reading.create(sensor = sensor, value = 17)
		data = {'node_id' : node.id, 'sensor_alias' : sensor.alias}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert api_response.first() == reading.json()

	def test_GET_reading_by_nodeid_but_no_sensoralias_failure(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		data = {'node_id' : node.id}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response, expect_success = False)

	def test_GET_reading_by_sensoralias_but_no_nodeid_failure(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		data = {'sensor_alias' : sensor.alias}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response, expect_success = False)
	# def test_GET_all_readings(self):
	# 	NodeSeeder.seed_ricefield_node(n_readings = 3)
	# 	n_readings = len(Reading.query.all())
	# 	url = UrlHelper.get_url(flapp, 'readings')
	# 	response = requests.get(url)
	# 	assert response.ok
	# 	api_response = ApiResponseHelper.assert_api_response(response)
	# 	assert len(api_response.objects) == n_readings 






	# 	# print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
		# print api_response
		# assert api_response.objects[0] == reading.json()


	# def test_that_when_the_user_does_a_get_request_to_a_reading_it_will_get_single_reading(self):
	# 	"""
	# 	Make ten readings for a sensor, and make sure that we only get one reading back
	# 	"""
	# 	NodeSeeder.seed_ricefield_node(n_readings = 10)
	# 	url = flapp.get_url('reading', 'node_1', 'distance')
	# 	r = requests.get(url)
		
	# 	api_response = ApiResponseHelper.get_api_response(r)
	# 	assert len(api_response.objects) == 1 ### This call should only return a single reading
	# 	assert api_response.objects[0].has_key('value')