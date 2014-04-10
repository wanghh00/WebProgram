#!/usr/bin/env python
# -*- coding: utf-8  -*-

import re, copy, os
import sys, commands
import ConfigParser
import argparse
import json

from BeautifulSoup import BeautifulSoup

Env = os.getenv('ENV', 'Prod')

ListDctTagSEO = [
    {'tag':'meta', 'http-equiv':'Content-Type', 'content':[] },
    {'tag':'meta', 'name':'keywords', 'content':[] },
    {'tag':'meta', 'name':'description', 'content':[] },
    {'tag':'meta', 'property':'fb:app_id', 'content':[] },
    {'tag':'meta', 'name':'apple-itunes-app', 'content':[] },
    {'tag':'meta', 'name':'verify-v1', 'content':[] },
    {'tag':'meta', 'name':'google-site-verification', 'content':[] },
    {'tag':'meta', 'name':'y_key', 'content':[] },
    {'tag':'meta', 'name':'msvalidate.01', 'content':[] },
    {'tag':'meta', 'name':'yandex-verification', 'content':[] },
    {'tag':'link', 'rel':'canonical', 'href':[] },
    {'tag':'title', 'content':[] },]

AgentFireFox = "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0"

def retArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config', help='<config file>')
    parser.add_argument('-o', '--output', help='<output file>')
    parser.add_argument('-g', '--gbx', help='<GBX uesers eg RU>')
    parser.add_argument('url', metavar='url', nargs='*')
    
    return parser

def getHTML(url, agent=AgentFireFox, cookie='', **kwargs):
    dctRet = {'stat':0, 'stdout':'', 'stderr':''}
    cmd = 'curl -A "%s" -H "%s" "%s" 2>/dev/null' % (agent, cookie, url)
    print cmd
    dctRet['stat'], dctRet['stdout'] = commands.getstatusoutput(cmd)
    return dctRet

def retSEOTags4Url(url='', **kwargs):
    retHTML = getHTML(url, **kwargs); html_doc = retHTML['stdout']
    soup = BeautifulSoup(html_doc)
    
    lstRet = []
    for one in ListDctTagSEO:
        ret = extracTagContent(soup, one)
        ret and lstRet.append(ret)
    return lstRet
    
def extracTagContent(soup, dctTag):
    dct = { }; dctRet = copy.deepcopy(dctTag)
    
    for k, v in dctTag.iteritems():
        if k in ['name', 'rel', 'http-equiv', 'property']: dct[k] = v        
    
    nodes = soup.findAll(dctTag['tag'], dct)
    if not nodes: return None    
    
    if dctTag['tag'] in ['title']:
        for one in nodes: dctRet['content'].append(one.string)
    elif dctTag['tag'] in ['link']:
        for one in nodes: dctRet['href'].append(one.get('href'))
    else:
        for one in nodes: dctRet['content'].append(one.get('content'))
    
    return dctRet

def getUrlsFromConfig(args):    
    lstRet = []
    if not args.config: return lstRet
    
    config = ConfigParser.ConfigParser()
    config.read(args.config)
        
    for one in config.sections():
        prefix = one.split()[0].lower()
        
        if not args.gbx:        
            if prefix != 'site': continue
            url = config.get(one, 'Url.%s'%Env)
            lstRet.append({'name':one, 'url':url})
        else:
            if prefix != 'gbx': continue
            url = config.get('Site US', 'Url.%s'%Env)
            cookie = config.get(one, 'Cookie')
            lstRet.append({'name':one, 'url':url, 'cookie':cookie})
    
    return lstRet

def getUrlsFromComd(args):
    lstRet = []
    for one in args.url: lstRet.append({'name':one.replace('http://',''), 'url':one})
    return lstRet
    
def genKeyName(ret):
    key = 'tag.%s' % ret['tag']
    for one in ['name', 'property', 'http-equiv', 'rel']:
        attr = ''
        if one in ret: attr = ret[one]; break
    if attr: key += '.%s' % attr
    return key
    
args = retArgParser().parse_args()
output_config = ConfigParser.RawConfigParser()

lstTask = getUrlsFromConfig(args) or getUrlsFromComd(args)

for one in lstTask:
    output_config.add_section(one['name'])
    output_config.set(one['name'], 'url', one['url'])
    
    print '\nProcessing [%s]' % one['url']
    for idx, ret in enumerate(retSEOTags4Url(**one)):
        jsonstr = json.dumps(ret)
        output_config.set(one['name'], genKeyName(ret), jsonstr)
        print jsonstr

if args.output:
    with open(args.output, 'wb') as fd: output_config.write(fd)
        