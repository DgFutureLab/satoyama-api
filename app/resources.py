from app import rest_api, flapp
from satoyama.models import Node, Sensor, Reading
import exc
from flask.ext import restful
from flask import request
from sqlalchemy.exc import DataError
import zlib
import sys
import json
from datetime import datetime, timedelta

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}


class ApiResponse(object):
	"""
	Designed so that client_side_response = ApiResponse(**server_side_response.json())
	where server_side_response is itself an ApiResponse instance
	"""
	__fields__ = ['errors', 'objects', 'query']

	def __init__(self, request = None, query = {}, objects = [], errors = []):
		"""
		kwargs is a dict which can contains the keys 'warnings', 'errors' and 'objects', each of which maps to an item which 
		can be a iterable of serializable objects, or just a single object. This is intended to make writing tests easier, as
		the json() serialization of an ApiResponse instance will always be contained in the HTTP response from the API.
		"""
		self.errors = list()
		self.objects = list()
		self.ok = True
		
		if request:
			if hasattr(request, 'form'):
				self.query = request.form
		else:
			self.query = {}	

		if self.is_json(objects):
			# for obj in objects: self += obj
			self.objects = objects[:]

		if self.is_json(errors):
			self.errors = errors[:]
		
		self.__validate__()

		
	def is_json(self, obj):
		try:
			json.dumps(obj)
			return True
		except TypeError:
			return False

		
	def __iadd__(self, obj):
		if hasattr(obj, '__class__'):
			if issubclass(obj.__class__, Exception):
				self.errors.append(getattr(obj, 'message'))
			elif self.is_json(obj):
				self.objects.append(obj)
			elif hasattr(obj, 'json'):
				obj_as_json = obj.json()
				if self.is_json(obj_as_json):
					self.objects.append(obj_as_json)
				else:
					self.errors.append(exc.ApiException('object had json method, but json method did not produce json-serializable output.').__str__())
			else:
				self.errors.append(exc.ApiException('object added to response could not be json serialized').__str__())
		else:
			self.errors.append(exc.ApiException('obj has no __class__ attribute'))
		self.__validate__()
		return self


	def __validate__(self):
		if self.errors:
			self.ok = False
		else:
			self.ok = True

	def __repr__(self):
		return 'ApiResponse() instance'

	def json(self):
		return dict(zip(ApiResponse.__fields__, map(lambda x: getattr(self, x), ApiResponse.__fields__)))


def get_form_data(response, field_name, field_type):
	"""
	Helper function for getting and type-validating a named query parameter from HTTP request.

	:param response: ApiResponse object
	:paran field_name: The name of the query parameter
	:param field_type: data type of the field. Must be a Python builtin type, e.g., int, str, etc.
	"""
	assert isinstance(response, ApiResponse), 'response must an instance of type ApiResponse'
	
	try:
		field = request.form[field_name]
	except KeyError:
		response += exc.MissingFieldException('Could not fulfill request. Missing field: %s. All query data must be placed in the request body.'%field_name)
		field = None
	try: 
		field = field_type(field)
	except ValueError, e:
		flapp.logger.exception(e)
	finally:
		return field









# class Unit:
# 	def __init__(self, unit_string):
# 		self.unit = unit_string

# 	def verify_unit(self):
# 		if not self.unit in API_UNITS.keys() or self.unit not in API_UNITS.values():
# 			raise UnknownUnitException(self.unit)
	
# 	def get_unit_name(self):
# 		return API_UNITS[self.unit]

# 	def get_unit_description(self):
# 		pass

# 	def __repr__(self):
# 		return str(self.unit)


class ResponseDecorator(object):

	def __init__(self, handler):
		self.handler = handler


	def __call(self):
		api_response = ApiResponse()
		response = self.handler()
		return json.dumps(response.json())

def view_decorator(view_func):
	def wrapper(*args, **kwwargs):
		api_response = ApiResponse()
		view_func(*args, **kwargs)







class NodeResource(restful.Resource):
	def get(self):
		response = ApiResponse(request)

		node_id = get_form_data(response, 'node_id', int)
		node = Node.query.filter_by(id = node_id).first()
		if node:
			response += node
		else:
			response += exc.MissingNodeException(node_id)
		return response.json()
			
		
	def post(self):
		response = ApiResponse(request)
		params = flapp.check_query_parameters(Node, response)
		node = Node.create(**params)
		response += node
		return response.json()
		

class SensorResource(restful.Resource):
	
	def get(self, alias, sensor_type):
		""" 
		REST GET handler. Query database and return json dump of retrieved object(s)
		:param alias: node UUID or alias
		:param sensor_type: 
		"""

		node = Node.query.filter_by(alias = alias).first()
		sensors = Sensor.query.filter_by(node_id = node.id, type = sensor_type).all()
		
		if readings.has_key(key):
			return {'value':readings[(alias, sensor_type)]}
		else:
			return {'value': 'EMPTY'}

	def put(self, node, sensor_type):
		readings[(node, sensor_type)] = request.data
		print readings
		return 'OK'



