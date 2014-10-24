import unittest
from app import conf, flapp
import urllib
import argparse

from threading import Thread

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--env', choices = ('test', 'dev', 'prod'), default = 'dev', help = 'Specify environment, which determines which database to use.', type = str)
	parser.add_argument('--host', default = urllib.localhost(), help = 'Specify which host to run tests against', type = str)
	parser.add_argument('--port', default = '8080', type = int)
	args = parser.parse_args()

	# root_url = 'http://%s:%s'%(args.host, args.port)

	conf.config_test_env(flapp, HOST = args.host, PORT = args.port)
	unittest.main()