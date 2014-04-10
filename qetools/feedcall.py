#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys, copy
import logging; LOG = logging.getLogger(__name__)

from utils import comm
from utils import servicecall
    
def handleFeedCallArgs(args):
    dct = {'data':'', 'header':{}, 'url':'', 'req':'GET', 'qa':None, '__stat':0, '__err': ''}
    if not args: dct['__stat'] = -1; dct['__err'] = '"args" was None!'; return dct
    
    dct['url'] = args.url[0]
    
    if args.data: dct['data'] = args.data
    if args.user_agent: dct['header']['User-Agent'] = args.user_agent
    if args.request: dct['req'] = args.request.upper()
    if args.qa: dct['qa'] = args.qa
    
    # handle two format of headers 1) plain text 2) JSON
    for one in args.header or []:
        one = one.strip()
        if not one: continue
        if one[0] == '{':  # JSON format
            dct['header'].update(json.loads(one))
        else:  # plain text
            k, v = one.split(':'); dct['header'][k] = v.strip()

    return dct

def callRest(url='', req='GET', header={}, data='', **kwargs):
    dctRet = { '__stat':0, '__err':'', '__rlogid':'' }    
    retRest = comm.callUrl(url, data=data, headers=header, req=req)
 
    dctRet['__url'] = url; dctRet['__header'] = header
    dctRet['__stat'] = retRest['status']; dctRet['__err'] = retRest['err']
    dctRet['__rlogid'] = retRest['info'] and retRest['info'].get('rlogid','').split(',')[0] or ''
    
    try:
        retRest['ret'] and dctRet.update(json.loads(retRest['ret']))
    except Exception as ex:
        LOG.exception(ex)
        dctRet['__stat'] = -120; dctRet['__err'] = str(ex)
    return dctRet
    
def handleFeedCommandLine(lstArgs=sys.argv[1:]):
    parser = comm.retFeedCallArgParser(); args = None
    try:
        args = parser.parse_args(lstArgs)
    except Exception as ex:
        LOG.exception(ex)
        return { '__stat':-100, '__err': 'Failed to parse_args [%s]' % str(ex) }
    
    try:
        return handleFeedCallArgs(args)
    except Exception as ex:
        LOG.exception(ex)
        return { '__stat':-110, '__err': 'Failed to handle feed call args [%s]' % str(ex) }
    
if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)
            
    dctArgs = handleFeedCommandLine(); dctRet = copy.deepcopy(dctArgs)        
    if dctArgs['__stat'] == 0: dctRet = callRest(**dctArgs)
    
    if dctArgs.get('qa') and dctRet.get('__stat') == 200:
        dctRet = servicecall.chkResult4feedservice_feed(retSvc, url=retSvc['__url'], header=retSvc['__header'])

    print json.dumps(dctRet)
    
