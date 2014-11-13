import unittest
import app
import satoyama
from app import conf, flapp, socketio

from multiprocessing import Process

def run_webserver(name, env):
	conf.configure_flapp(env)
	flapp.logger.debug('Running webserver with config: %s'%flapp.config)
	socketio.run(flapp, port = flapp.config['PORT'])

# 
		# self.p.start()

	# def tearDown(self):
	# 	


class DBTestBase(unittest.TestCase):

	def setUp(self):
		app.conf.configure_flapp('test')
		satoyama.database.manager.recreate()
		# self.p = Process(target = run_webserver, args = ('WEBSERVER', 'test'))
		# self.p.start()

	def tearDown(self):
		app.flapp.db_session.remove()
		# self.p.terminate()