from app import flapp
from app import rest_api
from satoyama.models import *
import exc
from flask.ext import restful
from flask import request
from sqlalchemy.exc import DataError
import zlib
import sys
import json
from datetime import datetime, timedelta
from satoyama.helpers import DatetimeHelper
from apiresponse import ApiResponse

# import app.helpers
# print dir(helpers)
import inspect
from apihelpers import RequestHelper

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}



class SiteResource(restful.Resource):
	def get(self, site_id):
		response = ApiResponse(request)
		site = Site.query.filter_by(id = site_id).first()
		if site:
			response += site
		else:
			response += exc.MissingResourceException(type(self), site_id)
		return response.json()



rest_api.add_resource(SiteResource, '/site/<int:site_id>')

class NodeList(restful.Resource):
	def get(self):
		# print 'asdasdasdsdJHHKJKHJHKJKJHKHJHJKKHJ'
		# print Node.query.all()

		# return ApiResponse(objects = Node.query.all()).json()

		api_response = ApiResponse()
		nodes = Node.query.all()
		for node in nodes: api_response += node
		return api_response.json()

rest_api.add_resource(NodeList, '/nodes', '/node/all')

# /node/1
# /node

# /reading/node_1/temperature?date_range=1week

class NodeResource(restful.Resource):
	"""
		This class represents end nodes in the sensor network
	"""

	def get(self, node_id = None):
		"""
			Use a HTTP GET request to /node/<int> get one node data 
			where <int> is the unique id of the node.
		"""
		response = ApiResponse(request)

		if node_id:
			node = Node.query.filter_by(id = node_id).first()
			if node:
				response += node
			else:
				response += exc.MissingNodeException(node_id)
		else: 
			response += MissingParameterException('node_id')
		return response.json()

	def post(self):
		"""
		Use a HTTP POST request to /node to create a new node inside the network
		
		Example in Python:
			>>> import requests
			>>> r = requests.post('http://localhost:8081/node',
							   data = {'alias':'mynode', 'site_id':'1', 'latitude' : '13.24234234', 'longitude': 23.222})
		"""		
		response = ApiResponse(request)
		RequestHelper.filter_valid_parameters(Node, response, request)
		node_alias = RequestHelper.get_form_data(response, 'alias', str)
		site_id = RequestHelper.get_form_data(response, 'site_id', int)
		longitude = RequestHelper.get_form_data(response, 'longitude', float)
		latitude = RequestHelper.get_form_data(response, 'latitude', float)
		
		print 'ASLDhISOADOASIDHJ'
		print site_id
		site = Site.query.filter_by(id = site_id).first()


		node = Node.create(alias = node_alias, site = site, latitude = latitude, longitude = longitude)
		response += node
		return response.json()
		
rest_api.add_resource(NodeResource, '/node/<string:node_id>', '/node')


class SensorResource(restful.Resource):
	def get(self, sensor_id):
		response = ApiResponse(request)
		sensor = Sensor.query.filter_by(id = sensor_id).first()
		if sensor:
			response += sensor
		else:
			response += exc.MissingSensorException(sensor_id)
		return response.json()

	def post(self):
		"""
		Use a HTTP POST request to /node to create a new node inside the network
		
		Example in Python:
			>>> import requests
			>>> r = requests.post('http://localhost:8081/node',
							   data = {'alias':'mynode', 'site_id':'1', 'latitude' : '13.24234234', 'longitude': 23.222})
		"""		
		response = ApiResponse(request)
		RequestHelper.filter_valid_parameters(Sensor, response, request)
		sensor_alias = RequestHelper.get_form_data(response, 'alias', str)
		sensortype_alias = RequestHelper.get_form_data(response, 'sensortype', str)
		node_id = RequestHelper.get_form_data(response, 'node_id', int)

		node = Node.query.filter_by(id = node_id).first()
		if not node:
			response += exc.MissingNodeException(node_id)

		sensortype = SensorType.query.filter_by(name = sensortype_alias).first()
		if not sensortype:
			response += exc.MissingSensorTypeException(sensortype_alias)
		
		if node and sensortype:
			sensor = Sensor.create(alias = sensor_alias, sensortype = sensortype, node = node)
			response += sensor

		return response.json()

