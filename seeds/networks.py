import satoyama
from satoyama.models import Node, Sensor, SensorType, Reading
from random import randint, random
from app import flapp



#def seed_network(number_nodes = 0, sensors = ('temperature'), readings = False):


def seed_simple_network(recreate = False, env = 'dev'):
	if recreate:

		satoyama.database.recreate()
	
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