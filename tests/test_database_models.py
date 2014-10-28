from satoyama.models import *
from seeds import networks
from apitestbase import ApiTestBase
from uuid import uuid4

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
		node = Node.create()
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		sensors = [Sensor.create(sensortype = sensortype, node = node) for i in range(5)]
		print sensors
		print node.sensors
		assert sensors == node.sensors

	# def test_node_JSON_method(self):
	# 	"""
	# 	Tests that a node with a sensor with some readings is 
	# 	"""

	# 	node = networks.seed_singlenode_network(n_readings = 5)
	# 	try:
	# 		json.
	# 	except TypeError:
	# 		assert False


class TestSensorModel(ApiTestBase):

	def test_sensor_insert(self):
		alias = uuid4().hex
		node = Node()
		sensortype = SensorType(name = 'Sonar', unit = 'm')
		sensor_inserted = Sensor.create(node = node, sensortype = sensortype, alias = alias)
		sensor_retrieved = Sensor.query.first()
		assert sensor_retrieved.alias == alias
		# assert sensortype_retrieved.node

	def test_sensor_json_method(self):
		pass

	def test_sensor_latest_reading(self):
		pass
