# coding: utf-8
from app import flapp
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

	


def format_data(sensor_data):
	sensor_data = map(lambda s: dict(zip(['time', 'addr', u'reading(°C)'], s.split(','))), sensor_data)
	for reading in sensor_data: reading.update({'time': datetime.datetime.fromtimestamp(float(reading['time'])).strftime('%Y-%m-%d %H:%M:%S')})
	sensor_data = map(lambda d: ', '.join(['%s: %s'%(k,v) for k,v in d.items()]), sensor_data)
	return sensor_data


###################################################################



@flapp.route('/reading/batch', methods = ['POST'])
def process_multiple_readings():
	flapp.logger.info('Received %s bytes of compressed data'%sys.getsizeof(request.data))
	decompressed = zlib.decompress(request.data)
	response = ApiResponse(request)
	try:
		request_json = json.loads(decompressed)
	except Exception, e:
		print e
	for reading in request_json:
		sensor_reading = SensorData(**reading)
		put_reading_in_database(api_response = response, **sensor_reading.as_dict())
	print len(Reading.query.all())
	return json.dumps(response.json())