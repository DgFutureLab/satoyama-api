from satoyama.models import *
from satoyama import nodetypes
from dbtestbase import DBTestBase
from uuid import uuid4
from satoyama.helpers import DatetimeHelper, JSONHelper
from datetime import datetime
from random import random
from seeds.sites import SiteSeeder
from seeds.nodes import NodeSeeder




class TestSensorTypeModel(DBTestBase):

	def test_sensortype_insert(self):
		name = uuid4().hex
		unit = uuid4().hex
		SensorType.create(name = name, unit = unit)
		sensortype_retrieved = SensorType.query.first()
		assert sensortype_retrieved.name == name
		assert sensortype_retrieved.unit == unit


class TestSiteModel(DBTestBase):
	def test_site_insert(self):
		site_alias = 'silly site'
		site_inserted = Site.create(alias = site_alias)
		site_retrieved = Site.query.first()
		assert site_inserted.alias == site_retrieved.alias

	def test_site_json_method(self):
		site = SiteSeeder.seed_ricefield_site()
		site_json = site.json()
		JSONHelper.test_model_json_method(Site, site_json)


class TestNodeModel(DBTestBase):

	def test_node_insert(self):
		node_inserted = NodeSeeder.seed_node('ricefield', alias = uuid4().hex)
		node_retrieved = Node.query.first()
		assert node_inserted.id == node_retrieved.id
		assert node_inserted.alias == node_retrieved.alias

	def test_add_sensors_to_node(self):
		node_inserted = NodeSeeder.seed_node('empty')
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		for i in range(3): Sensor.create(sensortype = sensortype, node = node_inserted)
		node_retrieved = Node.query.first()
		assert node_inserted.sensors == node_retrieved.sensors

	def test_node_json_method(self):
		node = NodeSeeder.seed_ricefield_node(n_readings = 3)
		node_json = node.json()
		JSONHelper.test_model_json_method(Node, node_json)


class TestSensorModel(DBTestBase):

	def test_sensor_insert(self):
		alias = uuid4().hex
		node = NodeSeeder.seed_node('ricefield')
		n_sensors_expected = nodetypes['ricefield']['sensors'].__len__()
		assert Sensor.all().__len__() == n_sensors_expected
		# sensortype = SensorType(name = 'Sonar', unit = 'm')
		# sensor_inserted = Sensor.create(node = node, sensortype = sensortype, alias = alias)
		# sensor_retrieved = Sensor.query.first()
		# assert sensor_retrieved.alias == sensor_inserted.alias
		# # assert sensortype_retrieved.node

	def test_sensor_json_method(self):
		sensor = NodeSeeder.seed_ricefield_node(n_readings = 3).sensors[0]
		sensor_json = sensor.json()
		JSONHelper.test_model_json_method(Sensor, sensor_json)

	# def test_sensor_latest_reading(self):
	# 	"""
	# 	Test that the latest reading 
	# 	Create a network without any readings, as we want to insert a reading with a
	# 	"""
	# 	timestamp = datetime.now()
	# 	timestamp_str = DatetimeHelper.convert_datetime_to_timestamp(timestamp)
		
	# 	sensor = NodeSeeder.seed_ricefield_node(n_readings = 0).sensors[0]
	# 	value = random()
	# 	Reading.create(sensor = sensor, timestamp = timestamp, value = value)
		
	# 	latest_reading = json.loads(sensor.latest_reading)
	# 	assert isinstance(latest_reading, dict)
	# 	assert latest_reading.has_key('timestamp')
	# 	assert latest_reading.has_key('value')
	# 	assert latest_reading.has_key('sensor_id')

	# 	assert latest_reading['timestamp'] == timestamp_str
	# 	assert round(latest_reading['value'], 10) == round(value, 10)
	# 	print latest_reading
	# 	assert latest_reading['sensor_id'] == sensor.id


