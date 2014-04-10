#!/usr/bin/env python
# -*- coding: utf-8  -*-

import argparse
import json, re, sys, time
import signal
import HTMLParser, string
import multiprocessing
import logging; LOG = logging.getLogger(__name__)

import requests
from pyvirtualdisplay import Display
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import UnicodeDammit
from lxml import etree
from lxml.html.soupparser import fromstring

from utils import comm

DefaultAgent = "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

def clearHtml4Lxml(html):
    soup = BeautifulSoup(html)
    parser = HTMLParser.HTMLParser()
    lstLine = []

    for idx, line in enumerate(soup.prettify().split()):
        try:
            line = filter(lambda x: x in string.printable, line)
            line = parser.unescape(line)
            line = filter(lambda x: x in string.printable, line)
        except Exception as ex:
            line = re.sub('&#\d+;', '', line)
        lstLine.append(line)
        
    return '\n'.join(lstLine)

def decode_html(html_string):
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError("Failed to detect encoding, tried [%s]", ', '.join(converted.triedEncodings))
    # print converted.originalEncoding
    return converted.unicode

def retHTMLbyCurl(url):
    cmd = 'curl -H "%s" "%s"' % (DefaultAgent, url)
    return comm.runCmd(cmd)

'''
def retHTMLbyWebDriverWithTimeout(url, timeout=60):
    dctCmd = {'stat':0, 'stdout':'', 'stderr':''}    
    pool = multiprocessing.Pool(processes=1)
    try:        
        result = pool.apply_async(retHTMLbyWebDriver, (url,))
        pool.close()
        dctCmd = result.get(timeout=timeout)
    except Exception as ex:
        LOG.exception(ex); dctCmd['stat'] = -1; dctCmd['setderr'] = str(ex)
        pool.terminate()

    pool.join()
    return dctCmd


def retHTMLbyWebDriverWithTimeout(url, timeout=60):
    import os, signal
    dctCmd = {'stat':0, 'stdout':'', 'stderr':''}
    q = multiprocessing.Queue()

    p = multiprocessing.Process(target=retHTMLbyWebDriver, args=(url,), kwargs={'queRet':q})
    p.start()
    print p.pid
    
    try: 
        dctCmd = q.get(True, timeout)
        p.join(1)
    except:
        dctCmd['stat'] = -100; dctCmd['stderr'] = 'Error: Timeout'

    if p.is_alive(): os.kill(p.pid, signal.SIGINT)

    p.join()
    return dctCmd
'''

def alarm_handler(signum, frame):
    #print 'Signal handler called with signal', signum, frame
    raise RuntimeError('TimeOut')

def retHTMLbyWebDriverWithTimeout(url, timeout=60):
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(int(timeout))
    dctCmd = retHTMLbyWebDriver(url)
    signal.alarm(0)

    return dctCmd

def quitDriver(dctDriver):
    url = dctDriver['executor_url'] + '/session/' + dctDriver['session_id']
    requests.delete(url)

def retHTMLbyWebDriver(url, queRet=None):
    dctCmd = {'stat':0, 'stdout':'', 'stderr':''}
    
    try:
        display = Display(visible=0, size=(1024, 768)); display.start()

        driver = webdriver.Firefox(); dctDriver = comm.getDriverAttr(driver)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(10)

        driver.get(url)
    except Exception as ex:
        LOG.exception(ex); dctCmd['stderr'] += '%s\n\n' % str(ex)

    try:
        dctCmd['stdout'] = driver.execute_script('return document.documentElement.outerHTML')
    except Exception as ex:
        LOG.exception(ex); dctCmd['stat'] = -1; dctCmd['stderr'] += '%s\n\n' % str(ex)
    finally:
        quitDriver(dctDriver); #driver.quit(); 
        display.stop()
    
    if queRet: queRet.put(dctCmd)
    return dctCmd

def retArgParser():
    parser = argparse.ArgumentParser()    
    parser.add_argument('-H', '--header', action='append', help='<header>')
    parser.add_argument('-x', '--xpath', action='append', help='<xpath>')
    parser.add_argument('-l', '--listxpath', action='append', help='<xpath>')
    parser.add_argument('-m', '--mode', default='curl', help='<mode>')
    parser.add_argument('-z', '--timeout', type=float, help='<timeout>')
    parser.add_argument('url', metavar='url', nargs='+')
    return parser

def main():
    parser = retArgParser(); ret = {'__stat':0, '__err':'', 'okay': True }
    try:
        args = parser.parse_args()
    except Exception as ex:
        LOG.exception(ex)
        ret['__stat'] = -100; ret['__err'] = 'Failed to parse_args [%s]' % str(ex)
            
    if args.mode.lower() == 'curl':
        dctCmd = retHTMLbyCurl(args.url[0])
    elif args.mode.lower() == 'webdriver':
        if args.timeout: dctCmd = retHTMLbyWebDriverWithTimeout(args.url[0], timeout=args.timeout)
        else: dctCmd = retHTMLbyWebDriver(args.url[0])
    else:
        dctCmd = {'stat':-100, 'stderr':'Unknown mode: %s'%args.mode, 'stdout':''}

    if dctCmd['stat'] == 0: ret['__stat'] = 200
    else:
        ret['__stat'] = dctCmd['stat']; ret['__err'] = dctCmd['stderr']

    while (ret['__stat'] == 200):
        try:
            tree = fromstring(dctCmd['stdout'])
        except Exception as ex:
            tree = None; LOG.exception(ex)
        if tree is None:
            tree = fromstring(clearHtml4Lxml(dctCmd['stdout']))

        stResult = set()
        for xpath in args.listxpath or []:
            for one in tree.xpath(xpath): stResult.add(one)    
        ret['__listxpath'] = list(stResult)

        for xpath in args.xpath or []:
            r = tree.xpath(xpath)
            if not r: ret['okay'] = False; break
        break
    
    if ret['__stat'] != 200 or ret['__err']: ret['okay'] = False
    return ret

if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)

    ret = main()
    print json.dumps(ret)
