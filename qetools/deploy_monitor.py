#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys, time, copy
import logging; LOG = logging.getLogger(__name__)

from utils import comm

BaseUrl = 'https://cmpaas.vip.ebay.com'

EnvSTG = 'STG'
EnvPP = 'PreProd'
ProjFeedHome = 'FeedHome'
ProjFeedService = 'FeedService'

dctLastChecking = { }

DctProjMon = {
    '/ENVaepuspdx2n20/feedhome-app__ENVaepuspdx2n20': {'project': ProjFeedHome, 'env': EnvSTG },
    '/ENVag5twdspkej4/feedsvcr-app__ENVag5twdspkej4': {'project': ProjFeedService, 'env': EnvSTG },
    '/ENVmapbmpm1db/feedhome-app__ENVmapbmpm1db': {'project': ProjFeedHome, 'env': EnvPP },
    '/ENV3vfaux8azz/feedsvcr-app__ENV3vfaux8azz': {'project': ProjFeedService, 'env': EnvPP }, 
    }

def listAllLocks(baseurl = ''):
    try:
        url = baseurl or BaseUrl; url += '/swdeploy/locks/details'
        ret = comm.getRestUrl(url)
        return json.loads(ret['ret'])
    except Exception as ex:
        return None

class DeployStatus:
    Start = 100
    Finish = 200

EmailFrom = 'DeployMon_QE_NYC@ebay.com'
EmailTo = ['hongwang@ebay.com', 'layang@ebay.com', 'wzhou@hunch.com']

def sendOutEmail(key, who, status, emailFrom=EmailFrom, emailTo=EmailTo):
    if status == DeployStatus.Start:
        subject = 'DeployMon: Deployment of [%s %s] started by [%s]' % (DctProjMon[key]['env'], DctProjMon[key]['project'], who)
        text = subject
    elif status == DeployStatus.Finish:
        subject = 'DeployMon: Deployment of [%s %s] finished' % (DctProjMon[key]['env'], DctProjMon[key]['project'])
        text = subject
    else:
        LOG.warning('Unknown Status [%s]', status); return
    comm.sendEmail(emailFrom, emailTo, subject, text, hostSMTP='atom.corp.ebay.com')
    
def monitorDeployment():
    print 'Scan...'
    ret = listAllLocks(); dctResult = { }
    if not ret or ret['status']['status'] != 'OK': return
    
    for one in ret['result']['result']:
        dctResult[one['path']] = one
        
        # Do not have project need to be monitored
        if not DctProjMon.get(one['path']): continue
        
        # projected already sent out "started" emails
        if one['path'] in dctLastChecking: continue
        dctLastChecking[one['path']] = copy.deepcopy(one);  dctLastChecking[one['path']]['systemTime'] = ret['status']['systemTime']
        sendOutEmail(one['path'], one['properties']['owner'], DeployStatus.Start)
    
    lstFinishedKey = []
    for one in dctLastChecking.iterkeys():
        if one in dctResult: continue
        try:
            sendOutEmail(one, dctLastChecking[one]['properties']['owner'], DeployStatus.Finish)
        except Exception as ex:
            LOG.exception(ex)
        #del dctLastChecking[one]
        lstFinishedKey.append(one)
    for one in lstFinishedKey: del dctLastChecking[one]

def main():
    while 1:
    #for x in xrange(3):
        monitorDeployment()
        time.sleep(10)
        

if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.DEBUG)
    
    main()
    sys.exit(0)
    #for one in ListEnvMon:
    #    print one['id'], one['project']
    #print EnvIndex    
    #sys.exit(0)
    
    ret = listAllLocks()
    for one in ret['result']['result']:
        print one['path'], one['properties']['owner']
        #print one['properties']['owner']
