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

#before is from http://mrselenium.blogspot.com/2012/02/getting-console-errors-from-browser.html
js = "var win = selenium.browserbot.getUserWindow();\
win.errors = win.errors || [];\
win.errorsJson = win.errorsJson || \"\";\
win.originalonerror = win.originalonerror || win.onerror ||\"none\";\
win.onerror = function(errorMsg, url, lineNumber) { \
    win.errors.push({\"errorMsg\": errorMsg || \"\",\"url\": url || \"\",\"lineNumber\": lineNumber || \"\"});\
    if (JSON &&JSON.stringify) win.errorsJson = JSON.stringify(win.errors); \
    if (win.originalonerror != \"none\") win.originalonerror(errorMsg, url, lineNumber);\
};\
win.console = {\
    logs: win.console.logs || [],\
    logsJson: win.console.logsJson || \"\",\
    log: function() {\
        win.console.logs.push(arguments);\
        if (JSON && JSON.stringify) win.console.logsJson = JSON.stringify(win.console.logs);\
    },\
    warns: win.console.warns || [],\
    warnsJson: win.console.warnsJson || \"\",\
    warn: function() {\
        win.console.warns.push(arguments); \
        if (JSON && JSON.stringify) win.console.warnsJson = JSON.stringify(win.console.warns);\
    },\
    errors: win.console.errors || [],\
    errorsJson: win.console.errorsJson || \"\",\
    error: function() { \
        win.console.errors.push(arguments);\
        if (JSON && JSON.stringify) win.console.errorsJson = JSON.stringify(win.console.errors);\
    }\
};"

username = "admin"
password = "admin"

xpaths = { 'usernameTxtBox' : "//input[@name='username']",
           'passwordTxtBox' : "//input[@name='password']",
           'submitButton' :   "//input[@name='login']"
         }

mydriver = webdriver.Firefox()
#mydriver.maximize_window()

#print mydriver.execute_script(js)

mydriver.get(baseurl)

#print mydriver.execute_script(js)

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
