import json
from app.resources import ApiResponse
class ApiTester(object):
	def assert_response_format(self, response):
		"""
		:param response: An instance of requests.Response
		Checks if an ApiResponse can be created
		from the text attribute of the response
		"""
		json_dict = json.loads(response.text)
		self.assertTrue(json_dict.has_key('warnings'))
		self.assertTrue(json_dict.has_key('errors'))
		self.assertTrue(json_dict.has_key('objects'))

	def assert_all_ok(self, response):
		"""
		Takes a requests.Response instance and checks if the status code is OK. ALSO checks if an ApiResponse can be created
		from the text attribute of the response, and if so, whether or not the ApiResponse status is OK. 
		"""
		self.assertTrue(response.ok)
		self.assert_response_format(response)
		api_response = self.get_api_response(response)
		self.assertTrue(api_response.ok)
		return api_response

	def get_api_response(self, response):
		json_dict = json.loads(response.text)
		api_response = ApiResponse(**json_dict)
		return api_response

