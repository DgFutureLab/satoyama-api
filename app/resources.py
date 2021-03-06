from app import flapp
from app import rest_api
from satoyama.models import *
from satoyama import nodetypes
import exc
from exc import *
from flask.ext import restful
from flask import request
from sqlalchemy.exc import DataError
from apiresponse import ApiResponse
from apihelpers import RequestHelper
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
import ujson

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}


class SiteList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		sites = Site.query.all()
		for site in sites: api_response += site
		# print api_response.json()
		return api_response.json()

rest_api.add_resource(SiteList, '/sites')

class SiteResource(restful.Resource):
	def get(self, site_id):
		response = ApiResponse(request)
		site = Site.query.filter_by(id = site_id).first()
		if site:
			response += site
		else:
			response += exc.MissingResourceException(type(self), site_id)
		return response.json()

	def delete(self, site_id):
		response = ApiResponse(request)
		site = Site.query.filter_by(id = site_id).first()
		if site:
			response += site
			
			succes = Site.delete(site_id)
		else:
			response += MissingSiteException(site_id)
		return response.json()

	def post(self):
		response = ApiResponse()
		site_alias = RequestHelper.get_form_data(response, 'alias', str)
		response += SiteSeeder.seed_empty_site(site_alias = site_alias)
		
		return response.json()



rest_api.add_resource(SiteResource, '/site/<int:site_id>', '/site')

class NodeList(restful.Resource):
	def get(self):
		
		api_response = ApiResponse()
		filters = {}

		site_id = RequestHelper.get_form_data(api_response, 'site_id', str)
		if site_id: filters.update({'site_id': site_id})
		nodes = Node.query.filter_by(**filters).all()
		for node in nodes: api_response += node
		return api_response.json()

rest_api.add_resource(NodeList, '/nodes', '/node/all')

class NodeResource(restful.Resource):
	"""
		This class represents end nodes in the sensor network
	"""

	def __parse_form_data(self):
		form = {}
		form.update({
			'node_alias' : RequestHelper.get_form_data(response, 'alias', str),
			'node_type' : RequestHelper.get_form_data(response, 'node_type', str, default = 'empty'),
			'site_id' : RequestHelper.get_form_data(response, 'site_id', int),
			'longitude' : RequestHelper.get_form_data(response, 'longitude', float),
			'latitude' : RequestHelper.get_form_data(response, 'latitude', float),
			'node_readings' : RequestHelper.get_form_data(response, 'node_readings', int, default = 0)
			})
		return form

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

	def delete(self, node_id):
		response = ApiResponse(request)
		node = Node.query.filter_by(id = node_id).first()
		if node:
			response += node
				
			succes = Node.delete(node_id)
		else:
			response += MissingNodeException(node_id)
		return response.json()

	def post(self):
		"""
		Use a HTTP POST request to /node to create a new node inside the network
		
		Example in Python:
			>>> import requests
			>>> r = requests.post('http://localhost:8080/node',
							   data = {'alias':'mynode', 'site_id':'1', 'latitude':'13.24234234', 'longitude':23.222, 'populate':3, 'node_type':'ricefield'})
		"""		
		response = ApiResponse(request)
		# RequestHelper.filter_valid_parameters(Node, response, request)
		node_alias = RequestHelper.get_form_data(response, 'alias', str)
		node_type = RequestHelper.get_form_data(response, 'node_type', str, default = 'empty')
		site_id = RequestHelper.get_form_data(response, 'site_id', int)
		longitude = RequestHelper.get_form_data(response, 'longitude', float)
		latitude = RequestHelper.get_form_data(response, 'latitude', float)
		populate = RequestHelper.get_form_data(response, 'populate', int, default = 0)

		site = Site.query.filter_by(id = site_id).first()
		if site:
			node = NodeSeeder.seed_node(node_type, alias = node_alias, site_id = site_id, latitude = latitude, longitude = longitude, populate = populate)
			response += node
		else:
			response += exc.MissingSiteException(site_id)
		return response.json()

	

		
