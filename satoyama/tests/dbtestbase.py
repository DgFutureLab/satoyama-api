import unittest
import app
import satoyama


class DBTestBase(unittest.TestCase):

	def setUp(self):
		app.conf.configure_flapp('test')
		satoyama.database.manager.recreate()

	def tearDown(self):
		app.flapp.db_session.remove()