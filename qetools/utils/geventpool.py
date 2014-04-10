#!/usr/bin/env python
# -*- coding: utf-8  -*-

import sys
import requests

import gevent
from gevent import monkey, Timeout
monkey.patch_all(thread=False, select=False)

from gevent.pool import Pool as GeventPool

POOL_SIZE=40

class GetUrlByRequests(object):
    def __init__(self, use_head=False, headers=None, params=None, timeout=30):
        self.use_head = use_head; self.headers = headers; self.params = params
        self.allow_redirects = True; self.timeout = timeout
        #{'headers', 'text', 'encoding', 'content', 'url', 'history'}
    def __call__(self, url):
        dct = {'url':url }
        try:
            if self.use_head: func = requests.head
            else: func = requests.get

            r = func(url, allow_redirects=self.allow_redirects, headers=self.headers, params=self.params, timeout=self.timeout)
            dct['status'] = r.status_code
            #if not self.use_head: dct['text'] = r.text
        except Exception as ex:
            dct['status'] = -1; dct['error'] = str(ex)
        return dct

def getUrlsByRequests(lstUrl, use_head=False, pool_size=POOL_SIZE):
    pool = GeventPool(pool_size)
    func = GetUrlByRequests(use_head=use_head)

    return pool.map(func, lstUrl)


def batchping(urls):
    pool = GeventPool(POOL_SIZE)

    jobs = [pool.spawn(ping, u) for u in urls]
    gevent.joinall(jobs)

    return jobs

'''
lstUrl = [
    'http://www.ebay.com',
    'http://www.ebay.com/articulos-coleccionables-y-arte',
    'http://www.ebay.com/articulos-deportivos/deportes-y-fitness',
    'http://www.ebay.com/hogar-y-jardin/articulos-para-el-jardin-y-exteriores',
    'http://slc4b01c-5294.stratus.slc.ebay.com:8080/www.ebay.com/hogar-y-jardin/',
    'http://www.ebay.com/motores/lanchas-y-barcos',
    'http://www.ebay.com/moda-es/carteras-bolsos-y-accesorios',
    'http://www.ebay.com/hogar-y-jardin/decoracion-para-el-hogar']

for one in batchping(lstUrl):
    print dir(one)
    #print one.value
'''

if __name__ == '__main__':
    lstUrl = []
    for one in open(sys.argv[1]).readlines():
        lstUrl.append(one.strip())
    #print lstUrl

    #for one in batchping(lstUrl):
    #   print one.value
    for one in getUrlsByRequests(lstUrl):
        print one

    #pool = GeventPool(10)
    #for one in pool.imap(ping, lstUrl):
    #   print one

