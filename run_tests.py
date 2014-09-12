import unittest
from tests.db import *
from app import conf, flapp

if __name__ == "__main__":
	conf.config_test_env(flapp)
	unittest.main()