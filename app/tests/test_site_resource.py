import requests
from satoyama.models import *
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from app.helpers import ApiResponseHelper

class SiteResourceTests(DBTestBase):

	#	###############################################################################
	#	### Tests for node REST URLs [GET, POST] /node
	#	###############################################################################


	def test_GET_existing_site_by_id(self):
	 	Site.create() # create the site that we want to GET
	 	url = flapp.get_url('site/1')
	 	r = requests.get(url)
	 	api_response = ApiResponseHelper.assert_all_ok(r)
	 	site_json = api_response.objects[0]
	 	for attr in Site.columns():
	 		assert site_json.has_key(attr)

	def test_GET_nonexisting_site_by_id(self):
	 	url = flapp.get_url('site/1')
	 	response = requests.get(url)
	 	api_response = ApiResponseHelper.assert_all_ok(response, expect_success = False)
	 	
