from inspect import getmembers, isfunction, ismethod

class HelperBase(object):
	"""
	Subclass this class to make a helper
	"""
	def __init__(self, obj):
		"""
		:param obj: An object of any type. When the helper is instantiated, it adds all methods in the helper to
		the namespace of the object.
		"""
		self.obj = obj
		helpers = [member for member, typ in getmembers(self) if isfunction(typ) or (ismethod(typ) and member != '__init__')]
		for helper in helpers:
			if hasattr(self.obj, helper):
				raise Exception('Cannot add helper "%s": The provided app already has a method with the same name'%helper)
			else:
				setattr(self.obj, helper, getattr(self, helper))
