#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, time
import jsonpath

from utils import comm

DctSiteLnk = {
    '0': {'preprod':'http://www(\.latest)?.ebay.com', 'prod':'http://www.ebay.com'},
    '3': {'preprod':'http://www(\.latest)?.ebay.co.uk', 'prod':'http://www.ebay.co.uk'},
    '77': {'preprod':'http://www(\.latest)?.ebay.de', 'prod':'http://www.ebay.de'},
    }

class JPFunc(object):
    @staticmethod
    def EQ(json, val):
        if not json: return 1
        return 0 if json[0] == val else 1

def _chkFeed3_eBay3Items(result, site, currency):
    ret = {'len':len(result), 'status':-1, 'asserts':[]}
    for one in result:
        if one['type'] == 'item':
            pass

class Checker(object):
    def __init__(self):
        pass

    def chkRegPat(self, pat, text):
        return True

    def chkJsonPathVal(self, json, path, val, func=JPFunc.EQ):
        return func(jsonpath.jsonpath(json, path), val)

    @staticmethod
    def assertGet(entity, jpath, dctAssert=None):
        err = 0; message = '(%s)' % jpath

        ret = jsonpath.jsonpath(entity, jpath)
        if not ret: err = 1

        if dctAssert:
            dctAssert['errnum'] += err
            dctAssert['asserts'].append('%s:%s' % (message, err==0))

        return ret and ret[0]

    @staticmethod
    def assertFunc(entity, jpath, func_name, val, dctAssert=None):
        err = 0; message = '(%s %s %s)' % (jpath, func_name, val)

        ret = jsonpath.jsonpath(entity, jpath)
        if not ret: err = 1

        if not err:
            ret = ret[0]
            if isinstance(val, basestring):
                val = val.replace('"', '\"')
                good = eval('ret %s "%s"' % (func_name, val))
            else: good = eval('ret %s %s' % (func_name, val))
            err = not good and 1 or 0

        if dctAssert:
            dctAssert['errnum'] += err
            dctAssert['asserts'].append('%s:%s' % (message, err==0))

        return ret

    @staticmethod
    def assertRex(entity, jpath, pat, mode='match', dctAssert=None):
        err = 0; message = 're.%s(%s, %s)' % (mode, pat, jpath); m = None

        ret = jsonpath.jsonpath(entity, jpath)
        if not ret: err = 1

        if not err:
            refunc = eval('re.%s' % mode); text = ret[0]
            m = refunc(pat, text)
            if not m: err = 1

        if dctAssert:
            dctAssert['errnum'] += err
            dctAssert['asserts'].append('%s:%s' % (message, err==0))

        return m

class Checker_Feed3_Json(object):
    def __init__(self, dctHeader={}, url='', env=''):
        super(Checker_Feed3_Json, self).__init__()

        self.url = url; self.env = env.lower()
        while not self.env:
            dct = comm.parseUrl(url)
            if dct['netloc'].find('feedsvcr-web-1.stratus') >= 0: self.env = 'preprod'; break
            else: self.env = 'prod'; break

        self.siteid = dctHeader.get('X-EBAY-REST-SITEID', 0); self.site = DctSiteLnk[self.siteid][self.env]
        self.currency = dctHeader.get('X-EBAY-FISNG-GEOINFO', '').split(',')[-1] or 'USD'
        self.tm_mst = int(time.mktime(time.gmtime()) - (7 * 3600)) # MST -7

        
    def assert_item(self, item):
        ret = {'asserts':[], 'errnum':0}

        itemId = Checker.assertGet(item, '$.itemId', ret)
        
        #paturl = '^%s/itm/%s$' % (self.site, itemId)
        paturl = '^%s/itm/%s$' % ('http://www.ebay.com', itemId)
        Checker.assertRex(item, '$.url', paturl, mode='match', dctAssert=ret)

        Checker.assertGet(item, '$.title', ret)
        Checker.assertGet(item, '$.interestId', ret)
        Checker.assertFunc(item, '$.endTime', '>', self.tm_mst, dctAssert=ret)
        Checker.assertFunc(item, '$.currentPrice.currencyId', '==', self.currency, dctAssert=ret)
        
        Checker.assertGet(item, '$.md5Image', ret)
        Checker.assertGet(item, '$.galleryImageUrl', ret)
        Checker.assertGet(item, '$.largeImageUrl', ret)

        ret['status'] = ret['errnum']; return ret

    def chk_eBay3Items(self, items):
        ret = { 'len':len(items), 'status':0, 'asserts':[] }
        for one in items:
            if one['type'] == 'item':
                r = self.assert_item(one)
                ret['status'] += r['status']; ret['asserts'].append(r)

        return ret

    def assert_collection(self, item):
        ret = {'asserts':[], 'errnum':0}
        
        collectionId = Checker.assertGet(item, '$.collectionId', ret)
        owner = Checker.assertGet(item, '$.owner', ret)
        Checker.assertGet(item, '$.name', ret)

        paturl = '^%s/cln/%s/\S+/%s$' % (self.site, owner, collectionId)
        Checker.assertRex(item, '$.url', paturl, mode='match', dctAssert=ret)
        Checker.assertFunc(item, '$.visibility', '==', 'PUBLIC', dctAssert=ret)

        if self.env in ['preprod']:
            Checker.assertFunc(item, '$.hidden', '==', False, dctAssert=ret)
        
        ret['status'] = ret['errnum']; return ret

    def chk_collections(self, items):
        ret = { 'len':len(items), 'status':0, 'asserts':[] }
        for one in items:
            r = self.assert_collection(one)
            ret['status'] += r['status']; ret['asserts'].append(r)

        return ret

    def assert_interest(self, item):
        ret = {'asserts':[], 'errnum':0}
        
        interestId = Checker.assertGet(item, '$.interestId', ret)
        Checker.assertGet(item, '$.ebay3Id', ret)
        Checker.assertGet(item, '$.title', ret)

        if self.env in ['preprod']:
            Checker.assertFunc(item, '$.hidden', '==', False, dctAssert=ret)
        
        ret['status'] = ret['errnum']; return ret

    def chk_interests(self, items):
        ret = { 'len':len(items), 'status':0, 'asserts':[] }
        for one in items:
            r = self.assert_interest(one)
            ret['status'] += r['status']; ret['asserts'].append(r)

        return ret

    def assert_person(self, item):
        ret = {'asserts':[], 'errnum':0}
        
        Checker.assertGet(item, '$.loginName', ret)
        Checker.assertGet(item, '$.userId', ret)

        if self.env in ['preprod']:
            Checker.assertFunc(item, '$.hidden', '==', False, dctAssert=ret)
        
        ret['status'] = ret['errnum']; return ret    

    def chk_people(self, items):
        ret = { 'len':len(items), 'status':0, 'asserts':[] }
        for one in items:
            r = self.assert_person(one)
            ret['status'] += r['status']; ret['asserts'].append(r)

        return ret

    def check(self, dctRet):
        ret = { 'status':0 }

        #ret['eBay3Items'] = self.chk_eBay3Items(dctRet['eBay3Items'])
        ret['collections'] = self.chk_collections(dctRet['collections'])
        ret['interests'] = self.chk_interests(dctRet['interests'])
        ret['people'] = self.chk_people(dctRet['people'])

        return ret

def chkFeed3(dctRet, header=None, url=None):
    ret = Checker_Feed3_Json(header, url=url).check(dctRet)
    print ret
