#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
import re
import logging; LOG = logging.getLogger(__name__)

from utils import comm
from utils import servicecall

MAX_SAMPLE_URLS = 3

def main(filename=''):
    filename = filename or sys.argv[1]    
    dctStat = { }
    
    fd = open(filename)
    for line in fd:
        lstLineToken = line.split('\t')
        
        idx = lstLineToken[0].rfind('.')
        if idx == -1: method = lstLineToken[0]
        else: method = lstLineToken[0][idx+1:]
        
        url = lstLineToken[1]; url = url.replace('/feedsvcr','/feedservice')
        
        ret = comm.parseUrl('http://ebay.com' + url)
        #print ret['query'].keys(), url
        
        callname = servicecall.matchSvcCalls(ret['path'])
        if not callname and ret['path']:
            LOG.info('Could not find CallName for [%s]', url)
            continue
        if not callname: continue
        
        if callname not in dctStat: dctStat[callname] = {}
                
        parameters = json.dumps([method]+sorted(ret['query'].iterkeys()))
        if parameters not in dctStat[callname]: dctStat[callname][parameters] = {'num':0, 'sample_urls':[] }
        
        dctStat[callname][parameters]['num'] += 1
        if len(dctStat[callname][parameters]['sample_urls']) < MAX_SAMPLE_URLS:
            if url not in dctStat[callname][parameters]['sample_urls']:
                dctStat[callname][parameters]['sample_urls'].append(url)
    
    fd.close()
    for k, v in dctStat.iteritems():
        print '\n%s' % k
        for k1, v1 in v.iteritems():
            print '%s%s:%s %s' % ('    ', k1, v1['num'], v1['sample_urls'])
    
if __name__ == '__main__':

    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)
    
    main()
    sys.exit(0)
    
    url = 'http://feedsvcr-web-1.stratus.phx.ebay.com/feedservice/feed/0?num=30'
    ret = comm.parseUrl(url)
    
    print matchSvcCalls(ret['path'])
