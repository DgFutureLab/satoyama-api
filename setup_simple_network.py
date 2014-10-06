import satoyama
from satoyama.models import Node, Sensor, SensorType, Reading

def seed_simple_network():
	satoyama.database.recreate()
	
	collector1 = Node.create(alias = "chibi_temp_dist", latitude = 35.143951, longitude = 139.988560)
	collector2 = Node.create(alias = 'chibi_temp', latitude = 35.143945, longitude = 139.988236)
	collector3 = Node.create(alias = 'saboten_hector_desk', latitude = 35.144150, longitude = 139.988486)

	st_temp = SensorType('temperature', 'C')
	st_dist = SensorType('distance', 'cm')
	st_hum = SensorType('humidity', '%')

	Sensor.create(sensortype = st_temp, node = collector1, alias = 'temperature')
	Sensor.create(sensortype = st_dist, node = collector1, alias = 'distance')
	Sensor.create(sensortype = st_dist, node = collector1, alias = 'humidity')

	Sensor.create(sensortype = st_temp, node = collector2, alias = 'temperature')
	Sensor.create(sensortype = st_dist, node = collector2, alias = 'distance')
	Sensor.create(sensortype = st_dist, node = collector2, alias = 'humidity')

	Sensor.create(sensortype = st_dist, node = collector3, alias = 'distance')

	print '****** Nodes: ', Node.query.all()
	print '****** Sensors: ', Sensor.query.all()

	return collector1, collector2, collector3