rest_api.add_resource(NodeResource, '/node/<int:node_id>', '/node')


from numpy.random import choice
from random import random
class YakResource(restful.Resource):
	def get(self, yak_id):
		return {
			'yak_id' : yak_id,
			'status' : choice(['dead', 'alive', 'sleeping', 'eating', 'yakking']),
			'mood': choice(['blue', 'euphoric', 'depressed', 'pissed', 'groovy']),
			'latitude' : random()*180 - 90,
			'longitude' : random()*360 - 180
			}



rest_api.add_resource(YakResource, '/yaks/<int:yak_id>')

class SensorResource(restful.Resource):
	def get(self, sensor_id):
		
		response = ApiResponse(request) 
		sensor = Sensor.query.filter_by(id = sensor_id).first()
		if sensor:
			response += sensor
		else:
			response += exc.MissingSensorException(sensor_id)
		return response.json()


# store_reading(response, sensor_id, value, timestamp_str):


rest_api.add_resource(SensorResource, '/sensor/<int:sensor_id>')

class SensorList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		sensors = Sensor.query.all()
		for sensor in sensors: api_response += sensor
		# print api_response.json()
		return api_response.json()

rest_api.add_resource(SensorList, '/sensors')

class NodeTypeList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		api_response += nodetypes
		return api_response.json()

rest_api.add_resource(NodeTypeList, '/nodetypes')

# 	def post(self):
# 		"""
# 		Use a HTTP POST request to /node to create a new node inside the network
		
# 		Example in Python:
# 			>>> import requests
# 			>>> r = requests.post('http://localhost:8081/node',
# 							   data = {'alias':'mynode', 'site_id':'1', 'latitude' : '13.24234234', 'longitude': 23.222})
# 		"""		
# 		response = ApiResponse(request)
# 		RequestHelper.filter_valid_parameters(Sensor, response, request)
# 		sensor_alias = RequestHelper.get_form_data(response, 'alias', str)
# 		sensortype_alias = RequestHelper.get_form_data(response, 'sensortype', str)
# 		node_id = RequestHelper.get_form_data(response, 'node_id', int)

# 		node = Node.query.filter_by(id = node_id).first()
# 		if not node:
# 			response += exc.MissingNodeException(node_id)

# 		sensortype = SensorType.query.filter_by(name = sensortype_alias).first()
# 		if not sensortype:
# 			response += exc.MissingSensorTypeException(sensortype_alias)
		
# 		if node and sensortype:
# 			sensor = Sensor.create(alias = sensor_alias, sensortype = sensortype, node = node)
# 			response += sensor

# 		return response.json()

# rest_api.add_resource(SensorResource, '/sensor/<string:sensor_id>', '/sensor')


def store_reading(response, sensor_id, value, timestamp_str):
		timestamp = DatetimeHelper.convert_timestamp_to_datetime(timestamp_str)
		print timestamp
		if not sensor_id: 
			response += exc.MissingReadingParameterException('sensor_id')
		elif not value: 
			response += exc.MissingReadingParameterException('value')
		elif not timestamp: 
			response += exc.MissingReadingParameterException('timestamp')
		else:
			sensor = Sensor.query.filter_by(id = sensor_id).first()
			if sensor:
				reading = Reading.create(sensor = sensor, value = value, timestamp = timestamp)
				response += reading
			else:
				response += exc.MissingSensorException(sensor_id)


