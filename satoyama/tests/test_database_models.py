from satoyama.models import *
from seeds import networks
from apitestbase import ApiTestBase
from uuid import uuid4
from satoyama.helpers import DatetimeHelper
from datetime import datetime
from random import random
# class ModelTester(ApiTestBase):

class TestSensorTypeModel(ApiTestBase):

	def test_sensortype_insert(self):
		name = uuid4().hex
		unit = uuid4().hex
		SensorType.create(name = name, unit = unit)
		sensortype_retrieved = SensorType.query.first()
		assert sensortype_retrieved.name == name
		assert sensortype_retrieved.unit == unit


class TestNodeModel(ApiTestBase):

	def test_node_insert(self):
		node_alias = uuid4().hex
		node_inserted = Node.create(alias = node_alias)
		node_retrieved = Node.query.first()
		assert node_inserted.id == node_retrieved.id
		assert node_inserted.alias == node_retrieved.alias

	def test_add_sensors_to_node(self):
		node_inserted = Node.create()
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		for i in range(3): Sensor.create(sensortype = sensortype, node = node_inserted)
		node_retrieved = Node.query.first()
		assert node_inserted.sensors == node_retrieved.sensors

	def test_node_JSON_method(self):
		"""
		Tests that a node with a sensor with some readings is JSON serializable.
		"""

		node = networks.seed_singlenode_network(n_readings = 3)
		try:
			json.dumps(node.json())
		except TypeError:
			assert False


class TestSensorModel(ApiTestBase):

	def test_sensor_insert(self):
		alias = uuid4().hex
		node = Node()
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		sensor_inserted = Sensor.create(node = node, sensortype = sensortype, alias = alias)
		sensor_retrieved = Sensor.query.first()
		assert sensor_retrieved.alias == sensor_inserted.alias
		# assert sensortype_retrieved.node

	def test_sensor_json_method(self):
		sensor = networks.seed_singlenode_network(n_readings = 3).sensors[0]
		try:
			json.dumps(sensor.json())
		except TypeError:
			assert False

	def test_sensor_latest_reading(self):
		"""
		Test that the latest reading 
		Create a network without any readings, as we want to insert a reading with a
		"""
		timestamp = datetime.now()
		timestamp_str = DatetimeHelper.convert_datetime_to_timestamp(timestamp)
		
		sensor = networks.seed_singlenode_network(n_readings = 0).sensors[0]
		value = random()
		Reading.create(sensor = sensor, timestamp = timestamp, value = value)
		
		latest_reading = json.loads(sensor.latest_reading)
		assert isinstance(latest_reading, dict)
		assert latest_reading.has_key('timestamp')
		assert latest_reading.has_key('value')
		assert latest_reading.has_key('sensor_id')

		assert latest_reading['timestamp'] == timestamp_str
		assert round(latest_reading['value'], 10) == round(value, 10)
		assert latest_reading['sensor_id'] == sensor.id



