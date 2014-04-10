#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import logging; LOG = logging.getLogger(__name__)

from utils import comm
  
DctBaseUrl = {
    'PreProd': 'http://feedsvcr-web-1.stratus.phx.ebay.com',
    'Prod': 'http://feedsvcr.vip.phx.ebay.com',
}

Env = 'PreProd'

def handleOne(dct):
    dctRet = { }
    if not dct[1]: return dctRet
    url = DctBaseUrl[Env] + dct[1]; headers = json.loads(dct.get(2)) or {}
    ret = comm.getRestUrl(url, headers)
    
    dctRet['url']=url; dctRet['status'] = ret['status']; dctRet['headers'] = headers
    dctRet['rlogid'] = ret['info'].get('rlogid','').split(',')[0]
    return dctRet

if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT, datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)
    
    inputfile = sys.argv[1]
    
    fdInput = open(inputfile)
    for line in fdInput:
        dct = dict(enumerate(line.strip().split('\t')))
        ret = handleOne(dct)
        if not ret: continue
        print '{status}\t{rlogid}\t{url}\t{headers}'.format(**ret)
