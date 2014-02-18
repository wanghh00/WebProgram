#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time

from selenium import webdriver

driver = webdriver.Remote(
	command_executor='http://127.0.0.1:4444/wd/hub',
   	desired_capabilities={'browserName': 'firefox', 'version': 'ANY', 'javascriptEnabled': True})

driver.get('http://google.com')

time.sleep(3)

driver.close()
