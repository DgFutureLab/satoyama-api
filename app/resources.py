from app import rest_api, flapp
from satoyama.models import Node, Sensor, Reading

from flask.ext import restful
from flask import request
from sqlalchemy.exc import DataError
import zlib
import sys
import json

API_UNITS = {
	'm':'SI meters', 
	's':'SI seconds'
	}

def get_form_data(response, field = None):
	assert isinstance(response, ApiResponse), 'response must an instance of type ApiResponse'
	try:
		field = request.form[field]
	except KeyError:
		response.add_warning('Missing field: %s'%field)
		field = None
	finally:
		return field

class ApiResponse(object):
	
	def __init__(self, request):
		self.warnings = list()
		self.errors = list()
		self.request_data = request.form
		self.objects = list()

	def add_warning(self, warning):
		self.warnings.append(warning)

	def add_error(self, error):
		self.errors.append(error)

	def add_object(self, obj):
		self.objects.append(obj.json_detailed())
		

	def json(self):
		return {'warnings': self.warnings, 'errors': self.errors, 'request': self.request_data, 'data': self.objects}



class ApiBaseException(Exception):
	def __init__(self, message = None):
		super(ApiBaseException, self).__init__(message)
		
		def __repr__(self):
			return self.message

		### Do some crazy logging in here


class UnknownUnitException(ApiBaseException):
	def __init__(self, supplied_unit):
		super(UnknownUnitException, self).__init__('Bad unit specified: %s'%supplied_unit)


class MissingNodeException(ApiBaseException):
	def __init__(self, node_id):
		super(MissingNodeException, self).__init__('No such node: %s'%node_id)


class Unit:
	def __init__(self, unit_string):
		self.unit = unit_string

	def verify_unit(self):
		if not self.unit in API_UNITS.keys() or self.unit not in API_UNITS.values():
			raise UnknownUnitException(self.unit)
	
	def get_unit_name(self):
		return API_UNITS[self.unit]

	def get_unit_description(self):
		pass

	def __repr__(self):
		return str(self.unit)



class NodeResource(restful.Resource):
	def get(self):
		response = ApiResponse(request)
		node_id = get_form_data(response, 'id')
		try:
			node_id = int(node_id)
		except ValueError:
			response.add_error('node_id must be an integer')
		node = Node.query.filter_by(id = node_id).first()
		if node:
			response.add_object(node)
		else:
			response.add_error('no such node')
		return response.json()
			
		

	def post(self):
		response = ApiResponse(request)
		try:
			node = Node.create()
			response.add_object(node)
		except Exception, e:
			response.add_error(e)
		return response.json()
		
rest_api.add_resource(NodeResource, '/node')		

class SensorResource(restful.Resource):
	

	def get(self, alias, sensor_type):
		""" 
		REST GET handler. Query database and return json dump of retrieved object(s)
		:param alias: node UUID or alias
		:param sensor_type: 
		"""

		#OPTIONAL SENSOR UUID

		print alias, sensor_type
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





class ReadingResource(restful.Resource):

	def get(self, node_id, sensor_alias):
		response = ApiResponse(request)

		node, sensor = None, None

		try:
			node = Node.query.filter_by(id = node_id).first()
		except DataError:
			response.add_error('node_id must be an integer')
		if not node: response.add_error('Insert reading failed: No node with id %s'%node_id)

		try:
			sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
		except DataError:
			response.add_error('sensor_id must an integer')

		 
		if not sensor: 
			response.add_error('Get reading failed: Node has no sensor with alias %s'%sensor_alias)
		else:
			try:
				reading = Reading.query.filter_by(sensor = sensor).all()[-1]
				print reading.json_detailed()
				response.add_object({'value': reading.value})
			except Exception, e:
				response.add_error(e.message)
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


def put_reading_in_database(node_id, sensor_alias, value, timestamp, api_response):
	### Would be cool to make this an instance method in SensorData
	node, sensor = None, None

	try:
		node = Node.query.filter_by(id = node_id).first()
	except DataError:
		api_response.add_error('node_id must be an integer')
	if not node: 
		api_response.add_error('Insert reading failed: No node with id %s'%node_id)

	try:
		sensor = Sensor.query.filter_by(alias = sensor_alias, node = node).first()
	except DataError:
		api_response.add_error('sensor_id must an integer')

	 
	if not sensor: 
		api_response.add_error('Insert reading failed: Node has no sensor with alias %s'%sensor_alias)
	else:
		try:
			Reading.create(sensor = sensor, value = value, timestamp = timestamp)
		except Exception, e:
			api_response.add_error(e.message)


@flapp.route('/reading/batch', methods = ['POST'])
def process_multiple_readings():
	flapp.logger.info('Received %s bytes of compressed data'%sys.getsizeof(request.data))
	decompressed = zlib.decompress(request.data)
	response = ApiResponse(request)
	try:
		request_json = json.loads(decompressed)
	except Exception, e:
		print e

	# if isinstance(request_json, list):
	for reading in request_json:
		sensor_reading = SensorData(**reading)
		put_reading_in_database(api_response = response, **sensor_reading.as_dict())
	print len(Reading.query.all())
	# else: 
	# 	pass
	print response.json()
	return json.dumps(response.json())

### For administration


rest_api.add_resource(SensorResource, '/sensor/<string:sensor_type>')
# rest_api.add_resource(SensorResource, '/sensor/<int:node_id>')



### For storing/accessing sensor readings
rest_api.add_resource(ReadingResource, '/reading/node_<string:node_id>/<string:sensor_alias>')

# rest_api.add_resource(ReadingResource, '/reading/sensor/<string:sensor_id>')


