import urllib
from inspect import getmembers, isfunction, ismethod
import exc
from flask import request, Flask
from satoyama.helpers import HelperBase


import unittest
import json
from resources import ApiResponse

class ApiResponseHelper():

	@staticmethod
	def assert_response_format(response):
		"""
		:param response: An instance of requests.Response
		Checks if an ApiResponse can be created
		from the text attribute of the response
		"""
		json_dict = json.loads(response.text)
		assert json_dict.has_key('errors')
		assert json_dict.has_key('objects')
		

	@staticmethod
	def assert_api_response(response, expect_success = True):
		"""
		Takes a requests.Response instance and checks if the status code is OK. ALSO checks if an ApiResponse can be created
		from the text attribute of the response, and if so, whether or not the ApiResponse status is OK. 
		"""
		# assert response.ok
		ApiResponseHelper.assert_response_format(response)
		api_response = ApiResponseHelper.get_api_response(response)

		if expect_success:
			assert api_response.ok
		else:
			assert not api_response.ok
		return api_response

	@staticmethod
	def get_api_response(response):
		json_dict = json.loads(response.text)
		api_response = ApiResponse(**json_dict)
		return api_response



class UrlHelper(object):
	
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = '8080'

	
	
	@staticmethod
	def get_root_url(flapp):
		"""
		Get root URL for the app. Defaults to 'http://localhost:8080' if app has not been configured with HOST and PORT keys.
		"""
		assert isinstance(flapp, Flask)
		try:
			host = flapp.config['HOST']
		except KeyError:
			host = UrlHelper.DEFAULT_HOST
			flapp.logger.warning('HOST not set for flask app. Using %s instead.'%UrlHelper.DEFAULT_HOST)
		try:
			port = flapp.config['PORT']
		except KeyError:
			port = UrlHelper.DEFAULT_PORT
			flapp.logger.warning('PORT not set for flask app. Using %s instead.'%UrlHelper.DEFAULT_PORT)

		return '%s:%s/'%(host, port)


	@staticmethod
	def get_url(flapp, *path, **query_params):
		"""
		Constructs a url from path elements and named query parameters.
		Example: >>> flapp.get_url('readings', node_id = 2, sensor_alias = 'indoor_temperature', when = 'latest')
		"""
		try:
			path = map(str, path)
			return UrlHelper.get_root_url(flapp) + '/'.join(path) + '?' + urllib.urlencode(query_params)
		except ValueError:
			raise ValueError('All path arguments must be convertible to strings')



class RequestHelper(HelperBase):
	@staticmethod
	def filter_valid_parameters(model, response, request):
		"""
		Helper method for checking if a passed query parameter is allowed for a particular model.
		"""
		assert isinstance(response, ApiResponse), 'response must an instance of type ApiResponse'
		query_params = {}
		settables = model.settables()
		for par, val in request.form.items():
			if par in settables:
				query_params.update({par : val})
			else:
				response += exc.InvalidAttributeException(par, model)
		return response

	@staticmethod
	def get_form_data(response, field_name, field_type, optional = True):
		"""
		Helper function for getting and type-validating a named query parameter from HTTP request.

		:param response: ApiResponse object
		:paran field_name: The name of the query parameter
		:param field_type: data type of the field. Must be a Python builtin type, e.g., int, str, etc.
		"""
		assert isinstance(response, ApiResponse), 'response must an instance of type ApiResponse'
		try:
			field = request.form[field_name]
			try:
				field = field_type(field)
				return field
			except ValueError:
				response += exc.InvalidParameterTypeException(field_name, field_type)
		except KeyError:
			if not optional:
				response += exc.MissingFieldException('Could not fulfill request. Missing field: %s. All query data must be placed in the request body.'%field_name)
				return None



