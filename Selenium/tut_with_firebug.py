#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Reference:
# http://stackoverflow.com/questions/497276/how-can-i-consume-firebug-net-panel-data-programmatically

# http://selenium-python.readthedocs.org/en/latest/faq.html#how-to-use-firebug-with-firefox
# http://www.softwareishard.com/blog/firebug/automate-page-load-performance-testing-with-firebug-and-selenium/


import sys, time

from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

baseurl = "http://69.248.94.79/test/hello.html"


ff_profile = webdriver.FirefoxProfile()
ff_profile.add_extension(extension='./firefox_ext/firebug-1.12.6-fx.xpi')
ff_profile.set_preference("extensions.firebug.currentVersion", "1.12.6") #Avoid startup screen
ff_profile.set_preference("extensions.firebug.allPagesActivation", "on")
ff_profile.set_preference("extensions.firebug.defaultPanelName", "net")
ff_profile.set_preference("extensions.firebug.net.enableSites", True) # enable net panel
ff_profile.set_preference("extensions.firebug.console.enableSites", True) # enable console panel
ff_profile.set_preference("extensions.firebug.cookies.enableSites", True) # enable cookies panel

mydriver = webdriver.Firefox(firefox_profile=ff_profile)

#mydriver.maximize_window()

mydriver.get(baseurl)

time.sleep(30)

mydriver.close()
