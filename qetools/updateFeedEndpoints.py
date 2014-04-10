import argparse
import urllib
import urllib2
import cookielib

DEFAULT_PERSON='me'

UPDATE_PATH='/admin/v3console/UpdateConfigCategoryXml?id='

US_USER='feed_maui'
GBX_USER='feed_maui_de_gbx'
PASSWORD='password'

FEEDHOME_FR='http://lnp.fr.paradise.qa.ebay.com:8080'

COLLECTION_SERVICE_ENDPOINT='http://phx5qa01c-f191.stratus.phx.qa.ebay.com:8080/collect'
PEOPLE_META_ENDPOINT='http://www.mywrldsvc.lnp.stratus.qa.ebay.com/mywrldsvc/v1/myworld'
LPCAL_ENDPOINT='lpcal.vip.qa.ebay.com:1118'
FISNG_ENDPOINT='http://pe-a195.phx.qa.ebay.com:8080/services/search/FindItemServiceNextGen/v1'
PDS_ENDPOINT='http://pe-a201.phx.qa.ebay.com:8080/ws/spf'

URLS = {
    'feedhome_me': 'http://phx5qa01c-22b8.stratus.phx.qa.ebay.com:8080',
    'feedservice_me': 'http://phx5qa01c-81d7.stratus.phx.qa.ebay.com:8080',
    'followservice_me': 'http://phx5qa01c-b0b4.stratus.phx.qa.ebay.com:8080',
    
    'feedhome_others': 'http://phx5qa01c-22b8.stratus.phx.qa.ebay.com',
    'feedservice_others': 'http://phx5qa01c-55f6.stratus.phx.qa.ebay.com:8080',
    'followservice_others': 'http://phx5qa01c-2efd.stratus.phx.qa.ebay.com:8080',
    }
    
def update(url):
	req = urllib2.Request(url)
	try:
		handler = urllib2.urlopen(req)
		print ("\t%s: %s" % (handler.getcode(), url))    
	except urllib2.HTTPError:
		print ("\tError: %s" % (url))
	
	
def logIn(feedhome, username):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

	try:
		opener.open("http://rover.qa.ebay.com/roversync/?site=0&stg=0&mpt=1225345381126")

		login_data = urllib.urlencode({'userid':username, 'MfcISAPICommand':'SignInWelcome', 'pass':PASSWORD, 'siteid':'0', 'co_partnerId':'121', 'UsingSSL':'1', 'pageType':'559', 'i1':'-1', 'ru':'', 'pp':'', 'pa1':'', 'pa2':'', 'pa3':''})
		opener.open("http://signin.qa.ebay.com/ws/eBayISAPI.dll", login_data)
		handler = opener.open(feedhome)
		print ("\t%s: Signed In - %s" % (handler.getcode(), feedhome))    
	except urllib2.HTTPError:
		print ("\tError: %s" % (feedhome))
	

def configFeedHome(feedhome, feedservice):
	print("Setting FeedHome (%s) config beans:" % (feedhome))
	
	update("%s%scom.ebay.kernel.cal.java.CalClientConfigBean&RemoteAddress=%s" % (feedhome, UPDATE_PATH, LPCAL_ENDPOINT))
	update("%s%sorg.ebayopensource.ginger.client.feedservice.v0.staging.FeedServiceClient&ENDPOINT_URI=%s/feedservice" % (feedhome, UPDATE_PATH, feedservice))
	update("%s%sebay.feed.home.BeanConfig&feedservice-base-url=%s/feedservice" % (feedhome, UPDATE_PATH, feedservice))
	update("%s%scom.ebay.soa.client.FindItemServiceNextGen.FindItemServiceNextGenFeedConsumer.staging.Invoker&SERVICE_URL=%s" % (feedhome, UPDATE_PATH, FISNG_ENDPOINT))
	update("%s%scom.ebay.soa.client.PersonalizationDataService.RaptorClient.staging.Invoker&SERVICE_URL=%s" % (feedhome, UPDATE_PATH, PDS_ENDPOINT))
	return

def configFeedService(feedservice, followservice):
	print("Setting FeedService (%s) config beans:" % (feedservice))

	update("%s%scom.ebay.kernel.cal.java.CalClientConfigBean&RemoteAddress=%s" % (feedservice, UPDATE_PATH, LPCAL_ENDPOINT))
	update("%s%scom.ebay.soa.client.FindItemServiceNextGen.FindItemServiceNextGenFeedConsumer.staging.Invoker&SERVICE_URL=%s" % (feedservice, UPDATE_PATH, FISNG_ENDPOINT))
	update("%s%sorg.ebayopensource.ginger.client.collect.v1.staging.CollectionsInternalClient&ENDPOINT_URI=%s" % (feedservice, UPDATE_PATH, COLLECTION_SERVICE_ENDPOINT))
	update("%s%sorg.ebayopensource.ginger.client.profile.v1.staging.ProfileInternalClient&ENDPOINT_URI=%s" % (feedservice, UPDATE_PATH, PEOPLE_META_ENDPOINT))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.FollowServiceConnection_mbe&SVC_HOST=%s" % (feedservice, UPDATE_PATH, followservice[7:-5]))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.FollowServiceConnection_mbe&SVC_PORT=%s" % (feedservice, UPDATE_PATH, followservice[-4:]))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.FollowServiceSecondaryConnection_mbe&SVC_HOST=%s" % (feedservice, UPDATE_PATH, followservice[7:-5]))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.FollowServiceSecondaryConnection_mbe&SVC_PORT=%s" % (feedservice, UPDATE_PATH, followservice[-4:]))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.feed_mbe&SVC_HOST=%s" % (feedservice, UPDATE_PATH, followservice[7:-5]))
	update("%s%scom.ebay.merch.mbe.client.MBEConnection.feed_mbe&SVC_PORT=%s" % (feedservice, UPDATE_PATH, followservice[-4:]))
	return


def configFollowService(followservice):
	print("Setting FollowService (%s) config beans:" % (followservice))
	update("%s%scom.ebay.kernel.cal.java.CalClientConfigBean&RemoteAddress=%s" % (followservice, UPDATE_PATH, LPCAL_ENDPOINT))
	return
	
def configTheBeans(env=DEFAULT_PERSON):
	feedhome = URLS["feedhome_"+env]
	feedservice = URLS["feedservice_"+env]
	followservice = URLS["followservice_"+env]

	print ("Lazy loading...")
	update("%s/feedservice/feed/1210545325?useEbay3=1&objectType=user&objectType=collection&objectType=interest" % (feedservice))
	update(feedhome)
	logIn(feedhome, US_USER)
	logIn(FEEDHOME_FR, US_USER)
	
	configFeedHome(feedhome, feedservice)
	configFeedService(feedservice, followservice)
	configFollowService(followservice)
	return

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Update config beans for LnP tests')
	parser.add_argument('--me', action='store_true', help='set bean configs for me')    
	parser.add_argument('--others', action='store_true', help='set bean configs for others')
	args = parser.parse_args()

	if not(args.me or args.others):
		print ("Incorrect parameters. Check help")
	elif (args.me == args.others):
		print ("Must specify '-me' xor 'others'")
	else:
		if args.me:
			configTheBeans('me')
		if args.others:
			configTheBeans('others')