class ReadingList(restful.Resource):
	
	def get(self):
		response = ApiResponse(request)
		

		sensor_id = RequestHelper.get_form_data(response, 'sensor_id', int, http_verb = 'GET')
		node_id = RequestHelper.get_form_data(response, 'node_id', int, http_verb = 'GET')
		sensor_alias = RequestHelper.get_form_data(response, 'sensor_alias', str, http_verb = 'GET')
		from_date = RequestHelper.get_form_data(response, 'from', str, http_verb = 'GET')
		until_date = RequestHelper.get_form_data(response, 'until', str, http_verb = 'GET')

		query = Reading.query
		readings = list()

		if sensor_id:
			query = Reading.query.filter_by(sensor_id = sensor_id)
			readings = Reading.query_interval(query, from_date, until_date).all()
			for reading in readings: response += reading
			return response.json()

		elif node_id and sensor_alias:
			node = Node.query.filter_by(id = node_id).first()
			
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
			if sensor:
				query = Reading.query.filter_by(sensor_id = sensor.id)
				readings = Reading.query_interval(query, from_date, until_date).all()
				for reading in readings: response += reading
			return response.json()

		elif node_id and not sensor_alias:
			response += exc.MissingParameterException('sensor_alias')
			return response.json()
		elif not node_id and sensor_alias:
			response += exc.MissingParameterException('node_id')
			return response.json()
		
		elif from_date or until_date:
			readings = Reading.query_interval(query, from_date, until_date).all()
			for reading in readings: response += reading
			return response.json()
		else:
			response += exc.MissingParameterException('sensor_id OR node_id and sensor_alias')
			return response.json()

	def post(self):
		response = ApiResponse(request)
		format = request.form.get('format', 'json')
		data = request.form.get('data', '')
		print format
		print data

		if format == 'compact':
			data = data.split(';')
			data.remove('')
			stored_readings = 0
			for reading in data:
				try:
					node_id, sensor_id, value, timestamp_str = reading.split(',')
					# print node_id, sensor_id, value, timestamp_str
				except ValueError:
					response += Exception('Please submit readings as sensor_id,value,timestamp;')				
				try: 
					store_reading(response, sensor_id, value, timestamp_str)
					stored_readings += 1
				except Exception, e:
					response += Exception('Could not store reading')								
			return 'Stored: ' + str(stored_readings) # This short return is to avoid crashing sensor nodes by sending back long response.

		elif format == 'json':
			try:
				readings = ujson.loads(data)
				if isinstance(readings, Iterable):
					for reading in readings:
						sensor_id = reading.get('sensor_id', None)
						value = reading.get('value', None)
						timestamp_str = reading.get('timestamp', None)
						store_reading(response, sensor_id, value, timestamp_str)
				else:
					response += Exception('Please submit data as a JSON list')
			except Exception, e:
				response += Exception('Could not parse json data')
			return response.json()

rest_api.add_resource(ReadingList, '/readings', '/readings/all')

from satoyama.helpers import DatetimeHelper
class ReadingResource(restful.Resource):


	def get(self, reading_id = None):
		response = ApiResponse(request)	
		if request.args:
			# print request.args.keys()
			### Temporary hack to posting data but sending urlencoded data in a GET request
			value = request.args['value']
			sensor_id = request.args['sensor_id']
			if Sensor.query.filter_by(id = sensor_id).all():
				store_reading(response, sensor_id, value, datetime.now())
				return 'OK'
			else:
				return 'ERROR'
		else:

			if reading_id:
				reading = Reading.query.filter_by(id = reading_id).first()
				if reading: 
					response += reading
				else: 
					response += exc.MissingReadingException(reading_id)			
			else:
				response += exc.IncompleteURLException(correct_url_format = 'GET /reading/<int:reading_id>')
		return response.json()

	def post(self):
		response = ApiResponse(request)
		sensor_id = RequestHelper.get_form_data(response, 'sensor_id', int)
		value = RequestHelper.get_form_data(response, 'value', float)
		timestamp_str = RequestHelper.get_form_data(response, 'timestamp', str)
		store_reading(response, sensor_id, value, timestamp_str)
		return response.json()


rest_api.add_resource(ReadingResource, '/reading/<int:reading_id>', '/reading')





def put_reading_in_database(node_id, sensor_alias, value, timestamp, api_response):
	### Would be cool to make this an instance method in SensorData

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

	print api_response.json()



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


