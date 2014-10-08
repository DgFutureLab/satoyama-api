import unittest
import app
import requests
from satoyama.models import Node, Sensor, SensorType, Reading
from app import flapp
import json
from test_helpers import ApiTester



class NodeResourceTests(unittest.TestCase, ApiTester):

	def setUp(self):
		app.database.recreate()


	def test_GET_existing_node_by_id(self):
		Node.create() # create the node that we want to get
		url = flapp.get_url('node', node_id = 1)
		r = requests.get(url, data = {'node_id' : 1})
		api_response = self.assert_all_ok(r)

	def test_GET_nonexisting_node_by_id(self):
		url = flapp.get_url('node')
		r = requests.get(url, data = {'node_id' : 100000000})
		self.assert_all_ok(r, expect_success = False)	
 
	def test_POST_node(self):
		url = flapp.get_url('node')
		r = requests.post(url, data = {'alias' : 'mynode'})
		api_response = self.assert_all_ok(r)
		
		
		# self.assertTrue(api_response.ok)
		# self.assertTrue(get_response_data(r)[0].id == 1)
		
	# 	self.assertTrue(r.ok) ### Simply assert that the server doesn't comlain about anything
	# 	print json.loads(r.text)
	# 	# self.assertTrue()

		# self.assertTrue(r.ok)

	# def test_POST_node_without_id(self):
	# 	url = flapp.get_url('node', 'new')
	# 	r = requests.post(url)
		
	# 	self.assertTrue(r.ok) ### Simply assert that the server doesn't comlain about anything
	# 	# print json.loads(r.text)

	# def test_GET_node_by_alias(self):
	# 	pass

	# def test_POST_node_by_alias(self):
	# 	pass

	# def test_database_empty_after_recreate(self):
	# 	for model in app.database.get_defined_models():
	# 		self.assertTrue(len(model.query.all()) == 0)

	# def tests_database_insert(self):
	# 	pass
		
		# model.create()
		# self.assertTrue(len(model.query.all()) == 1)		
		

# if __name__ == "__main__":
# 	models = app.database.get_defined_models()
# 	print models