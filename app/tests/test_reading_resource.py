import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
import seeds
from seeds.nodes import NodeSeeder
from app.apihelpers import ApiResponseHelper, UrlHelper
from datetime import datetime, timedelta
class ReadingResourceTests(DBTestBase):


	#	###############################################################################
	#	### Tests for reading GET /reading/node_:id/distance
	#			  http://127.0.0.1/node/:node_id/sensor/:sensor_id?from_date=&to_date=
			      # http://127.0.0.1/node/:node_id 

	#   ### TODO: http://127.0.0.1/reading?node_id=1&sensor_id
	#	###############################################################################

	def test_GET_existing_reading_by_id_success(self):
		"""
		GET /reading/<int>
		"""
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
		"""
		GET /reading?sensor_id=<int>
		"""
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
		"""
		GET /reading?node_id=<int>&sensor_alias=<str>
		"""
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
		"""
		GET /reading?node_id=<int>
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		data = {'node_id' : node.id}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)

	def test_GET_reading_by_sensoralias_but_no_nodeid_failure(self):
		"""
		GET /reading?sensor_alias=<str>
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		data = {'sensor_alias' : sensor.alias}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)

	def test_GET_reading_by_sensor_id_with_interval_time_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-1-1&until=2014-2-1
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20):
			Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))

		data = {'sensor_id' : sensor.id, 'from': '2014-12-1', 'until': '2014-12-11'}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert len(api_response.objects) == 11


	def test_GET_reading_by_node_id_and_sensor_alias_with_interval_time_filtering_success(self):
		"""
		GET /reading?node_id=<int>&sensor_alias=<str>&from=2014-1-1&until=2014-2-1
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20):
			Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))

		data = {'node_id' : node.id, 'sensor_alias': sensor.alias, 'from': '2014-12-1', 'until': '2014-12-11'}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert len(api_response.objects) == 11


	def test_GET_reading_by_sensor_id_with_from_date_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-1-1&until=2014-2-1
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20):
			Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))

		data = {'sensor_id' : sensor.id, 'from': '2014-12-1'}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert len(api_response.objects) == 20

	def test_GET_reading_by_sensor_id_with_until_date_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-1-1&until=2014-2-1
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20):
			Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))

		data = {'sensor_id' : sensor.id, 'until': '2014-12-1'}
		url = UrlHelper.get_url(flapp, 'reading')
		response = requests.get(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert len(api_response.objects) == 1


	def test_GET_reading_by(self):
		pass

	def test_GET_all_readings(self):
		"""
		GET /nodes
		"""
		NodeSeeder.seed_ricefield_node(n_readings = 3)
		n_readings = len(Reading.query.all())
		url = UrlHelper.get_url(flapp, 'readings')
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert len(api_response.objects) == n_readings 

