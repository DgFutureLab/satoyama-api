import urllib
from inspect import getmembers, isfunction, ismethod
import exc
from flask import request

class ApiHelper(object):
	def __init__(self, flapp):
		self.flapp = flapp
		helpers = [member for member, typ in getmembers(self) if isfunction(typ) or (ismethod(typ) and member != '__init__')]
		for helper in helpers:
			if hasattr(self.flapp, helper):
				raise Exception('Cannot add helper "%s": The provided app already has a method with the same name'%helper)
			else:
				setattr(self.flapp, helper, getattr(self, helper))


class UrlHelper(ApiHelper):
	
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = '8080'

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

		return 'http://%s:%s/'%(host, port)


	def get_url(self, *path, **query_params):
		"""
		Constructs a url from path elements and named query parameters.
		Example: >>> flapp.get_url('readings', node_id = 2, sensor_alias = 'indoor_temperature', when = 'latest')
		"""
		try:
			path = map(str, path)
			return self.get_root_url() + '/'.join(path) + '?' + urllib.urlencode(query_params)
		except ValueError:
			raise ValueError('All path arguments must be convertible to strings')
		

class RequestHelper(ApiHelper):
	def check_query_parameters(model, response):
		query_params = {}
		settables = model.settables()
		for par, val in request.form.items():
			if par in settables:
				query_params.update({par : val})
			else:
				response.add_warning(exc.InvalidAttributeException(par))
		return query_params