from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.exc import DataError
from sqlalchemy.orm import object_mapper, class_mapper, relationship, backref
from collections import Iterable
from helpers import DatetimeHelper, JSONHelper
import json
from database import Base, manager
from datetime import datetime

def create(model):						### 'create' is the name of the decorator
	@staticmethod
	def autocommit(*args, **kwargs): 		### Gets arguments for the object to create
		try:
			instance = model(*args, **kwargs) 	### Instance is created		
		except Exception, e:
			manager.session.rollback()
			raise e
		if instance:
			try:
				manager.session.add(instance)			### ..added to the session
				if isinstance(instance, Reading):   ### If the new object is a Reading, add it as the lastest reading of the sensor
					instance.sensor.latest_reading = json.dumps(instance.json())				
				manager.session.commit()
				return instance 					### ..and returned to the caller
			except Exception, e:
				manager.session.rollback()
				print e
	model.create = autocommit 			###	The model class (e.g. Node, Sensor, etc, is given a create method which calls the inner function) 		
	return model 						### The decorated model class is returned and replaces the origin model class


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

	def insert(self):
		pass

	def json(self, column_transformations, relationship_representation):
		json_dict = {}
		json_dict.update(dict(zip(object_mapper(self).columns.keys(), map(lambda column_name: column_transformations.get(column_name, lambda x: x)(getattr(self, column_name)), object_mapper(self).columns.keys()))))
		json_dict.update(dict(zip(relationship_representation.keys(), map(lambda (relation, entry): map(lambda column: dict(zip(entry['columns'], map(lambda a: entry['transformations'].get(a, lambda x: x)(getattr(column, a)), entry['columns']))), getattr(self, relation) if isinstance(getattr(self, relation), Iterable) else [getattr(self, relation)]), relationship_representation.items()))))
		return json_dict

	@classmethod
	def settables(cls):
		"""
		Returns a list of which fields in the inhereted model can be set when instantiating the class.
		"""
		return filter(lambda x: x != 'id', [p.key for p in class_mapper(cls).iterate_properties])

	@classmethod
	def columns(cls):
		"""
		Returns a list of all columns (including relations)
		"""
		return cls.settables() + ['id']

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

	@classmethod
	def query_interval(cls, query = None, from_date = None, until_date = None):
		if not query: query = cls.query		
		if from_date: from_date = DatetimeHelper.convert_timestamp_to_datetime(from_date)
		if until_date: until_date = DatetimeHelper.convert_timestamp_to_datetime(until_date)

		if from_date and until_date:
			query = query.filter(cls.timestamp >= from_date).filter(cls.timestamp <= until_date)
		elif from_date and not until_date:
			query = query.filter(cls.timestamp >= from_date)
		elif not from_date and until_date:
			query = query.filter(cls.timestamp <= until_date)
		return query


@create
class Site(SatoyamaBase, Base):

	__tablename__ = 'sites'
	json_column_transformations = {}
	
	json_relationship_representation = {
		'nodes': {
			'columns' : ['id', 'alias', 'longitude', 'latitude', 'sensors'], 
			'transformations' : {'sensors': lambda sensors: map(lambda sensor: {'id': sensor.id, 'alias': sensor.alias, 'latest_reading': JSONHelper.load_string_safe(sensor.latest_reading)}, sensors)}
			}
		}

	id = Column( Integer, primary_key = True)
	alias = Column( String(100) )
	nodes = relationship(
		'Node',
		cascade='all,delete-orphan', 
		backref = backref('site', single_parent = True)
		)

	def __init__(self, alias = None, nodes = []):
		self.alias = alias
		assert isinstance(nodes, Iterable), 'nodes must be iterable'
		for node in nodes:
			assert isinstance(node, Node), 'Each item in nodes must be an instance of type Node'
			self.nodes.append(node)

	def json(self):
		return super(Site, self).json(Site.json_column_transformations, Site.json_relationship_representation)


	

