#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#import simplejson as json
import json

filename = sys.argv[1]
linesTrans = []

#['prefix','type','name','status','duration','data']

SetHeaders = set(['accept-language', 'user-agent', 'x-ebay-rest-siteid', 'x-ebay-fisng-geoinfo', 'x-ebay-c-marketplace-id'])

def breakLineDown(one):
    lstToken = one.strip().split('\t'); numToken = len(lstToken)
	
    if numToken == 1: return None	
    dct = {'prefix':lstToken[0],'type':lstToken[1],'name':lstToken[2], 'status':None,'duration':None,'data':None}
    if numToken == 3: return dct
    if numToken == 4: dct['status'] = lstToken[3]; return dct	
    if numToken == 5: dct['data'] = lstToken[4]; return dct
    dct['duration'] = lstToken[4]; dct['data'] = lstToken[5]
    return dct

def procHeader(strHeaders):
    dct = {}
    for head in strHeaders.split('&'):
        p = head.find('=')
        if p == -1: continue        
        k, v = head[:p], head[p+1:]
        
        if k in SetHeaders: dct[k] = v
        continue
        
        if k[:7] != 'x-ebay-': continue
        if k.find('rest') != -1: dct[k] = v
        if k.find('fisng') != -1: dct[k] = v
        
    return dct

def handleTransaction(trans_lines):
    if not trans_lines: return None
	
    ret = {'headers':'', 'url':'', 'request':'', 'urltype':''}
    for idx, one in enumerate(trans_lines):
        dct = breakLineDown(one)
        if not dct: continue
		
        if idx == 0: ret['urltype'] = dct['name']
        if dct['type'] in ['URL'] and dct['name'] in ['Payload']:
            ret['url'] = dct['data']; continue
        if dct['type'] in ['URL'] and dct['name'] in ['Request']:
            ret['request'] = dct['data']; continue
        if dct['type'] in ['URL'] and dct['name'] in ['RequestHeaders']:
            ret['headers'] = procHeader(dct['data']); continue
        dct = None
	
    return ret
		
for one in open(filename):
    if one[0] == '-':
        ret = handleTransaction(linesTrans)            
        if ret and ret['urltype']:
            print '%s\t%s\t%s' % (ret['urltype'], ret['request'], json.dumps(ret['headers']))
        linesTrans=[]; continue
    linesTrans.append(one)
    
