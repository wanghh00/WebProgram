#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
import logging; LOG = logging.getLogger(__name__)

import requests
from selenium import webdriver
from pyvirtualdisplay import Display

import comm

JSEvalXpath = \
'''
var tmpXpathResult = document.evaluate('%s', document, null, XPathResult.ANY_TYPE, null);
var tmpRet;
if (tmpXpathResult.resultType == 1) tmpRet = tmpXpathResult.numberValue;
else if (tmpXpathResult.resultType == 2) tmpRet = tmpXpathResult.stringValue;
else if (tmpXpathResult.resultType == 3) tmpRet = tmpXpathResult.booleanValue;
else {
    var tmpList = [];
    var tmpOne = tmpXpathResult.iterateNext();
    while (tmpOne) {
        if (tmpOne instanceof HTMLElement) tmpList.push(tmpOne.outerHTML);
        else tmpList.push(tmpOne.value);
        tmpOne = tmpXpathResult.iterateNext(); 
    }
    tmpRet = tmpList;
}
return tmpRet;
'''
def getXpathValue(driver, xpath):
    return driver.execute_script(JSEvalXpath % xpath)

def getDriverAttr(driver):
    dct = {}
    if not driver : return dct
    dct['executor_url'] = driver.command_executor._url
    dct['session_id'] = driver.session_id
    return dct

def quitDriver(dctDriver):
    url = dctDriver['executor_url'] + '/session/' + dctDriver['session_id']
    requests.delete(url)


#def genWebDriver(mode='firefox',executor='',session_id='',capabilities=None,show=False,
#        display_size=(1024, 768), **kwargs):
# mode:: 'firefox' | 'ghost' | 'remote'
# show: True | False
# executor: executor_url | executor_obj
# capabilities: selenium capabilities dictionary
def genWebDriver(**kwargs):
    kwargs['mode'] = kwargs.get('mode', 'firefox').lower(); mode = kwargs['mode']
    dctRet = {'driver': None, 'dirver_args':kwargs, 'display':None}
    display_size = kwargs.get('display_size') or (1024, 768)

    try:
        if mode in ['firefox'] and not kwargs.get('show', True):
            dctRet['display'] = Display(visible=0, size=display_size); display.start()

        if mode in ['ghost','phantomjs']:
            driver = webdriver.PhantomJS(executable_path='phantomjs', port=comm.getFreePort(), service_args=['--ignore-ssl-errors=true'])
        elif mode in ['firefox']:
            driver = webdriver.Firefox()
        elif mode in ['remote']:
            driver = webdriver.Remote(command_executor=kwargs['executor'], desired_capabilities=kwargs.get('capabilities'))

        dctRet['driver'] = driver
    except Exception as ex:
        LOG.exception(ex)

        driver and driver.quit()
        dctRet['display'] and dctRet['display'].stop()
        dctRet['driver'] = None; dctRet['display'] = None

    return dctRet

def tstKwargs(**kwargs):
    print kwargs

if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.DEBUG)

    xpath = '//div[@id="content"]//a[starts-with(@href,"http:")]'
    #xpath = 'count(//a)'
    #getXpathValue(None, xpath)
    #sys.exit(0)

    mode = 'ghost'

    #print 'Hi'
    #tstKwargs(mode='111', type='bbb')
    driver = genWebDriver(mode=mode)
    #print getDriverAttr(driver['driver'])
    driver['driver'].get('http://www.ebay.com')
    print getXpathValue(driver['driver'], xpath)


    #ret = genWebDriver(mode=mode)
    #print getDriverAttr(ret['driver'])    

    #time.sleep(10)
    sys.exit(0)
