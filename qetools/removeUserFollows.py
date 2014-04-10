#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
import time

#import simplejson as json
import json

followGetUserFollow = 'http://merbak-web-2.stratus.phx.ebay.com/merbak/v0/feed/users/%(userId)s/follows?getFollowerCounts=true'
followRemoveFollow='http://www.mbeupdater.vip.ebay.com/merchbupd/v0/feed/users/%(userId)s/follows/%(entityType)s/%(entityId)s'

lstTestUsers = ['1192171204', '1192172927', '1192174280', '1194179468', '1194179679', 
	'1194179913', '1194180086', '1194180284', '1194180443', '1194180603', '1146729584',
        '1195707069', '1195707641', '1195708097', '1195708436', '1195708696',
        '1195708926', '1195709191', '1195709347', '1195709512', '1195711338', '1190369982', '1200968852',
	'1222701072', '1222707084', '1223157267', '1223156683',
	'1201035813' ]

def getUserFollow(userid):    
    exec_url = followGetUserFollow % {'userId':userid}; lstEntity = []    
    print exec_url
    
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    req1 = urllib2.Request(exec_url)
    result = opener.open(req1)
    #print 'rlogid for reset is %s' % result.info().get('rlogid')
    result = json.loads(result.read())

    for one in result['data']['follows']:
        dct = { 'userId': userid}
        for k in ['entityType', 'entityId']: dct[k] = one[k]
        lstEntity.append(dct)
    return lstEntity

def removeFollow(dct):
    exec_url = followRemoveFollow % dct

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(exec_url); request.get_method = lambda: 'DELETE'
    ret = opener.open(request)
    return ret.read()

def removeFollow4User(userid):
    for dct in getUserFollow(userid):
        ret = removeFollow(dct)
        print 'Remove: %s\t%s' % (ret, dct)

for userid in sys.argv[1:]:
    if userid not in lstTestUsers:
		print 'UserId [%s] is not a TestUser!' % userid
		continue
    removeFollow4User(userid)
    
