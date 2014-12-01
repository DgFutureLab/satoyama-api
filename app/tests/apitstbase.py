import unittest
import json
from app.resources import ApiResponse
import requests
class ApiTestBase():

	GET_TIMEOUT = 2

	def get(url, **query_params):
		return requests.get(url, timeout = ApiTestBase.GET_TIMEOUT, **query_params)

	def assert_response_format(self, response):
		"""
		:param response: An instance of requests.Response
		Checks if an ApiResponse can be created
		from the text attribute of the response
		"""
		json_dict = json.loads(response.text)
		assert json_dict.has_key('errors')
		assert json_dict.has_key('objects')
		

	def assert_all_ok(self, response, expect_success = True):
		"""
		Takes a requests.Response instance and checks if the status code is OK. ALSO checks if an ApiResponse can be created
		from the text attribute of the response, and if so, whether or not the ApiResponse status is OK. 
		"""
		assert response.ok
		self.assert_response_format(response)
		api_response = self.get_api_response(response)
		if expect_success:
			self.assertTrue(api_response.ok)
		else:
			self.assertTrue(not api_response.ok)
		return api_response

	def get_api_response(self, response):
		json_dict = json.loads(response.text)
		api_response = ApiResponse(**json_dict)
		return api_response