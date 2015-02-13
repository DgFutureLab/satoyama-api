from satoyama.tests.dbtestbase import DBTestBase
from satoyama.models import *
from satoyama import nodetypes
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from inspect import getmembers, isfunction

class TestSiteSeeds(DBTestBase):
	def test_ricefield_site_returns_site_with_one_node(self):
		site = SiteSeeder.seed_ricefield_site()
		assert isinstance(site, Site)
		assert len(site.nodes) == 1

	def test_seed_ricefield_node_returns_one_node_with_four_sensors(self):
		node = NodeSeeder.seed_ricefield_node()
		assert isinstance(node, Node)
		assert len(node.sensors) == len(nodetypes['ricefield']['sensors'])

	def test_seed_ricefield_node_has_correct_coordinates(self):
		latitude = 1.5
		longitude = 2.5
		node = NodeSeeder.seed_ricefield_node(latitude = latitude, longitude = longitude)
		assert node.latitude == latitude
		assert node.longitude == longitude

	def test_quick_and_dirty(self):
		for seeder in [NodeSeeder, SiteSeeder]:
			for name, attr in getmembers(seeder):
				print name, attr
				if isfunction(attr) and not hasattr(attr, 'notest'):
					try:
						attr()
					except Exception:
						print 'FAILED METHOD: %s. If you do not want this method to be tested, please decorate it with the notest decorator.'%attr
						assert False