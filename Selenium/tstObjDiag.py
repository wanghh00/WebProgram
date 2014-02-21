#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, time

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

baseurl = "http://192.168.0.115/TestJS/TestAjax.html"

mydriver = webdriver.Firefox()
#mydriver.maximize_window()

mydriver.get(baseurl)
mydriver.find_element_by_xpath('//button').click()

objDiag = mydriver.execute_script('return objDiag;')
print objDiag['lstJsErr']
print objDiag['lstAjaxReq']

time.sleep(3)

mydriver.close()
