import urllib
from inspect import getmembers, isfunction, ismethod
import exc
from flask import request, Flask

class HelperBase(object):
	"""
	Subclass this class to make a helper
	"""
	def __init__(self, obj = None):
		"""
		:param obj (optional): An object of any type. When the helper is instantiated, it adds all methods in the helper to
		the namespace of the object. If not specified, the helper methods are available by accessing the helper class instance directly.
		"""
		if obj:
			self.obj = obj
			if isinstance(obj, Flask):
				self.flapp = obj
			helpers = [member for member, typ in getmembers(self) if isfunction(typ) or (ismethod(typ) and member != '__init__')]
			for helper in helpers:
				if hasattr(self.obj, helper):
					raise Exception('Cannot add helper "%s": The provided app already has a method with the same name'%helper)
				else:
					setattr(self.obj, helper, getattr(self, helper))


class UrlHelper(HelperBase):
	
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