#
# Actions: get all, get datetime range , get a geolocated range
#

class DatetimeResource():
	def get(self, object_type, start_date, end_date):
		pass


'/time/reading/star/end'
'/geo/'

meter = 10**(-5)/1.113

class GeoResource(restful.Resource):
	def get(self, object_type, longitude, latitude, radius):
		response = ApiResponse()
		model = eval(object_type.capitalize())

		longitude_cond = (model.longitude > longitude - radius) & (model.longitude < longitude + radius)
		latitude_cond = (model.latitude > latitude - radius) & (model.latitude < latitude + radius)

		results = model.query.filter(longitude_cond & latitude_cond).all()
		for result in results:
			response += result
		return response.json()

rest_api.add_resource(GeoResource, '/geo/<string:object_type>/<float:longitude>/<float:latitude>/<float:radius>')

 
class ReadingResource(restful.Resource):

	def get(self, node_id, sensor_alias):
		node, sensor = None, None
		response = ApiResponse(request)
		date_range = request.args.get('date_range', None)

		try:
			node = Node.query.filter_by(id = node_id).first()
		except DataError:
			response += exc.ApiException('node_id must be an integer')
		if not node: 
			response += exc.ApiException('Insert reading failed: No node with id %s'%node_id)

		try:
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
		except DataError:
			response += exc.ApiException('sensor_id must an integer')

		if not sensor: 
			response += exc.ApiException('Get reading failed: Node has no sensor with alias %s'%sensor_alias)
		else:
			if date_range == '1week':
				from_date = datetime.now() - timedelta(weeks = 1)
				readings = Reading.query.filter_by(sensor = sensor).filter(Reading.timestamp > from_date).all()				
				for reading in readings: 
					response += exc.ApiException({'value': reading.value})
			else:
				readings = Reading.query.filter(Reading.sensor == sensor).all()
				for reading in readings:
					response += exc.ApiException(reading)
		return response.json()
	
	def put(self, node_id, sensor_alias):
		""" 
		:param node_uuid: uuid of the node
		:param sensor_identifier: Can be either sensor uuid or sensor alias. 
		"""
		response = ApiResponse(request)

		timestamp = get_form_data(response, 'timestamp')
		value = get_form_data(response, 'value')

		put_reading_in_database(node_id, sensor_alias, value, timestamp, response)

		return response.json()

class SensorData(object):
	"""
	This is a convenience class for structuring data sent from the aggregator nodes. 
	It contains methods which act as a bridge between the API and the database.
	"""
	def __init__(self, alias = None, value = None, timestamp = None, node_id = None, **kwargs):
		self.alias = alias
		self.value = value
		self.timestamp = timestamp
		self.node_id = node_id
		if kwargs:
			flapp.logger.warning('Got unknown sensor: %s'%kwargs)

	def as_dict(self):
		return {'node_id' : self.node_id, 'sensor_alias': self.alias, 'value': self.value, 'timestamp': self.timestamp}

	def __repr__(self):
		return str(self.__dict__)

#class Filterer(object):
#	def add_condition(condition):
#		self.conditions.append(condition)
#
#	def run_query(model)
		# for q in self.conditions:
		# 	r = model.filter(q)
		# pass


def put_reading_in_database(node_id, sensor_alias, value, timestamp, api_response):
	### Would be cool to make this an instance method in SensorData
	node, sensor = None, None

	try:
		node = Node.query.filter_by(id = node_id).first()
	except DataError:
		api_response += exc.ApiException('node_id must be an integer')
	if not node: 
		api_response += exc.ApiException('Insert reading failed: No node with id %s'%node_id)

	try:
		sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
	except DataError:
		api_response += exc.ApiException('sensor_id must an integer')

	 
	if not sensor: 
		api_response += exc.ApiException('Insert reading failed: Node has no sensor with alias %s'%sensor_alias)
	else:
		try:
			Reading.create(sensor = sensor, value = value, timestamp = timestamp)
		except Exception, e:
			api_response += e



### For administration

rest_api.add_resource(NodeResource, '/node', '/sensornodes/')


rest_api.add_resource(SensorResource, '/sensor/<string:sensor_type>')

rest_api.add_resource(ReadingResource, '/reading/node_<string:node_id>/<string:sensor_alias>')

#rest_api.add_resource(ReadingResource, '/reading?node_id=1&sensor_alias=distance')
#rest_api.add_resource(ReadingResource, '/node/<string:node_id>/sensor/distance/reading/1week')

