# coding: utf-8
from app import flapp, socketio
from flask import render_template, request
import datetime
import json
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from forms import NodeForm
from resources import ApiResponse
from satoyama.models import Node

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

# @flapp.route('/node/all', methods = ['GET'])
# def get_all_nodes():
# 	response = ApiResponse(request)
# 	nodes = Node.query.all()
# 	return json.dumps(map(lambda n: n.json_detailed(), nodes))



'''
	Admin tool
'''

@flapp.route('/admin', methods =['GET'])
def admin_top():
	return render_template('admin/index.html')

@flapp.route('/admin/addnode', methods =['GET'])
def add_node():
	form = NodeForm(request.form)
	return render_template('admin/add_node.html', form=form)

@flapp.route('/admin/addnode/submit', methods=('GET', 'POST'))
def submit():
    form = NodeForm(request.form)

    if request.method == 'POST':
    	node = Node.create(uuid = request.form['uuid'], alias = request.form['alias'])
    	return 'A new Node has been added to the network'
    	redirect('/admin')
	return render_template('admin/add_node.html', form=form)