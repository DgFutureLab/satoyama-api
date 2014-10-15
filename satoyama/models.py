from app import flapp
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.exc import DataError
from sqlalchemy.orm import object_mapper, class_mapper, relationship
from collections import Iterable
from helpers import DatetimeHelper
import json



def create(model):						### 'create' is the name of the decorator
	@staticmethod
	def autocommit(*args, **kwargs): 		### Gets arguments for the object to create
		try:
			instance = model(*args, **kwargs) 	### Instance is created		
		except Exception, e:
			flapp.db_session.rollback()
			raise e

		if instance:
			try:
				flapp.db_session.add(instance)			### ..added to the session
				flapp.db_session.commit()					### ..inserted to the database
				if isinstance(instance, Reading):   ### If the new object is a Reading, add it as the lastest reading of the sensor
					instance.sensor.latest_reading = json.dumps(instance.json('sensor', 'sensor_id'))				
				return instance 					### ..and returned to the caller
			except Exception, e:
				flapp.db_session.rollback()
				print 'ARGAJS', e

	model.create = autocommit 			###	The model class (e.g. Node, Sensor, etc, is given a create method which calls the inner function) 		
	return model						### The decorated model class is returned and replaces the origin model class

class SatoyamaBase(object):

	def __init__(self, for_testing = False):
		"""
		:param for_testing: When you want to do something like creating satoyama models from a json parsed response
		 from the API, such as you would when writing tests.
		"""
		# self.messages = list()
		# if not inspect.stack()[4][3] == 'autocommit' or not for_testing:
		# 	raise Exception('Please use the "create" method to create instances that are meant to be commited to the database, or set the for_testing argument to True')
		pass		

	def json(self, *exclude_fields):
		print 'IN PARENT', exclude_fields
		jsondict = {}
		for prop in object_mapper(self).iterate_properties: 
			if not prop.key in exclude_fields:
				attr = getattr(self, prop.key)	
				if hasattr(attr, '__iter__'):
					# If the attribute is iterable (such as Node.sensors), each item in the iterable must be converted to a string.
					attr = map(lambda x: json.loads(repr(x)) if isinstance(self, SatoyamaBase) else x, attr)
				jsondict.update({prop.key: attr})
		jsondict.update({'type': str(type(self))})
		return jsondict

	@classmethod
	def settables(cls):
		"""
		Returns a list of which fields in the inhereted model can be set when instantiating the class.
		"""
		return filter(lambda x: x != 'id', [p.key for p in class_mapper(cls).iterate_properties])

	@classmethod
	def deep_validate_pars(cls, **kwargs):
		"""
		This methods takes the dictionary provided in kwargs and tries to make an instance AND 
		insert that instance into the database. If it succeeds, it deletes the row, and returns True. 
		If it fails to instantiate OR insert, it returns False.
		"""
		# columns = sqlalchemy.inspection.inspect(cls).columns
		# relationships = sqlalchemy.inspection.inspect(cls).relationships
		

		# valid = True
		# for k, v in kwargs.items():
		# 	if k in columns.keys():
		# 		valid &= type(v) == columns.get(k).type.python_type
		# 	elif not k in relationships.keys():
				
		# 		valid = False
		# return valid
		try:
			instance = cls.create(**kwargs)
			cls.query.filter_by(id = instance.id).delete()
			return True
		except Exception, e:
			return False


@create
class Node(SatoyamaBase, Base):
	
	__tablename__ = 'nodes'
	
	id = Column( Integer, primary_key = True )
	alias = Column( String(100) )
	sensors = relationship('Sensor', backref = 'node')
	longitude = Column( Float()) 
	latitude = Column( Float())

	def __init__(self, alias = None, sensors = [], longitude = None, latitude = None, **kwargs):
		super(Node, self).__init__(**kwargs)
		assert isinstance(sensors, Iterable), 'sensors must be iterable'
		for sensor in sensors:
			assert isinstance(sensor, Sensor), 'Each item in sensors must be an instance of type Sensor'
			self.sensors.append(sensor)

		self.longitude = longitude
		self.latitude = latitude
		self.alias = alias

	def __repr__(self):
		json_dict = {'type' : str(self.__class__)}
		if self.alias: 
			json_dict.update({'alias' : self.alias})
		else: 
			json_dict.update({'id' : self.id})
		return json.dumps(json_dict)

@create
class SensorType(SatoyamaBase, Base):
	__tablename__ = 'sensortypes'

	id = Column( Integer, primary_key = True)
	name = Column( String() )
	unit = Column( String() )
	sensors = relationship('Sensor', backref = 'sensortype')

	def __init__(self, name, unit, **kwwargs):
		super(SensorType, self).__init__()
		self.name = name
		self.unit = unit

	def __repr__(self):
		json_dict = {'type' : str(self.__class__)}
		if self.name: 
			json_dict.update({'name' : self.name})
		else: 
			json_dict.update({'id' : self.id})
		return json.dumps(json_dict)

@create
class Sensor(SatoyamaBase, Base):
	__tablename__ = 'sensors'
	
	id = Column( Integer, primary_key = True )
	alias = Column( String() )
	readings = relationship('Reading', backref = 'sensor')
	latest_reading = Column( String() )
	node_id = Column( Integer, ForeignKey('nodes.id') )
	sensortype_id = Column( Integer, ForeignKey('sensortypes.id') )
	
	def __init__(self, sensortype, node, alias = None, readings = [], **kwargs):
		super(Sensor, self).__init__(**kwargs)
		assert isinstance(sensortype, SensorType), 'sensortype must be an instance of type SensorType'
		assert isinstance(node, Node), 'node must be an instance of type Node'
		assert isinstance(readings, Iterable), 'readings must iterable'
		
		self.sensortype = sensortype
		self.node = node
		self.alias = alias
		self.latest_reading = None
		
		for reading in readings:
			assert isinstance(reading, Reading), 'Each item in readings must be an instance of type Reading'
			self.readings.append(reading)

	def __repr__(self):
		json_dict = {'type' : str(self.__class__), 'latest_reading' : self.latest_reading}
		if self.alias: 
			json_dict.update({'alias' : self.alias})
		else: 
			json_dict.update({'id' : self.id})
		return json.dumps(json_dict)

@create
class Reading(SatoyamaBase, Base):
	__tablename__ = 'readings'

	id = Column( Integer, primary_key = True )
	timestamp = Column( DateTime() )
	value = Column( Float() )
	sensor_id = Column( Integer, ForeignKey('sensors.id') )

	def __init__(self, sensor, value = None, timestamp = None, **kwargs):
		super(Reading, self).__init__(**kwargs)
		self.sensor = sensor
		# sensor.latest_reading = self	
		if value:
			try:
				self.value = float(value)
			except DataError, e:
				value = None
				raise e

		self.timestamp = DatetimeHelper.convert_timestamp_to_datetime(timestamp)
	
	def json(self, *exclude_fields):
		print exclude_fields
		json_dict = super(Reading, self).json('timestamp', *exclude_fields)
		json_dict.update({'timestamp': DatetimeHelper.convert_datetime_to_timestamp(self.timestamp)})
		return json_dict

	def __repr__(self):
		json_dict = {'type' : str(self.__class__)}
		if self.value: 
			json_dict.update({'value' : self.value})
		else: 
			json_dict.update({'id' : self.id})
		return json.dumps(json_dict)

