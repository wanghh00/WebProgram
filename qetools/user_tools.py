#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, unicode_literals

import requests
import urllib

DEFAULT_ENV = 'prod'

BASE_URLS = {
    'qa': 'http://myworldsvc.stratus.qa.ebay.com/mywrldsvc/v1/myworld',
    'prod': 'http://www.mywrldsvc.stratus.ebay.com/mywrldsvc/v1/myworld',
    }

def name_to_id(username, env=DEFAULT_ENV):
    base = BASE_URLS[env]
    url = '{}/user/{}/indexcard?ident=username'
    url = url.format(base, urllib.quote(username))
    r = requests.get(url)

    data = r.json()
    return data.get('userId')

def id_to_name(user_id, env=DEFAULT_ENV):
    base = BASE_URLS[env]
    url = '{}/user/{:d}/indexcard?ident=userId'
    url = url.format(base, user_id)
    r = requests.get(url)

    data = r.json()
    return data.get('loginName')

if __name__ == '__main__':
    DEFAULT_QA_USER_ID = 1189881165
    DEFAULT_PROD_USER_ID = 1087728519
    import argparse
    parser = argparse.ArgumentParser(description='Lookup username or oracle id from the other in prod or qa')
    parser.add_argument('--qa', '-q', action='store_true', help='lookup in the QA environment')
    parser.add_argument('--production', '-p', action='store_true', help='lookup in the Prod environment (default)')
    parser.add_argument('-i', '--id', default=0, type=int, help='oracle id for which we want a username')
    parser.add_argument('-u', '--username', default='', type=str, help='username for which we want a user id')
    args = parser.parse_args()

    env = DEFAULT_ENV
    if args.qa:
        env = 'qa'
    elif args.production:
        env = 'prod'

    if args.id:
        username = id_to_name(args.id, env)
        print('{:d} -> {}'.format(args.id, username))

    if args.username:
        user_id = name_to_id(args.username, env)
        print('{} -> {}'.format(args.username, user_id))