rest_api.add_resource(SensorResource, '/sensor/<string:sensor_id>', '/sensor')



class ReadingResource(restful.Resource):

	# def __init__(self):
	# 	super(ReadingResource, self).__init__()
	# 	self.response = ApiResponse(request)

			# from_date = datetime.now() - timedelta(weeks = 1)
			# readings = Reading.query.filter_by(sensor = sensor).filter(Reading.timestamp > from_date).all()				
			# for reading in readings: 
			# 	self.response += reading



	def get(self, reading_id = None):
		
		response = ApiResponse(request)

		# RequestHelper.filter_valid_parameters(Sensor, response, request)
		
		sensor_id = RequestHelper.get_form_data(response, 'sensor_id', int)
		print 'SSSSSSSSSSSSSSSSSSSSSSSSSSSSID'
		print request.form
		node_id = RequestHelper.get_form_data(response, 'node_id', int)
		sensor_alias = RequestHelper.get_form_data(response, 'sensor_alias', str)

		from_date = RequestHelper.get_form_data(response, 'from', str)
		until_date = RequestHelper.get_form_data(response, 'until', str)
		latest = RequestHelper.get_form_data(response, 'latest', str)

		

		# RequestHelper.assert_codependent_parameters(response, node_id, sensor_alias)
		# RequestHelper.assert_codependent_parameters(response, from_date, until_date)

		# if not response.ok: return response.json()
		readings = list()
		if reading_id:
			print 'OK THIS WORKS AAAAAAAAAAAAA'
			### Retrieve reading directly by ID
			reading = Reading.query.filter_by(id = reading_id).first()
			if reading:
				readings.append(reading)
			else:
				response += exc.MissingReadingException(reading_id)
		
		elif sensor_id:
			print 'OK THIS WORKS BBBBBBBBBBBBBBBBBBBBBBBB'
			# if from_date or until_date or latest:
			# 	readings = interval_query = Reading.query_interval().interval_query.filter_by(sensor_id = sensor_id).all()
			# else:
			readings = Reading.query.filter_by(sensor_id = sensor_id).all()

			# query.filter_by(sensor_id = sensor_id).all()
			# for reading in readings: response += reading
		elif node_id and sensor_alias:
			print 'CCCCCCCCCCCCCCCCCCCCCCCCCCC'
			node = Node.query.filter_by(id = node_id).first()
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
			readings = Reading.query.filter_by(sensor_id = sensor.id).all()
			
		elif node_id and not sensor_alias:
			response += exc.MissingParameterException('sensor_alias')
		elif not node_id and sensor_alias:
			response += exc.MissingParameterException('node_id')
		

		for reading in readings: response += reading
		return response.json()



	# def get(self, node_id, sensor_alias):
	# 	node, sensor = None, None
	# 	response = ApiResponse(request)

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
			return response.json()
		
		

		

		# print from_date, until_date, date_range
		# # from_date = DatetimeHelper.convert_timestamp_to_datetime(from_date)
		# # until_date = DatetimeHelper.convert_datetime_to_timestamp(until_date)
		# print from_date, until_date

		# if date_range == '1week':
			
		# else:
		# 	readings = [Reading.query.filter(Reading.sensor == sensor).order_by(Reading.timestamp.desc()).first()]
		# for reading in readings:
		# 	response += reading
		# return response.json()
		
	
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

rest_api.add_resource(ReadingResource, '/reading/<int:reading_id>', '/reading')




class ReadingList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		readings = Reading.query.all()
		for reading in readings: api_response += reading
		return api_response.json()

rest_api.add_resource(ReadingList, '/readings', '/reading/all')



# rest_api.add_resource(ReadingResource, '/reading/node_<string:node_id>/<string:sensor_alias>')


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


### For administration

# rest_api.add_resource(NodeResource, '/node/<string:node_id>/sensor/<string:sensor_id>/')



#rest_api.add_resource(ReadingResource, '/reading?node_id=1&sensor_alias=distance')
#rest_api.add_resource(ReadingResource, '/node/<string:node_id>/sensor/distance/reading/1week')

