import urllib
import urllib2
import cookielib
import argparse

REGISTER_URL='https://reg.ebay.com/reg/PartialReg'

def padErrorMessage(message):
	print("\t\033[31m******************************************************************************************************************\
			\n\tError: %s\n\t******************************************************************************************************************\033[37m" % (message))

	
def register(url, username, password, email, firstName, lastName):
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		
	try:
		register_data = urllib.urlencode({'countryId':'1', 'userid':username, 'pass':password, 'rpass': password, 'email':email, 'firstname':firstName, 'lastname':lastName, 'frmaction':'submit', 'isSug':'false', 'mode':'1', 'ru':'http://www.ebay.com'})
		handler = opener.open(url, register_data)
		body = handler.read()
	except urllib2.URLError, e:
		padErrorMessage("Error: Registering - %s" % (str(e), url))
	except urllib2.HTTPError:
		padErrorMessage("Error: Registering  - %s" % (url))
	else:
		if("Hi," in body):
			print("Successfully registered with username: '%s', password: '%s'." % (username, password))		
		else:
			print "Did not register successfully." 
		
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Register a production user')
	parser.add_argument('--user', required=True, help='Desired eBay username')    
	parser.add_argument('--password', required=True, help='Desired eBay password')
	parser.add_argument('--email', required=True, help='Desired eBay email')
	parser.add_argument('--firstName', required=True, help='First name')
	parser.add_argument('--lastName', required=True, help='Last name')

	args = parser.parse_args()
	register(REGISTER_URL, args.user, args.password, args.email, args.firstName, args.lastName)