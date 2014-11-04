from satoyama.tests.dbtestbase import DBTestBase
from satoyama.models import *
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from seeds.sites import SiteSeeder
from inspect import getmembers, isfunction


class TestSiteSeeds(DBTestBase):
	def test_singlenode_site_returns_site_with_one_node(self):
		site = SiteSeeder.seed_ricefield_site()
		assert isinstance(site, Site)
		assert len(site.nodes) == 1

	def test_quick_and_dirty(self):
		for seeder in [NodeSeeder, SiteSeeder]:
			for name, attr in getmembers(seeder):
				if isfunction(attr):
					try:
						attr()
					except Exception:
						print 'FAILED METHOD:', attr
						raise False