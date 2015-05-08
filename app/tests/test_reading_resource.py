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
		
	def test_GET_nonexisting_reading_by_id_failure(self):
		"""
		GET /reading/<int>
		"""
		url = UrlHelper.get_url(flapp, 'reading', 191230)
		response = requests.get(url)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)
	
	
	def test_GET_reading_by_sensorid_with_existing_sensor_success(self):
		"""
		GET /reading?sensor_id=<int>
		This call should return all the readings belonging to the sensor (in this case three readings)
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 3)
		sensor = node.sensors[0]
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_id' : sensor.id})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(map(lambda x: x.json(), sensor.readings)) == sorted(api_response.objects)

	def test_GET_readings_by_sensorid_with_nonexisting_sensor_response_empty(self):
		"""
		GET /reading?sensor_id=<int>
		This call should return no readings as sensor 100 does not exist
		"""
		NodeSeeder.seed_ricefield_node(n_readings = 3)
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_id' : 100})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert api_response.first() == None


	def test_GET_readings_by_nodeid_and_sensoralias_success(self):
		"""
		GET /reading?node_id=<int>&sensor_alias=<str>
		This call should return all readings belonging to the sensor in the specified node, in this case two readings
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 3)
		sensor = node.sensors[0]
		url = UrlHelper.get_url(flapp, 'readings', **{'node_id' : node.id, 'sensor_alias' : sensor.alias})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(map(lambda x: x.json(), sensor.readings)) == sorted(api_response.objects)

	def test_GET_reading_by_nodeid_but_no_sensoralias_failure(self):
		"""
		GET /reading?node_id=<int>
		This call should return an API error as specifying node_id but no sensor_alias is insuficcient to complete the query
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		url = UrlHelper.get_url(flapp, 'readings', **{'node_id' : node.id})
		response = requests.get(url)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)


	def test_GET_reading_by_sensoralias_but_no_nodeid_failure(self):
		"""
		GET /reading?sensor_alias=<str>
		This call should return an API error as specifying sensor_alias but no node_id is insufficient to complete the query
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_alias' : sensor.alias})
		response = requests.get(url)
		assert response.ok
		ApiResponseHelper.assert_api_response(response, expect_success = False)

	def test_GET_reading_by_sensor_id_with_interval_time_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-12-2&until=2014-12-11
		This call should return all the readings created in the interval from 2014-12-2 until 2014-12-11 for a particular sensor 
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20): Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_id' : sensor.id, 'from': '2014-12-2', 'until': '2014-12-11'})
		response = requests.get(url)
		assert response.ok
		readings_in_interval = map(lambda r: r.json(), filter(lambda r: r.timestamp >= datetime(2014,12,2) and r.timestamp <= datetime(2014,12,11), sensor.readings))
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(readings_in_interval) == sorted(api_response.objects)


	def test_GET_reading_by_node_id_and_sensor_alias_with_interval_time_filtering_success(self):
		"""
		GET /reading?node_id=<int>&sensor_alias=<str>&from=2014-12-2&until=2014-12-11
		This call should return all the readings created in the interval from 2014-12-2 until 2014-12-11 for a sensor in the specified node
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20): Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))
		url = UrlHelper.get_url(flapp, 'readings', **{'node_id' : node.id, 'sensor_alias': sensor.alias, 'from': '2014-12-2', 'until': '2014-12-11'})
		response = requests.get(url)
		assert response.ok
		readings_in_interval = map(lambda r: r.json(), filter(lambda r: r.timestamp >= datetime(2014,12,2) and r.timestamp <= datetime(2014,12,11), sensor.readings))
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(readings_in_interval) == sorted(api_response.objects)

	def test_GET_readings_by_sensor_id_with_nonsensical_time_parameters_returns_no_objects(self):
		"""
		GET /reading?node_id=<int>&sensor_alias=<str>&from=2014-12-10&until=2013-1-1
		This call should return no objects as the specified until date is before the from_date
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		start_date = datetime(2014, 12, 1)
		for day in range(20): Reading.create(sensor = sensor, value = 17, timestamp = start_date + timedelta(days=day))
		url = UrlHelper.get_url(flapp, 'readings', **{'node_id' : node.id, 'sensor_alias': sensor.alias, 'from': '2014-12-2', 'until': '2013-1-1'})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		assert api_response.first() == None


	def test_GET_reading_by_sensor_id_with_from_date_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-12-2
		This call should return all the readings created after 2014-12-2
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0] 
		for day in range(20): Reading.create(sensor = sensor, value = 17, timestamp = datetime(2014, 12, 1) + timedelta(days=day))
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_id' : sensor.id, 'from': '2014-12-2'})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		readings_in_interval = map(lambda r: r.json(), filter(lambda r: r.timestamp >= datetime(2014,12,2), sensor.readings))
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(readings_in_interval) == sorted(api_response.objects)

	def test_GET_reading_by_sensor_id_with_until_date_filtering_success(self):
		"""
		GET /reading?sensor_id=<int>&from=2014-1-1&until=2014-2-1
		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 0)
		sensor = node.sensors[0]
		for day in range(20): Reading.create(sensor = sensor, value = 17, timestamp = datetime(2014, 12, 1) + timedelta(days=day))
		url = UrlHelper.get_url(flapp, 'readings', **{'sensor_id' : sensor.id, 'until': '2014-12-1'})
		response = requests.get(url)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		readings_in_interval = map(lambda r: r.json(), filter(lambda r: r.timestamp <= datetime(2014,12,1), sensor.readings))
		api_response = ApiResponseHelper.assert_api_response(response)
		assert sorted(readings_in_interval) == sorted(api_response.objects)


	# def test_GET_all_readings(self):
	# 	"""
	# 	GET /readings
	# 	"""
	# 	NodeSeeder.seed_ricefield_node(n_readings = 3)
	# 	n_readings = len(Reading.query.all())
	# 	url = UrlHelper.get_url(flapp, 'readings')
	# 	response = requests.get(url)
	# 	assert response.ok
	# 	api_response = ApiResponseHelper.assert_api_response(response)
	# 	assert len(api_response.objects) == n_readings 

