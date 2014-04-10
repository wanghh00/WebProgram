'''
Created on Nov 12, 2013

@author: hcao1
'''
import requests
import json

from random import randrange
from random import choice

def getCatogories(site = 0,limit= 10):
    url= 'http://mbe.vip.ebay.com/merbak/v0/sites/{si}/categories?&limit={lmt}'.format(si=site, lmt=limit)
    r = requests.get(url)
    d = json.loads(r.text)
    results = d['data']['results']
    cid = list([results[i]['category']['id'] for i in range(len(results))])
    return cid

def getseeds(site=0, fc = 1, dis = 'random'):
    seeds = []
    clist = getCatogories(site)
    
    if dis == 'random':
        r = requests.get("http://merch.ebay.com/merch/sbe/query/?si={si}&allCats={cat}&sort=random&fc={fc}".format(
                                                                                            si=site,
                                                                                            cat=str(clist),
                                                                                            fc=fc))
        d = json.loads(r.text)
        
        seeds=list([i['id'] for i in d['data']])                                                         
    elif dis == 'eqaulCategory':
        for i in range(fc):
            cid = choice(clist)
            r = requests.get("http://merch.ebay.com/merch/sbe/query/?si={si}&allCats={cat}&sort=random&fc=1".format(
                                                                                            si=site,
                                                                                            cat=cid))
            d = json.loads(r.text)
            seed = d['data'][0]['id']
            seeds.append(seed)
    
    return seeds
        