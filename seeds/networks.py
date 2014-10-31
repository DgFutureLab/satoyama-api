import satoyama
# from satoyama.models import Node, Sensor, SensorType, Reading
from random import randint, random
import uuid
from satoyama.models import *

#def seed_network(number_nodes = 0, sensors = ('temperature'), readings = False):

# class NetworkManager(object):

def seed_singlenode_network(n_readings = 10):
	node = Node.create(alias = uuid.uuid4().hex)
	st = SensorType('Sonar', 'cm')
	sensor = Sensor.create(node = node, sensortype = st, alias = 'distance')
	for i in range(n_readings):
		Reading.create(sensor = sensor, value = random())

	return node


def seed_singlenode_site(n_readings = 5):
	node = seed_singlenode_network(n_readings)
	site = Site.create(alias = uuid.uuid4().hex, nodes = [node])
	return site



def seed_simple_network(recreate = False, env = 'dev'):
	if recreate:
		satoyama.database.manager.recreate()
	
	node1 = Node.create(alias = "chibi_temp_dist", latitude = 35.143951, longitude = 139.988560)
	node2 = Node.create(alias = 'chibi_temp', latitude = 35.143945, longitude = 139.988236)
	node3 = Node.create(alias = 'saboten_hector_desk', latitude = 35.144150, longitude = 139.988486)

	st_temp = SensorType('temperature', 'C')
	st_dist = SensorType('distance', 'cm')
	st_hum = SensorType('humidity', '%')

	Sensor.create(sensortype = st_temp, node = node1, alias = 'temperature')
	Sensor.create(sensortype = st_dist, node = node1, alias = 'distance')
	Sensor.create(sensortype = st_hum, node = node1, alias = 'humidity')

	Sensor.create(sensortype = st_temp, node = node2, alias = 'temperature')
	Sensor.create(sensortype = st_dist, node = node2, alias = 'distance')
	Sensor.create(sensortype = st_dist, node = node2, alias = 'humidity')
	Sensor.create(sensortype = st_dist, node = node3, alias = 'distance')

	nodes = [node1, node2, node3]

	for node in nodes:
		for sensor in node.sensors:
			for r in range(0, randint(0, 100)):
				Reading.create(sensor = sensor, value = random())

	return nodes


if __name__ == "__main__":
	seed_simple_network()