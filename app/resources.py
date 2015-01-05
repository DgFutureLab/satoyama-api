from app import flapp
from app import rest_api
from satoyama.models import *
import exc
from flask.ext import restful
from flask import request
from sqlalchemy.exc import DataError
from apiresponse import ApiResponse
from apihelpers import RequestHelper
from seeds.nodes import NodeSeeder

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}


class SiteList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		sites = Site.query.all()
		for site in sites: api_response += site
		print api_response.json()
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

	def post(self):
		response = ApiResponse()
		node_alias = RequestHelper.get_form_data(response, 'site_type', str)
		return 'OK'



rest_api.add_resource(SiteResource, '/site/<int:site_id>', '/site')

class NodeList(restful.Resource):
	def get(self):
		api_response = ApiResponse()
		nodes = Node.query.all()
		for node in nodes: api_response += node
		return api_response.json()

rest_api.add_resource(NodeList, '/nodes', '/node/all')

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

	def delete(self, node_id):
		pass
		
	def post(self):
		"""
		Use a HTTP POST request to /node to create a new node inside the network
		
		Example in Python:
			>>> import requests
			>>> r = requests.post('http://localhost:8081/node',
							   data = {'alias':'mynode', 'site_id':'1', 'latitude' : '13.24234234', 'longitude': 23.222})
		"""		
		response = ApiResponse(request)
		# RequestHelper.filter_valid_parameters(Node, response, request)
		node_alias = RequestHelper.get_form_data(response, 'alias', str)
		node_type = RequestHelper.get_form_data(response, 'node_type', str, default = 'empty')
		site_id = RequestHelper.get_form_data(response, 'site_id', int)
		longitude = RequestHelper.get_form_data(response, 'longitude', float)
		latitude = RequestHelper.get_form_data(response, 'latitude', float)
		# short_address = RequestHelper.get_form_data(response, 'short_address', int)

		site = Site.query.filter_by(id = site_id).first()
		if site:
			node = NodeSeeder.seed_node(node_type, alias = node_alias, site_id = site_id, latitude = latitude, longitude = longitude)
			response += node
		else:
			response += exc.MissingSiteException(site_id)
		return response.json()

	

		
rest_api.add_resource(NodeResource, '/node/<string:node_id>', '/node')


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
		

rest_api.add_resource(ReadingList, '/readings', '/readings/all')

class ReadingResource(restful.Resource):


	def get(self, reading_id = None):
		response = ApiResponse()
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
		pass
	# def put(self, node_id, sensor_alias):
	# 	""" 
	# 	:param node_uuid: uuid of the node
	# 	:param sensor_identifier: Can be either sensor uuid or sensor alias. 
	# 	"""
	# 	response = ApiResponse(request)

	# 	timestamp = get_form_data(response, 'timestamp')
	# 	value = get_form_data(response, 'value')

	# 	put_reading_in_database(node_id, sensor_alias, value, timestamp, response)

	# 	return response.json()

rest_api.add_resource(ReadingResource, '/reading/<int:reading_id>', '/reading')




# class ReadingList(restful.Resource):
# 	def get(self):
# 		api_response = ApiResponse()
# 		readings = Reading.query.all()
# 		for reading in readings: api_response += reading
# 		return api_response.json()

# rest_api.add_resource(ReadingList, '/readings', '/reading/all')



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


