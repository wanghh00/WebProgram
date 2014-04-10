#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json, copy, urllib
import sys, subprocess
import argparse
import logging; LOG = logging.getLogger(__name__)

#from ..utils import comm
from utils import comm

DctCountryName = {
    'US': u'United States',
    'CA': u'Canada',
    'GB': u'United Kingdom',
    'RU': u'Russian Federation',
    'MX': u'Mexico',
    'DE': u'Germany',
}


class GvfChecker(object):
    def __init__(self, env='Prod', filters=["LEGAL","BUSINESS_POLICY","SHIPPING_POLICY"], 
            contextType='TARGET_COUNTRY', app='collections'):
        if env.lower() in ['prod', 'preprod']:
            self.endurl = 'http://www.gvf.stratus.ebay.com'
        else: self.endurl = 'http://www.gvf.stg.stratus.qa.ebay.com'
        self.endurl += '/gvf/visibility/v1/items/simple'
        self.app = app; self.filter = filters; self.contextType = contextType
    
    def _get(self, lstItems):
        dct = { 'status':0 }
        args = {'ids': lstItems, 'filter': self.filter, 'contextType': self.contextType}
        params={'request': json.dumps(args), 'app': self.app}

        try: 
            r = requests.get(self.endurl, params={'request': json.dumps(args), 'app': self.app}, allow_redirects=False)
            dct['status'] = r.status_code; dct['rlogid'] = r.headers.get('rlogid')

            if r.status_code == requests.codes.ok: dct['ret'] = r.json()
            
        except Exception as ex:
            dct['status'] = -1; dct['err'] = str(ex)
        
        return dct

    def checkItemShow(self, lstItems, countryId):
        dctGVF = self._get(lstItems)
        dctRet = {'status': dctGVF['status'], 'ret': [] }

        retGVF = dctGVF.get('ret')
        if not retGVF: return dctRet

        
        #for one in gvfRet.items:
        for one in retGVF.get('items'):
            dct = { }; dct['status'] = one['status']
            if dct['status'] != 'SUCCESS': dct['errorMessage'] = one['errorMessage']
            dct['id'] = one['id']
            dct['visible'] = countryId in one.get('visible', [])
            dctRet['ret'].append(dct)

        return dctRet

            
def validShipCountries(itemid, lstCountries):
    dctRet = { 'stat': 0 }; dct = {}
    dctChk = dict(zip(lstCountries, map(lambda x: DctCountryName.get(x), lstCountries)))
    txtShip = u''

    url = 'http://www.ebay.com/itm/{id}'

    r = requests.get(url.format(id=itemid))

    p_s = r.text.find('<div class="sh-sLoc">')
    if p_s == -1: dctRet['stat'] = -100; return dctRet

    p_e = r.text.find('</div>', p_s)
    if p_e == -1: dctRet['stat'] = -100; return dctRet

    txtShip += r.text[p_s+21:p_e]

    p_s = r.text.find('<div class="sh-sLoc">', p_e)
    while p_s != -1:
        p_e = r.text.find('</div>', p_s)
        if p_e != -1: txtShip += r.text[p_s+21:p_e]
        break

    for k, v in dctChk.iteritems():
        if not v: continue
        dct[k] = True
        if txtShip.find(v) != -1: dct[k] = False

    dctRet['ret'] = dct
    return dctRet

    
if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)
    
    #print validShipCountries(131152890450, ['RU', 'CA'])
    #print validShipCountries(271343866488, ['DE'])

    chk = GvfChecker()
    #chk._get([271343866488, 1])
    ret = chk.checkItemShow([271440447287,271440431066,291114931292,360894470261,390810080104,301140615756,390809208916,221406077826], 'RU')
    print json.dumps(ret)
    