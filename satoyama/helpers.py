from datetime import datetime 
from definitions import DATETIME_FORMATS
from inspect import getmembers, isfunction, ismethod
import json

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
			helpers = [member for member, typ in getmembers(self) if isfunction(typ) or (ismethod(typ) and member != '__init__')]
			for helper in helpers:
				if hasattr(self.obj, helper):
					raise Exception('Cannot add helper "%s": The provided app already has a method with the same name'%helper)
				else:
					setattr(self.obj, helper, getattr(self, helper))

	

class JSONHelper(HelperBase):
	@staticmethod
	def load_string_safe(string):
		try:
			loaded = json.loads(string)
			return loaded
		except Exception:
			return ''

	@staticmethod
	def test_model_json_method(cls, json_response):
		for relation, defining_dict in cls.json_relationship_representation.items():
			assert json_response.has_key(relation)  ### Check that the json response contains the a key for each of the relations defined in the model (e.g. 'nodes' for an instance of Site)
			
			for model_instance in json_response[relation]:
				for column in defining_dict['columns']:
					assert model_instance.has_key(column)


class DatetimeHelper(HelperBase):

	@staticmethod
	def convert_timestamp_to_datetime(timestamp):
		"""
		Convert a string timestamp to a datetime instance. If timestamp is already a datetime instance, the
		method just returns the same instance.
		:param timestamp: Must be an instance of datetime, or a string with one of the allowed satoyama datetime formats.
		"""
		converted = False
		if not isinstance(timestamp, datetime):
			for format in DATETIME_FORMATS:
				try:
					timestamp = datetime.strptime(timestamp, format)
					converted = True
					break
				except Exception:
					pass
		if not converted:
			timestamp = None

		if timestamp:
			return timestamp
		else:
			# self.messages.append('Provided timestamp matched none of the allowed datetime formats. Using local server time.')
			return datetime.utcnow()

	@staticmethod
	def convert_datetime_to_timestamp(datetime_instance):
		"""
		Converts a datetime instance into a timestamp string with the highest precision format
		:param datetime_instance: instance of datetime.datetime
		"""
		timestamp_str = datetime_instance.strftime(DATETIME_FORMATS[0])
		return timestamp_str