@create
class Node(SatoyamaBase, Base):
	
	__tablename__ = 'nodes'

	json_column_transformations = {}
	json_relationship_representation = {
		'sensors': {
			'columns' : ['id', 'alias', 'latest_reading'], 
			'transformations' : {'latest_reading' : JSONHelper.load_string_safe}
			}
		}
	
	id = Column( Integer, primary_key = True )
	alias = Column( String(100) )
	longitude = Column( Float()) 
	latitude = Column( Float())

	short_address = Column(Integer, unique = True)

	sensors = relationship(
		'Sensor', 
		cascade='all,delete-orphan',
		backref = backref('node')
		)

	site_id = Column( Integer, ForeignKey('sites.id', ondelete = 'CASCADE') )

	def __init__(self, site = None, alias = None, sensors = [], longitude = None, latitude = None, **kwargs):
		super(Node, self).__init__(**kwargs)
		assert isinstance(sensors, Iterable), 'sensors must be iterable'
		for sensor in sensors:
			assert isinstance(sensor, Sensor), 'Each item in sensors must be an instance of type Sensor'
			self.sensors.append(sensor)

		self.longitude = longitude
		self.latitude = latitude
		self.alias = alias
		if site: 
			assert isinstance(site, Site), 'site must be an instance of %s'%type(Site)
			self.site = site


	def json(self):
		return super(Node, self).json(Node.json_column_transformations, Node.json_relationship_representation)

@create
class SensorType(SatoyamaBase, Base):
	__tablename__ = 'sensortypes'

	id = Column( Integer, primary_key = True)
	name = Column( String() )
	unit = Column( String() )
	
	sensors = relationship(
		'Sensor', 
		backref = backref('sensortype')
		)

	def __init__(self, name, unit, **kwwargs):
		super(SensorType, self).__init__()
		self.name = name
		self.unit = unit


@create
class Sensor(SatoyamaBase, Base):
	__tablename__ = 'sensors'
	
	json_column_transformations = {}
	json_relationship_representation = {
		'readings': {
			'columns' : ['id', 'value', 'timestamp'], 
			'transformations' : {'timestamp': DatetimeHelper.convert_datetime_to_timestamp}
			},
		'sensortype': {
			'columns' : ['unit', 'name'],
			'transformations': {}
			}
		}

	id = Column( Integer, primary_key = True )
	alias = Column( String() )
	latest_reading = Column( String() )
	
	readings = relationship(
		'Reading',
		 cascade='all,delete-orphan', 
		 backref = backref('sensor', single_parent = True)
		 )

	node_id = Column( Integer, ForeignKey('nodes.id', ondelete = 'CASCADE') )
	sensortype_id = Column( Integer, ForeignKey('sensortypes.id', ondelete = 'SET NULL') )

	#minimum_value = Column( Float, ForeignKey('nodes.id', ondelete = 'CASCADE') )
	#maximum_value = Column( Float, ForeignKey('nodes.id', ondelete = 'CASCADE') )
	
	def __init__(self, node, sensortype = None, alias = None, readings = [], **kwargs):
		super(Sensor, self).__init__(**kwargs)
		# assert isinstance(sensortype, SensorType), 'sensortype must be an instance of type SensorType'
		assert isinstance(node, Node), 'node must be an instance of type Node'
		assert isinstance(readings, Iterable), 'readings must iterable'
		
		self.sensortype = sensortype
		self.node = node
		self.alias = alias
		self.latest_reading = ''
		
		for reading in readings:
			assert isinstance(reading, Reading), 'Each item in readings must be an instance of type Reading'
			self.readings.append(reading)

	# def create(self):
	# 	### Run super create and then add latest reading things

	def json(self):
		return super(Sensor, self).json(Sensor.json_column_transformations, Sensor.json_relationship_representation)


@create
class Reading(SatoyamaBase, Base):
	__tablename__ = 'readings'

	id = Column( Integer, primary_key = True )
	timestamp = Column( DateTime() )
	value = Column( Float() )
	sensor_id = Column( Integer, ForeignKey('sensors.id', ondelete = 'CASCADE') )

	json_column_transformations = {
			'timestamp' : DatetimeHelper.convert_datetime_to_timestamp
			}
	
	json_relationship_representation = {
		'sensor': {
			'columns' : ['id', 'alias'], 
			'transformations' : {'id' : str}
			}
		}

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
		if isinstance(timestamp, datetime):
			self.timestamp = timestamp
		else:
			self.timestamp = DatetimeHelper.convert_timestamp_to_datetime(timestamp)

	def json(self):
		return super(Reading, self).json(Reading.json_column_transformations, Reading.json_relationship_representation)

