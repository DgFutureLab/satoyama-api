import exc, json
class ApiResponse(object):
	"""
	Designed so that client_side_response = ApiResponse(**server_side_response.json())
	where server_side_response is itself an ApiResponse instance
	"""
	__fields__ = ['errors', 'objects', 'query']

	def __init__(self, request = None, query = {}, objects = [], errors = []):
		"""
		
		"""
		self.errors = list()
		self.objects = list()
		self.ok = True
		
		if request:
			if hasattr(request, 'form'):
				self.query = dict(request.form.items())
		else:
			self.query = {}	

		if self.is_json(objects):
			for obj in objects: self += obj

		if self.is_json(errors):
			self.errors = errors[:]
		
		self.__validate__()

		
	def is_json(self, obj):
		try:
			json.dumps(obj)
			return True
		except TypeError:
			return False

		
	def __iadd__(self, obj):
		if hasattr(obj, '__class__'):
			if issubclass(obj.__class__, Exception):
				self.errors.append(getattr(obj, 'message'))
			elif self.is_json(obj):
				self.objects.append(obj)
			elif hasattr(obj, 'json'):
				obj_as_json = obj.json()
				if self.is_json(obj_as_json):
					self.objects.append(obj_as_json)
				else:
					self.errors.append(exc.ApiException('object had json method, but json method did not produce json-serializable output.: %s'%obj).__str__())
			else:
				self.errors.append(exc.ApiException('object added to response could not be json serialized').__str__())
		else:
			self.errors.append(exc.ApiException('obj has no __class__ attribute'))
		self.__validate__()
		return self


	def __validate__(self):
		if self.errors:
			self.ok = False
		else:
			self.ok = True

	def first(self):
		try:
			return self.objects[0]
		except KeyError:
			return None


	def __repr__(self):
		return json.dumps(self.json())

	def json(self):
		return dict(zip(ApiResponse.__fields__, map(lambda x: getattr(self, x), ApiResponse.__fields__)))
