# coding: utf-8
from app import flapp, socketio
from flask import render_template, request
import datetime
import json
from resources import ApiResponse
from satoyama.models import Node, Reading
import zlib 
import sys
from resources import put_reading_in_database, SensorData

@flapp.route('/', methods = ['GET'])
def index():
	# return 'OK'
	return render_template('index.html')

@flapp.route('/update_temperature', methods = ['GET', 'POST'])
def emit_temperature():
	temperature = json.loads(request.data)
	socketio.emit('new serial data', {'temperature': format_data(temperature)}, namespace = '/serial')
	return 'OK'

@socketio.on('request serial data', namespace = '/serial')
def respond_to_data_request():
	flapp.logger.debug('Got request for data')


def format_data(sensor_data):
	sensor_data = map(lambda s: dict(zip(['time', 'addr', u'reading(°C)'], s.split(','))), sensor_data)
	for reading in sensor_data: reading.update({'time': datetime.datetime.fromtimestamp(float(reading['time'])).strftime('%Y-%m-%d %H:%M:%S')})
	sensor_data = map(lambda d: ', '.join(['%s: %s'%(k,v) for k,v in d.items()]), sensor_data)
	return sensor_data


###################################################################
### BELOW ARE API ROUTES
###################################################################


@flapp.route('/hello', methods = ['GET'])
def hello():
	"""	This return info about all nodes. """
	return 'HELLO!'
	# return repr(response)


@flapp.route('/node/all', methods = ['GET'])
def get_all_nodes():
	"""	This return info about all nodes. """
	response = ApiResponse(request)
	nodes = Node.query.all()
	for node in nodes: response += node
	return json.dumps(response.json())
	# return repr(response)



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
	# print response.json()
	return json.dumps(response.json())