from app.resources import ApiResponse
from satoyama.models import *
import unittest
from datetime import datetime

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
		node_dict = {'alias': 'supernode'}
		node = Node(**node_dict)
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