import unittest
import app

class DatabaseTests(unittest.TestCase):

	def setUp(self):
		app.database.recreate()

	def test_database_empty_after_recreate(self):
		for model in app.database.get_defined_models():
			self.assertTrue(len(model.query.all()) == 0)

	def tests_database_insert(self):
		pass
		
		# model.create()
		# self.assertTrue(len(model.query.all()) == 1)		
		

if __name__ == "__main__":
	from tests import app
	models = app.database.get_defined_models()
	print models