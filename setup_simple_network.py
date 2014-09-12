import satoyama
from satoyama.models import Node, Sensor, SensorType, Reading

if __name__ == "__main__":
	satoyama.database.recreate()
	
	collector1 = Node.create(alias = "chibi_temp_dist")
	collector2 = Node.create(alias = 'chibi_temp')
	collector3 = Node.create(alias = 'saboten_hector_desk')

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