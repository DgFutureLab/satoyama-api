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
import inspect

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
			for obj in objects: self += obj
			# self.objects = objects[:]

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
					self.errors.append(exc.ApiException('object had json method, but json method did not produce json-serializable output.: %s'%obj).__str__())
					# print map(lambda x: {'file': x[1], 'line': x[2]}, inspect.stack())
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

	# @classmethod
	# def from_json(cls, json_dict):
	# 	instance = cls(**json_dict)
	# 	return instance

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




# class ResponseDecorator(object):

# 	def __init__(self, handler):
# 		self.handler = handler


# 	def __call__(self, *args, **kwargs):
# 		self.response = ApiResponse()
# 		self.handler()
# 		return response.json()

# # def view_decorator(view_func):
# # 	def wrapper(*args, **kwwargs):
# # 		self.response = ApiResponse()
# # 		view_func(*args, **kwargs)


# class TestResource(restful.Resource):
# 	def get(self):





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
			else:
				readings = [Reading.query.filter(Reading.sensor == sensor).order_by(Reading.timestamp.desc()).first()]
			for reading in readings:
				response += reading
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

rest_api.add_resource(ReadingResource, '/reading/node_<string:node_id>/<string:sensor_alias>')

#rest_api.add_resource(ReadingResource, '/reading?node_id=1&sensor_alias=distance')
#rest_api.add_resource(ReadingResource, '/node/<string:node_id>/sensor/distance/reading/1week')

