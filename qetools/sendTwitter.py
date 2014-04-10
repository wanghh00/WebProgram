#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import requests
import urllib, argparse
import json, sys
from requests_oauthlib import OAuth1
from urlparse import parse_qs

DctUserToken = {
    'FeedQE' : {'CONSUMER_KEY':"xWF6m6nIFy7pLrmcK2YZGg", 'CONSUMER_SECRET':"9DLQ1hk9RfKHBawOnryT6sPbfgQPK2PCtiXT4AQ", 
        'OAUTH_TOKEN':"2207494622-kcXezDeTYJwoOilfaeoRs1LmLoeb0A2rpldCNEG", 'OAUTH_TOKEN_SECRET':"4xRVH9h2uM5ywgOI57BFTIe1OdpfO1QDw4I4Pslv4Kh5O"}, }

DctTwitterUrls = {
    'update': 'https://api.twitter.com/1.1/statuses/update.json',
    'user_timeline': 'https://api.twitter.com/1.1/statuses/user_timeline.json', }

def retArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', default='FeedQE')
    parser.add_argument('-m', '--message')
    parser.add_argument('-i', '--interface', default='update')
    return parser

def getOauth(user):
    dct = DctUserToken.get(user)
    if not dct: raise RuntimeError('Unauthorized twitter user [%s]', user)
    return OAuth1(dct['CONSUMER_KEY'], client_secret=dct['CONSUMER_SECRET'], resource_owner_key=dct['OAUTH_TOKEN'], resource_owner_secret=dct['OAUTH_TOKEN_SECRET'])

def twitterStatus_update(message, oauth):
    if not message: raise RuntimeError('Message could not be empty!')
    
    ret = {'stat':-1, 'ret':None}
    r = requests.post(url=DctTwitterUrls['update'], data='status=%s' % urllib.quote(message), auth=oauth)
    ret['stat'] = r.status_code
    if r.status_code == 200: ret['ret'] = r.json()
    
    return ret

def twitterStatus_user_timeline(oauth):
    ret = {'stat':-1, 'ret':None}
    
    r = requests.get(url=DctTwitterUrls['user_timeline'], auth=oauth)
    ret['stat'] = r.status_code
    if r.status_code == 200: ret['ret'] = r.json()
    
    return ret
    
if __name__ == "__main__":
    parser = retArgParser(); args = parser.parse_args()    
    oauth = getOauth(args.user)
        
    if args.interface == 'user_timeline':
        ret = twitterStatus_user_timeline(oauth)
    elif args.interface == 'update':
        ret = twitterStatus_update(args.message, oauth)
    
    print json.dumps(ret)
