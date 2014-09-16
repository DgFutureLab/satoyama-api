import urllib
import urlparse
from flask import Flask
from inspect import getmembers, isfunction, ismethod


### *** IS THIS USED??
flapp = Flask(__name__)
def register_helper(self, func):
	setattr(self, func.func_name, func)	
flapp.register_helper = register_helper





class BaseHelper(object):
	pass

class UrlHelper(BaseHelper):
	
	DEFAULT_HOST = 'localhost'
	DEFAULT_PORT = '8080'

	def __init__(self, flapp = None):
		self.flapp = flapp
		helpers = [member for member, typ in getmembers(self) if isfunction(typ) or (ismethod(typ) and member != '__init__')]
		for helper in helpers:
			if hasattr(self.flapp, helper):
				raise Exception('Cannot add helper "%s": The provided app already has a method with the same name'%helper)
			else:
				setattr(self.flapp, helper, getattr(self, helper))


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
			flapp.logger.warning('HOST not set for flask app. Using %s instead.'%self.DEFAULT_HOST)
		try:
			port = self.flapp.config['PORT']
		except KeyError:
			port = self.DEFAULT_PORT
			flapp.logger.warning('PORT not set for flask app. Using %s instead.'%self.DEFAULT_PORT)

		return 'http://%s:%s/'%(host, port)


	def get_url(self, *path, **query_params):
		"""
		Constructs a url from path elements and named query parameters.
		Example: >>> flapp.get_url('readings', node_id = 2, sensor_alias = 'indoor_temperature', when = 'latest')
		"""
		try:
			path = map(str, path)
			return self.get_root_url() + '/'.join(path) + '?' + urllib.urlencode(query_params)
		except ValueError, e:
			raise ValueError('All path arguments must be convertible to strings')
		

		



# # @flapp.add_helper
# # def get_url():
# # 	print 'jim'

# # flapp.get_url = get_url

# def route(self, rule, **options):
#         """A decorator that is used to register a view function for a
#         given URL rule.  This does the same thing as :meth:`add_url_rule`
#         but is intended for decorator usage::

#             @app.route('/')
#             def index():
#                 return 'Hello World'

#         For more information refer to :ref:`url-route-registrations`.

#         :param rule: the URL rule as string
#         :param endpoint: the endpoint for the registered URL rule.  Flask
#                          itself assumes the name of the view function as
#                          endpoint
#         :param options: the options to be forwarded to the underlying
#                         :class:`~werkzeug.routing.Rule` object.  A change
#                         to Werkzeug is handling of method options.  methods
#                         is a list of methods this rule should be limited
#                         to (`GET`, `POST` etc.).  By default a rule
#                         just listens for `GET` (and implicitly `HEAD`).
#                         Starting with Flask 0.6, `OPTIONS` is implicitly
#                         added and handled by the standard request handling.
#         """
#         def decorator(f):
#             endpoint = options.pop('endpoint', None)
#             self.add_url_rule(rule, endpoint, f, **options)
#             return f
#         return decorator