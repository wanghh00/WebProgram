#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json, copy, urllib
import sys, subprocess
import argparse
import logging; LOG = logging.getLogger(__name__)

from utils import comm
from utils import geventpool

class CmdChkUrlStatus(object):
    def __init__(self, lstArg=None):
        self.ret = {'__stat':0, '__name': 'CmdChkUrlStatus', '__err':'' }
        try:
            self.args = self.retParser().parse_args(lstArg)
            LOG.debug('Args: %s', str(self.args))
        except Exception as ex:
            LOG.exception(ex)
            self.ret.update({ '__stat':-100, '__err': 'Failed to parse_args [%s]' % str(ex) })

    def retParser(self):
        parser = comm.ThrowingArgumentParser()
        parser.add_argument('-f', '--file', help='<file>')
        parser.add_argument('-l', '--link', action='append', help='<link>')
        return parser

    def checkResults(self, results):
        lstErr = []; nTest = 0; nFailure = 0; nError = 0
        for one in results:
            nTest += 1
            if one['status'] == 200: continue
            nFailure += 1
            lstErr.append('Get %s failed' % one['url'])

        self.ret['__assert'] = { 'errors':lstErr }

    def __call__(self):
        if self.ret['__stat'] : return self.ret

        lstUrl = []

        try:
            if self.args.file:
                lstUrl += map(lambda x: x.strip(), open(self.args.file).readlines())

            if self.args.link: lstUrl += self.args.link

            self.ret['__ret'] = geventpool.getUrlsByRequests(lstUrl)
            self.checkResults(self.ret['__ret'])
        except Exception as ex:
            LOG.exception(ex)
            self.ret.update({ '__stat':-200, '__err': 'Failed to parse_args [%s]' % str(ex) })

        return self.ret

if __name__ == '__main__':
    logging.basicConfig(format=comm.LOGFMT,datefmt=comm.LOGDATEFMT)
    logging.getLogger().setLevel(logging.INFO)
    #logging.getLogger().setLevel(logging.DEBUG)

    ret = CmdChkUrlStatus(sys.argv[1:])()
    print ret
    sys.exit(0)

    lstUrl = []
    for one in open(sys.argv[1]).readlines():
        lstUrl.append(one.strip())
    #print lstUrl

    #for one in batchping(lstUrl):
    #   print one.value

    pool = GeventPool(10)
    for one in pool.imap(chkUrlStatus, lstUrl):
        print one
    