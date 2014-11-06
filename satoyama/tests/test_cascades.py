from satoyama.models import *
from seeds.sites import SiteSeeder
from seeds.nodes import NodeSeeder
from dbtestbase import DBTestBase

class TestCascades(DBTestBase):

	def test_site_forward_cascade(self):
		"""
		Deleting a site should delete all the associated nodes

		"""
		SiteSeeder.seed_ricefield_site(n_nodes = 3)
		assert Site.query.count() == 1
		assert Node.query.count() > 0
		Site.query.delete()
		assert Site.query.count() == 0
		assert Node.query.count() == 0

	
	def test_site_backwards_cascade(self):
		"""
		Deleting an object referenced by a site should NOT delete the site
		"""
		SiteSeeder.seed_ricefield_site(n_nodes = 3)
		assert Site.query.count() == 1
		assert Node.query.count() > 0
		
		n_deleted = Node.query.delete()
		
		assert n_deleted == 3
		assert Site.query.count() == 1
		assert Node.query.count() == 0

	
	def test_node_forward_cascade(self):
		"""
		Deleting a node should delete all the associated sensors

		"""
		NodeSeeder.seed_ricefield_node()
		assert Node.query.count() == 1
		assert Sensor.query.count() > 0
		Node.query.delete()
		assert Node.query.count() == 0
		assert Sensor.query.count() == 0

	def test_node_backwards_cascade(self):
		"""
		Deleting an object referenced by a node should NOT delete the node
		"""
		NodeSeeder.seed_ricefield_node()
		assert Node.query.count() == 1
		assert Sensor.query.count() > 0
		Sensor.query.delete()
		assert Node.query.count() == 1
		assert Sensor.query.count() == 0

	
	def test_sensor_forward_cascade(self):
		"""
		Deleting a sensor should delete all the associated readings

		"""
		n_readings = 5
		NodeSeeder.seed_ricefield_node(n_readings = n_readings)
		assert Sensor.query.count() > 0 ## >0 in case number of sensors are changed in the seed method
		assert Reading.query.count() > 0
		Sensor.query.delete()
		assert Sensor.query.count() == 0
		assert Reading.query.count() == 0		


	def test_sensor_backward_cascade(self):
		"""
		Deleting an object referenced by a sensor should NOT delete the sensor

		"""
		n_readings = 5
		node = NodeSeeder.seed_ricefield_node(n_readings = n_readings)
		n_sensors = len(node.sensors)
		
		assert Sensor.query.count() > 0 ## >0 in case number of sensors are changed in the seed method
		assert Reading.query.count() > 0
		
		Reading.query.delete()
		
		assert Sensor.query.count() == n_sensors
		assert Reading.query.count() == 0


	def test_sensortype_forward_cascade(self):
		"""
		Deleting a sensortype should NOT delete any associated sensors

		"""
		node = NodeSeeder.seed_ricefield_node(n_readings = 5)
		n_sensors_before_delete = Sensor.query.count()

		assert SensorType.query.count() > 0
		assert Sensor.query.count() > 0
		
		n_deleted = SensorType.query.filter_by(id = node.sensors[0].sensortype.id).delete()

		assert n_deleted == 1
		assert Sensor.query.count() == n_sensors_before_delete

	def test_sensortype_backwards_cascade(self):
		"""
		Deleting an object referenced by a sensortype should NOT delete the sensortype
		"""
		n_readings = 5
		NodeSeeder.seed_ricefield_node(n_readings = n_readings)
		n_sensortypes_before_delete = SensorType.query.count()

		assert SensorType.query.count() > 0
		assert Sensor.query.count() > 0
		
		Sensor.query.delete()
		
		assert Sensor.query.count() == 0
		assert SensorType.query.count() == n_sensortypes_before_delete







