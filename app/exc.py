import json

class ApiBaseException(Exception):
	def __init__(self, message = 'Something went wrong. Please call customer support.'):
		super(ApiBaseException, self).__init__(message)
		
	def json(self):
		return self.message
		#

		### Do some crazy logging in here

class InternalErrorException(ApiBaseException):
	def __init__(self):
		super(InternalErrorException, self).__init__('Sorry, something went wrong. Please call technical support!')

class UnknownUnitException(ApiBaseException):
	def __init__(self, supplied_unit):
		super(UnknownUnitException, self).__init__('Bad unit specified: %s'%supplied_unit)

class InvalidAttributeException(ApiBaseException):
	def __init__(self, attribute, model = None):
		message = '"%s" has no meaning or is not allowed the context of the current request.'%attribute
		if model: 
			message += ' Valid parameters for model %s are: %s'%(model.__name__, model.settables())
		super(InvalidAttributeException, self).__init__(message)

class MissingNodeException(ApiBaseException):
	def __init__(self, node_id):
		super(MissingNodeException, self).__init__('No such node: %s'%node_id)

	# def __repr__(self):
	# 	return json.dumps({'error': self.message})
