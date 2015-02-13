from app.resources import ApiResponse
from satoyama.models import *
import unittest
from datetime import datetime
import json
from seeds.nodes import NodeSeeder

class Badboy(object):

	def __init__(self, msg = "I'm a bad object."):
		self.message = msg

	def json(self):
		"""
		This badboy deliberately returns something that is not JSON parseable
		"""
		return datetime.now()


class TestApiResponse(unittest.TestCase):

	def setUp(self):
		self.r = ApiResponse()
		

	def test_add_objects(self):
		
		for i in range(10):
			self.r += i
		assert len(self.r.errors) == 0
		assert len(self.r.objects) == 10

	def test_add_errors(self):
		for i in range(10):
			self.r += Exception('error number %s'%i)
		assert len(self.r.errors) == 10
		assert len(self.r.objects) == 0

	def test_add_obj_with_json_method(self):
		# node_dict = {'node_type_str': 'empty', 'alias': 'supernode'}
		node = NodeSeeder.seed_node('ricefield', alias = 'mynode')
		# node = Node.create(**node_dict)
		self.r += node
		assert len(self.r.objects) == 1
		assert self.r.objects[0] == node.json()


	def test_add_obj_with_faulty_json_method(self):
		badboy = Badboy('')
		self.r += badboy
		assert len(self.r.objects) == 0 # This badboy should not be added to the objects
		assert len(self.r.errors) == 1

	def test_add_not_JSON_serializable_object(self):
		d = datetime.now()
		self.r += d
		assert len(self.r.errors) == 1
		assert len(self.r.objects) == 0

	def test_ApiResponse_ok_attribute(self):
		assert self.r.ok
		self.r += 2
		assert self.r.ok
		self.r += Exception()
		assert not self.r.ok

	def test_ApiResponse_json_method(self):
		try:
			### Empty ApiResponse
			json.dumps(self.r.json())
		except Exception:
			assert False

		try:
			### ApiResponse with object
			self.r += NodeSeeder.seed_node('ricefield')
			json.dumps(self.r.json())
		except Exception, e:
			print e
			assert False

		try:
			### ApiResponse with error
			self.r += Exception('I will destroy you')
			json.dumps(self.r.json())
		except Exception:
			assert False

	# def test_ApiResponse_get_nodes_method():
	# 	nodes = [Node.create(alias = 'node_%s'%i) for i in range(10)]
	# 	sensors = [Sensor.create(node = nodes[i], alias = 'sensor_%s'%i) for i in range(10)]
	# 	for node in nodes: self.r += node
		
	# 	assert len(self.r.get_nodes()) == 10
	# 	for node_dict in self.r.get_nodes():
	# 		assert Node.deep_validate_pars()




	# 	for sensor in sensors: self.r += sensors
	# 	assert len(self.r.get_nodes()) == 10  ### Test that sensors are not retrieved by get_nodes



