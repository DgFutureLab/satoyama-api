import json

class ApiException(Exception):
	def __init__(self, message = 'Sorry, something went wrong. Please call technical support!'):
		super(ApiException, self).__init__(message)
		
	def json(self):
		return self.message
		### Do some crazy logging in here, based on the exception class?


class UnknownUnitException(ApiException):
	def __init__(self, supplied_unit = None):
			super(UnknownUnitException, self).__init__('Bad unit specified: %s'%supplied_unit)


class InvalidAttributeException(ApiException):
	def __init__(self, attribute, model = None):
		message = '"%s" has no meaning or is not allowed the context of the current request.'%attribute
		if model: 
			message += ' Valid parameters for model %s are: %s'%(model.__name__, model.settables())
		super(InvalidAttributeException, self).__init__(message)


class MissingNodeException(ApiException):
	def __init__(self, node_id):
		super(MissingNodeException, self).__init__('No such node: %s'%node_id)

	# def __repr__(self):
	# 	return json.dumps({'error': self.message})
