#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests, sys
from BeautifulSoup import BeautifulSoup
import json, urllib

url_signin = 'https://signin.ebay.com/ws/eBayISAPI.dll'

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'})
ret = s.get(url_signin)


#print dir(s)
#print s.cookies
#print ret.text.encode('utf-8')
#print ret.text
#print type(ret.text)

soup = BeautifulSoup(ret.text)

dctData = {}
for one in soup.find('form', {'id':'SignInForm'}).findAll('input'):
	dctData[one['name']] = one['value'].replace(' ', '+')

dctData['userid'] = 'feed_auto_1'
dctData['pass'] = 'password'
dctData['ru'] = urllib.quote('http://www.ebay.com/')

data_text = ''
for k, v in dctData.iteritems():
	data_text += '%s=%s&' % (k,v)

print data_text

#print json.dumps(dctData)

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
#	'Referer': 'https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&errmsg=8&pUserId=feed_auto_1&co_partnerId=2&siteid=0&pageType=-1&pa1=&i1=-1&UsingSSL=1&k=1&favoritenav=&ru=http%3A%2F%2Fwww.ebay.com%2F&pp=&bshowgif=0&gu=0'}

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

url = 'https://signin.ebay.com/ws/eBayISAPI.dll?co_partnerId=2&siteid=0&UsingSSL=1'

#req = requests.Request('POST', url, data=json.dumps(dctData), headers=headers)
#req = requests.Request('POST', url, data=json.dumps(dctData))
req = requests.Request('POST', url, data=data_text[:-1], headers=headers)

prep_req = s.prepare_request(req)
ret = s.send(prep_req)

print ret.cookies
print ret.text.encode('utf-8')
print dir(ret.request)
print ret.request.headers
print ret.request.body
