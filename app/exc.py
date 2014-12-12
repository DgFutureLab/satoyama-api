import json

class ApiException(Exception):
	def __init__(self, message = 'Sorry, something went wrong. Please call technical support!'):
		super(ApiException, self).__init__(message)
		
	def json(self):
		return self.message
		### Do some crazy logging in here, based on the exception class?

	def __repr__(self):
		return '%s : %s'%(self.__class__, self.message)



class UnknownUnitException(ApiException):
	def __init__(self, supplied_unit = None):
			super(UnknownUnitException, self).__init__('Bad unit specified: %s'%supplied_unit)


class InvalidAttributeException(ApiException):
	def __init__(self, attribute, model = None):
		message = '"%s" has no meaning or is not allowed the context of the current request.'%attribute
		if model: 
			message += ' Valid parameters for model %s are: %s'%(model.__name__, model.settables())
		super(InvalidAttributeException, self).__init__(message)


class MissingFieldException(ApiException):
	def __init__(self, message = None):
		super(MissingFieldException, self).__init__(message)


class MissingResourceException(ApiException):
	def __init__(self, resource_type, resource_id):
		super(MissingResourceException, self).__init__('No %s with id %s'%(resource_type, resource_id))


class MissingNodeException(ApiException):
	def __init__(self, node_id):
		super(MissingNodeException, self).__init__('No such node: %s'%node_id)


class MissingSensorException(ApiException):
	def __init__(self, sensor_id):
		super(MissingSensorException, self).__init__('No such reading: %s'%sensor_id)


class MissingReadingException(ApiException):
	def __init__(self, sensor_id):
		super(MissingReadingException, self).__init__('No such reading: %s'%sensor_id)


class MissingSensorTypeException(ApiException):
	def __init__(self, sensor_id):
		super(MissingSensorTypeException, self).__init__('No such sensortype: %s'%sensor_id)


class MissingParameterException(ApiException):
	def __init__(self, parameter_name):
		super(MissingParameterException, self).__init__('Could not fulfill request because of missing parameter: %s'%parameter_name)


class InvalidParameterTypeException(ApiException):
	def __init__(self, parameter_name, partype):
		super(InvalidParameterTypeException, self).__init__('Expected %s to be of type %s.'%(parameter_name, partype))

# class InvalidParameterValueException(ApiException):
# 	def __init__(self, parameter_name, choices):
# 		super(InvalidParameterValueException, self).__init__('Parameter %s must be one of %s.'%(parameter_name, partype))
	# def __repr__(self):
	# 	return json.dumps({'error': self.message})
