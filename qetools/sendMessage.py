#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import sys, re
import json
import logging; LOG = logging.getLogger(__name__)

from utils import comm
from utils import twtapi

EmailFrom='NYC_QE@ebay.com'

DctUser = {
    'weiyu': '7329393611@txt.att.net',
    'honghao': '@FeedQE',
    'laura': '9082160202@vtext.com',
    'justin': '3476383545@vtext.com',
    'huiwen': 'huiwenyu@gmail.com', 
    'hu': '6468211339@tmomail.net',
    'ryan': '6467891772@txt.att.net',
    'all': 'weiyu honghao laura justin huiwen hu ryan', 
    'feed': 'weiyu honghao laura justin', 
    'mbe': 'weiyu huiwen ryan' }

def retArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', action='append')
    parser.add_argument('-d', '--dumpfile')
    parser.add_argument('-m', '--message', default='')
    return parser

def genTestSum(test):
    def gensum(ttt):
        rrr = ttt['id']
        if rrr.find('Exec') >= 0 and ttt['description']: rrr = ttt['description']
        return rrr

    ret = gensum(test)
    for one in test['subtests']:
        if one['status'].lower() == 'failed': ret += '(%s)' % genTestSum(one); break

    for one in test['posttests']:
        if one['status'].lower() == 'failed': ret += '(%s)' % genTestSum(one); break

    return ret

def parseDumpFile(filename, numMax=3):
    msg = ''; fcnt = 0; scnt = 0; num = numMax
    try:
        tcbuf = json.loads(open(filename).read())
    except Exception as ex:
        LOG.exception(ex); return None

    for test in tcbuf['testcases']:
        if test['status'].lower() == 'failed':
            fcnt+=1;
            if num: msg += '; %s' % genTestSum(test); num -= 1
        elif test['status'].lower() == 'skipped':
            scnt+=1
    return '%s|%s|%s%s%s' % (len(tcbuf['testcases']),fcnt,scnt,msg,fcnt>numMax and '...' or '')

if __name__ == "__main__":
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)

    lstEmails = set(); lstTwitter = set()
    parser = retArgParser(); args = parser.parse_args()

    #msgDump = args.dumpfile and parseDumpFile(args.dumpfile) or ''
    msgDump = ''
    if args.dumpfile:
        msgDump = parseDumpFile(args.dumpfile)
        if not msgDump: sys.exit(0)

    message = '%s %s' % (args.message, msgDump)
    
    lstUser = []
    for one in args.user or []:
        if one.find('@') != -1: lstUser.append(one); continue
        
        user_str = DctUser.get(one.lower(), '')
        if user_str.find('@') != -1: lstUser.append(user_str); continue
        
        for x in re.split('\W+', user_str):
            lstUser.append(DctUser.get(x, ''))
    
    LOG.info('Sending message[%s] to %s' % (message, lstUser))
    
    for user in lstUser:
        user = user.strip()
        if not user: continue        
        if user[0] == '@': lstTwitter.add(user[1:])
        else: lstEmails.add(user)
    
    try:
        #if lstEmails: comm.sendEmail(EmailFrom, list(lstEmails), args.message, args.message)
        #if lstEmails: comm.sendEmail(EmailFrom, list(lstEmails), message, '')
        if lstEmails: comm.sendEmail(EmailFrom, list(lstEmails), '', message)
    except Exception as ex:
        LOG.exception(ex)
        LOG.error('Failed to send email to %s' % lstEmails)
    
    for one in lstTwitter:
        try:
            oauth = twtapi.getOauth(one)
            ret = twtapi.twitterStatus_update(message[:120], oauth)
            LOG.info('Twtapi: %s', str(ret))
        except Exception as ex:
            LOG.exception(ex)
            LOG.error('Failed to send tweet for [%s]' % one)
