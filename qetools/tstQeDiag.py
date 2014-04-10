#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, time

from selenium import webdriver

baseurl = "http://10.224.81.168/MyTest/TestQeDiag.html"

mydriver = webdriver.Firefox()

mydriver.get(baseurl)
mydriver.find_element_by_xpath('//button').click()

objDiag = mydriver.execute_script('return objDiag;')
print objDiag['lstJsErr']
print objDiag['lstAjaxReq']

time.sleep(3)

mydriver.close()
