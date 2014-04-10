#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import copy

import comm

FEED_ITEMS_NUM = 30
FEED_FISNG_GEOINFO='EBAY-US,en-US_US,USD'

ASSERT_GOOD = 0
ASSERT_OK = 100
ASSERT_WARN = 200
ASSERT_ERROR = 400

Okay = 'Okay'
Warn = 'Warning'
Error = 'Error'

DctFeedSvcCalls = {
    # Feed
    'feedservice_feed:user_id':{'pat':'^/feedservice/feed/-?\d+$'},
    'feedservice_feed:user_name':{'pat':'^/feedservice/feed/[%7E|~][^/]+$'},
    
    'feedservice_feed_interest:user_id:interest_id':{'pat':'^/feedservice/feed/interest/-?\d+/[0-9a-f]+$'},
    'feedservice_feed_interest:user_name:interest_id':{'pat':'^/feedservice/feed/interest/%7E[^/]+/[0-9a-f]+$'},
    'feedservice_feed_interest:interest_desc': {'pat':'^/feedservice/feed/interest$'},
    
    'feedservice_feed_email:user_id': {'pat':'^/feedservice/feed/email/\d+$'},
    
    # Feed Today
    'feedservice_today': {'pat': '^/feedservice/today/\d+$'},
    
    # Feed User
    'feedservice_user:user_id':{'pat':'^/feedservice/user/\d+$'},
    'feedservice_user:user_name':{'pat':'^/feedservice/user/[%7E|~][^/]+$'},
    'feedservice_user_activity:user_id':{'pat':'^/feedservice/user/\d+/activity/\d+$'},  # ending with timestamps
    'feedservice_user_activity:user_name':{'pat':'^/feedservice/user/%7E[^/]+/activity/\d+$'},
    
    # Interest
    'feedservice_interest:user_id': {'pat': '^/feedservice/interest/\d+$'},
    'feedservice_interest_ss:user_id': {'pat': '^/feedservice/interest/ss/\d+$'},
    'feedservice_interest:user_name': {'pat': '^/feedservice/interest/[%7E|~][^/]+$'},    
    'feedservice_interest:user_id:interest_id': {'pat': '^/feedservice/interest/-?\d+/[0-9a-f]+$'},
    'feedservice_interest:user_name:interest_id': {'pat': '^/feedservice/interest/%7E[^/]+/[0-9a-f]+$'},
    
    # Reco
    'feedservice_reco:user_id': {'pat': '^/feedservice/reco/\d+$'},
    
    # Block
    'feedservice_blockeditem': {'pat': '^/feedservice/blockeditem/\d+$'},

    # Interest Service
    'feedservice_interestservice_v1_ss_interest-id': {'pat': '^/feedservice/interestservice/v1/ss/interest-id$'},
    'feedservice_interestservice_v1_interest-id': {'pat': '^/feedservice/interestservice/v1/interest-id$'},
    'feedservice_interestservice_v1_interest_activity': {'pat': '^/feedservice/interestservice/v1/interest/activity$'},
    }

def matchSvcCalls(path, dctSvcCalls=DctFeedSvcCalls):
    for k, v in dctSvcCalls.iteritems():
        m = re.match(v['pat'], path)
        if m: return k
    return None
    
def chkResult4feedservice_feed(retSvc, url='', header={}, retParseUrl=None):
    dctRet = {'status':Okay}; numError = 0; numWarning = 0
    retParseUrl = retParseUrl or comm.parseUrl(url)
    
    dctHeader = {}
    for k, v in header.iteritems(): dctHeader[k.lower()] = v
    
    num = int(retParseUrl['query'].get('num', [FEED_ITEMS_NUM])[0])
    siteId = int(dctHeader.get('x-ebay-rest-siteid', 0))
    currencyId = dctHeader.get('x-ebay-fisng-geoinfo', FEED_FISNG_GEOINFO).split(',')[2]
    
    lstItems = retSvc.get('eBay3Items') or retSvc.get('items')
    dctRet['numItems'] = len(lstItems)
    if dctRet['numItems'] == num: dctRet['chk_num'] = ASSERT_GOOD
    elif dctRet['numItems'] > 0 and dctRet['numItems'] <= num: dctRet['chk_num'] = ASSERT_OK
    else: dctRet['chk_num'] = ASSERT_ERROR
    
    def chkFeedItem(item):
        dct = {'chk_siteId': True, 'chk_currencyId': True, 'type':'item', 'chk_before_after':True}
        dct['chk_siteId'] = item['siteId'] == 0 or item['siteId'] == siteId
        return dct
    
    dctRet['chk_items'] = []
    for item in lstItems:
        #print item['itemId']
        if item['type'] == 'item': dctRet['chk_items'].append(chkFeedItem(item))
    
    if numError: dctRet['status'] = Error
    elif numWarning: dctRet['status'] = Warn
    
    return dctRet
    
if __name__ == '__main__':
    url = 'http://ebay.com/feedservice/feed/516639453?num=30&after=1382460267000&collectionsAfter=1382468435870&followsAfter=1382468135871&useEbay3=1&objectType=interest&objectType=collection&objectType=user'
    dct = chkResult4feedservice_feed({}, url, {"X-ebay-rest-siteid": "3", "x-ebay-fisng-geoinfo": "EBAY-GB,en-GB_GB,GBP"})
