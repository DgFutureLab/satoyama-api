import requests
from satoyama.models import *
from app import flapp
from satoyama.tests.dbtestbase import DBTestBase
from seeds.nodes import NodeSeeder
from seeds.sites import SiteSeeder
from app.apihelpers import UrlHelper, ApiResponseHelper

class SiteResourceTests(DBTestBase):

	#	###############################################################################
	#	### Tests for node REST URLs [GET, POST] /node
	#	###############################################################################


	def test_GET_existing_site_by_id(self):
	 	site = SiteSeeder.seed_empty_site()
	 	url = UrlHelper.get_url(flapp, 'site', site.id)
	 	response = requests.get(url)
	 	assert response.ok
	 	api_response = ApiResponseHelper.assert_api_response(response)
	 	assert api_response.first() == site.json()

	def test_GET_nonexisting_site_by_id(self):
	 	url = UrlHelper.get_url(flapp, 'site', 123017)
	 	response = requests.get(url)
	 	assert response.ok
	 	api_response = ApiResponseHelper.assert_api_response(response, expect_success = False)
	 	
	def test_POST_empty_site(self):
	 	url = UrlHelper.get_url(flapp, 'site')
		data = {'alias':'Kamogawa_east'}
		response = requests.post(url, data = data)
		assert response.ok
		api_response = ApiResponseHelper.assert_api_response(response)
		print api_response.objects
		assert api_response.first()['alias'] == 'Kamogawa_east'