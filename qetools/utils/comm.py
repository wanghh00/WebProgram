#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urlparse
import urllib2
import json
import sys, subprocess
import argparse
import socket
import logging; LOG = logging.getLogger(__name__)

import smtplib
from email.mime.text import MIMEText

LOGFMT = '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d] %(message)s'
LOGDATEFMT = '%Y%m%d-%H:%M:%S'

class ArgumentParserError(Exception): pass
class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)
        
def retFeedCallArgParser(throwException=True):
    if throwException: parser = ThrowingArgumentParser()
    else: parser = argparse.ArgumentParser()
    
    parser.add_argument('-H', '--header', action='append', help='<header>')
    parser.add_argument('-A', '--user-agent', help='<agent string>')
    parser.add_argument('-X', '--request', help='<command>')
    parser.add_argument('-d', '--data', help='<data>')
    parser.add_argument('url', metavar='url', nargs='+')
    
    parser.add_argument('-Q', '--qa', help='quality assertion')
    
    return parser

def getFreePort():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    s.listen(5)
    port = s.getsockname()[1]
    s.close()
    return port

def getDriverAttr(driver):
    dct = {}
    if not driver : return dct
    dct['executor_url'] = driver.command_executor._url
    dct['session_id'] = driver.session_id

    return dct

def callUrl(url, data='', headers={}, req='GET'):
    dct = {'status':0, 'err':'', 'info':None, 'ret':None}
    
    try:
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        urlreq = urllib2.Request(url, data=data, headers=headers)
        urlreq.get_method = lambda: req
        result = opener.open(urlreq)
    except urllib2.URLError as url_err:
        result = url_err
    except Exception as ex:
        LOG.exception(ex)
        dct['status'] = -200; dct['err'] = str(ex)
        return dct
        
    if hasattr(result, 'info'): dct['info'] = result.info()  # response headers
    if hasattr(result, 'read'): dct['ret'] = result.read()   # content
    if hasattr(result, 'code'): dct['status'] = result.code  # should be 200 if success
    else: dct['status'] = -300; dct['err'] = str(result.reason)

    return dct
    
def getRestUrl(url, headers={}):
    return callUrl(url, headers=headers)

def prettyJson(dct):
    return json.dumps(dct, sort_keys=True, indent=4, separators=(',', ': '))

'''
def parseUrl(url):
    pret = urlparse.urlparse(url)
    return {'path': pret.path, 'query':urlparse.parse_qs(pret.query)}
'''
def parseUrl(url):
    pret = urlparse.urlparse(url); ret = {}
    for one in ['path', 'netloc', 'scheme', 'params','fragment']:
        ret[one] = eval('pret.%s' %  one)
    ret['query'] = urlparse.parse_qs(pret.query)
    return ret

def sendEmail(emailFrom, lstEmailTo, subject, text, hostSMTP='atom.corp.ebay.com'):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = emailFrom; msg['To'] = ', '.join(lstEmailTo)
    
    s = smtplib.SMTP(hostSMTP)
    LOG.debug('%s', msg.as_string())
    s.sendmail(emailFrom, lstEmailTo, msg.as_string()); s.quit()

def runCmd(cmd):
    dct = {}
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dct['stdout'], dct['stderr'] = proc.communicate()
    dct['stat'] = proc.returncode
    return dct
        
txtMsg = '''
2013/10/22 11:21:13
Feed_Featured_Tab_Internations, 20/1/0
Check_Featured_Tab_For_Sites-Exec-5, Failed -- IT: $.interests[*] NR 8'''
  
#txtSample = '''Check_Featured_Tab_For_Sites-Exec-5, status: Failed -- IT sites '''
    
if __name__ == '__main__':
    logging.basicConfig(format=LOGFMT,datefmt=LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)

    print getFreePort()
    sys.exit(0)
    
    url = 'http://feedsvcr-web-1.stratus.phx.ebay.com/feedservice/feed/0?num=30'
    print parseUrl(url)
    sys.exit(0)
    
    #sendEmail('hongwang@ebay.com', ['hongwang@ebay.com'], '', 'Testing... haha...')
    sendEmail('FeedQEMonitor@ebay.com', ['7329393611@txt.att.net'], '', txtMsg)
    #sendEmail('FeedQEMonitor@ebay.com', ['5516896823@txt.att.net'], '', txtMsg)
    sys.exit(0)
            
    url = 'https://cmpaas.vip.ebay.com/swdeploy/locks/details'
    LOG.info('Url [%s]', url)
    sys.exit(0)    
    
    if len(sys.argv) > 1: url = sys.argv[1]
    ret = getRestUrl(url, {'Accept':'application/json', 'Content-type': 'application/json'})
    print ret['ret']
    sys.exit(0)
        
    dct = {"x-ebay-rest-siteid": "0", "x-ebay-fisng-geoinfo": "EBAY-RU,ru-RU_RU,RUB"}
    print 'hehe...'
    ret = getRestUrl(url, headers=dct)
    dct = json.loads(ret['ret'])
    print prettyJson(dct)
