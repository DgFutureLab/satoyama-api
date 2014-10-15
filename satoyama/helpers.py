from core import HelperBase
from datetime import datetime 

from definitions import DATETIME_FORMATS

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
		return datetime_instance.strftime(DATETIME_FORMATS[0])