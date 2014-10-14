from core import HelperBase
from datetime import datetime 

from definitions import DATETIME_FORMATS

class DatetimeHelper(HelperBase):

	def convert_timestamp(self, timestamp):
		"""
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