#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, time

from selenium import webdriver

#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

#baseurl = "http://www.mywebsite.com/login.php"
baseurl = "http://69.248.94.79/test/hello.html"

#js = "window.onerror = function(msg, url, line_num) { document.write('hehe...'); return false; }"
js = "var s=window.document.createElement('script'); s.src='ttt.js'; window.document.head.appendChild(s);"

username = "admin"
password = "admin"

xpaths = { 'usernameTxtBox' : "//input[@name='username']",
           'passwordTxtBox' : "//input[@name='password']",
           'submitButton' :   "//input[@name='login']"
         }

mydriver = webdriver.Firefox()
#mydriver.maximize_window()

print mydriver.execute_script(js)

mydriver.get(baseurl)


time.sleep(3)

mydriver.close()

sys.exit(0)

#Clear Username TextBox if already allowed "Remember Me" 
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()

#Write Username in Username TextBox
mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)

#Clear Password TextBox if already allowed "Remember Me" 
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()

#Write Password in password TextBox
mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)

#Click Login button
mydriver.find_element_by_xpath(xpaths['submitButton']).click()
