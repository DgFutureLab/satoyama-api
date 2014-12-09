import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
import seeds
from seeds.nodes import NodeSeeder
from app.helpers import ApiResponseHelper

class ReadingResourceTests(DBTestBase):


	#	###############################################################################
	#	### Tests for reading GET /reading/node_:id/distance
	#			  http://127.0.0.1/node/:node_id/sensor/:sensor_id?from_date=&to_date=
			      # http://127.0.0.1/node/:node_id 

	#   ### TODO: http://127.0.0.1/reading?node_id=1&sensor_id
	#	###############################################################################

	def test_GET_reading_by_nodeid_and_sensorid(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 1)
		sensor = node.sensors[0]
		reading = sensor.readings[0]
		url = flapp.get_url('reading', 'node_%s'%node.id, sensor.alias)
		response = requests.get(url)
		api_response = ApiResponseHelper.assert_all_ok(response)
		
		assert api_response.objects[0] == reading.json()


	def test_that_when_the_user_does_a_get_request_to_a_reading_it_will_get_single_reading(self):
		"""
		Make ten readings for a sensor, and make sure that we only get one reading back
		"""
		NodeSeeder.seed_ricefield_node(n_readings = 10)
		url = flapp.get_url('reading', 'node_1', 'distance')
		r = requests.get(url)
		
		api_response = ApiResponseHelper.get_api_response(r)
		assert len(api_response.objects) == 1 ### This call should only return a single reading
		assert api_response.objects[0].has_key('value')