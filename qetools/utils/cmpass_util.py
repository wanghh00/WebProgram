#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import sys

import comm

BaseUrl = 'https://cmpaas.vip.ebay.com'

def listAllLocks(baseurl = ''):
    url = baseurl or BaseUrl; url += '/swdeploy/locks/details'
    ret = comm.getRestUrl(url)
    return json.loads(ret['ret'])

EnvSTG = 'STG'
EnvPP = 'PreProd'
ProjFeedHome = 'FeedHome'
ProjFeedService = 'FeedService'

ListEnvMon = [
    {'id': '/ENVaepuspdx2n20/feedhome-app__ENVaepuspdx2n20', 'project': ProjFeedHome, 'env': EnvSTG },
    {'id': '/ENVag5twdspkej4/feedsvcr-app__ENVag5twdspkej4', 'project': ProjFeedService, 'env': EnvSTG },
    {'id': '/ENVmapbmpm1db/feedhome-app__ENVmapbmpm1db', 'project': ProjFeedHome, 'env': EnvPP },
    {'id': '/ENV3vfaux8azz/feedsvcr-app__ENV3vfaux8azz', 'project': ProjFeedService, 'env': EnvPP }, ]

EnvIndex = {}
for num, one in enumerate(ListEnvMon):
    EnvIndex[one['id']] = num

if __name__ == '__main__':
    #for one in ListEnvMon:
    #    print one['id'], one['project']
    #print EnvIndex    
    #sys.exit(0)
    
    ret = listAllLocks()
    for one in ret['result']['result']:
        print one['path'], one['properties']['owner']
        #print one['properties']['owner']
