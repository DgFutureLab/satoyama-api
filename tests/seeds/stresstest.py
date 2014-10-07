from satoyama.models import *
from satoyama.database import recreate
from numpy.random import uniform, shuffle, rand
from datetime import datetime
from time import sleep

n_nodes = 100
n_sensortypes = 20
n_sensors_per_node = 10
reading_refresh_rate = 60*60


class RandomNetwork(object):
	def __init__(self, n_nodes, avr_sensors_per_node, avr_readings_per_sensor):
		self.nodes = list()
		self.sensortypes = list()
		self.sensors = list()
		for i in n_sensortypes:
			st = SensorType.create()
		# self.readings = list()

	def get_random_coordinates(self):
		return {'longitude' : uniform(139.988, 139.989), 'latitude': uniform(35.143, 35.144)}


	def add_nodes(n_nodes):
		for n in range(n_nodes):
			pass



def get_random_coordinates():
	return {'longitude' : uniform(139.988, 139.989), 'latitude': uniform(35.143, 35.144)}


def create_nodes():
	recreate()
	
	sensortypes = list()
	for n in range(n_sensortypes):
		sensortypes.append(SensorType.create(name = 'CPRT33 Sonar', unit = 'Chinese inches'))

	nodes = list()
	for n in range(n_nodes):
		coords = get_random_coordinates()
		node = Node.create(**coords)
		nodes.append(node)
		for i in range(int(uniform(1, n_sensors_per_node))): 
			shuffle(sensortypes)
			Sensor.create(sensortype = sensortypes[0], node = node, alias = 'distance')
	return nodes


def read_sensors():
	nodes = Node.query.all()
	while True:
		for node in nodes:
			for sensor in node.sensors:
				r = Reading.create(value = uniform(30, 100), sensor = sensor, timestamp = datetime.utcnow())
				print datetime.utcnow(), r
		sleep(reading_refresh_rate)


if __name__ == "__main__":
	create_nodes()
	read_sensors()
