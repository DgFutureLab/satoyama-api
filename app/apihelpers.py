import urllib
from inspect import getmembers, isfunction, ismethod
import exc
from flask import request, Flask
from satoyama.helpers import HelperBase


import unittest
import json
from app.resources import ApiResponse

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
	def assert_all_ok(response, expect_success = True):
		"""
		Takes a requests.Response instance and checks if the status code is OK. ALSO checks if an ApiResponse can be created
		from the text attribute of the response, and if so, whether or not the ApiResponse status is OK. 
		"""
		assert response.ok
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

class UrlHelper(HelperBase):
	
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = '8080'

	def __init__(self, flapp):
		super(UrlHelper, self).__init__(flapp)
		self.flapp = self.obj

	@staticmethod
	def example_static_method():
		print 'hum'

	@classmethod
	def example_class_method(UrlHelper):
		print UrlHelper.value
	
	def get_root_url(self):
		"""
		Get root URL for the app. Defaults to 'http://localhost:8080' if app has not been configured with HOST and PORT keys.
		"""
		try:
			host = self.flapp.config['HOST']
		except KeyError:
			host = self.DEFAULT_HOST
			self.flapp.logger.warning('HOST not set for flask app. Using %s instead.'%self.DEFAULT_HOST)
		try:
			port = self.flapp.config['PORT']
		except KeyError:
			port = self.DEFAULT_PORT
			self.flapp.logger.warning('PORT not set for flask app. Using %s instead.'%self.DEFAULT_PORT)

		return '%s:%s/'%(host, port)

	
	def get_url(self, *path, **query_params):
		"""
		### *** UNNECCESARRY! REPLACE WITH werkzeug.urls.Href
		******************************************************

		Constructs a url from path elements and named query parameters.
		Example: >>> flapp.get_url('readings', node_id = 2, sensor_alias = 'indoor_temperature', when = 'latest')
		"""
		try:
			path = map(str, path)
			return self.get_root_url() + '/'.join(path) + '?' + urllib.urlencode(query_params)
		except ValueError:
			raise ValueError('All path arguments must be convertible to strings')

# class GeoHelper()		

class RequestHelper(HelperBase):
	def check_query_parameters(self, model, response):
		"""
		Helper method for checking if a passed query parameter is allowed for a particular model.
		"""
		query_params = {}
		settables = model.settables()
		for par, val in request.form.items():
			if par in settables:
				query_params.update({par : val})
			else:
				response.add_warning(exc.InvalidAttributeException(par, model))
		return query_params

