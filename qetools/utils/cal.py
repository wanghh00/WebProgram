'''
Created on Nov 12, 2013

@author: hcao1
'''
import requests
import json
import base64
import io
import re
from datetime import datetime,timedelta
import logging
import time

from .ebaytime import *
from .exceptions import *
from .urlutils import *

envurl = "http://appmon.vip.ebay.com/logview/environments"
poolurl = "http://appmon.vip.ebay.com/logview/environment/{env}/pools"
defaultpoolurl = "http://appmon.vip.ebay.com/logview/pools"
machinesinpoolurl="http://appmon.vip.ebay.com/logview/pool/{pool}/machines"
overviewurl="http://appmon.vip.ebay.com/logview/pool/{pool}/machine/{machine}/machineOverview"
eventurl= r'http://appmon.vip.ebay.com/logview/pool/{pool}/machine/{machine}/eventDetail'
rlogideventurl=r'http://appmon.vip.ebay.com/logview/rlogid/{rlogid}/eventDetail'
rawlogurl = r'http://appmon.vip.ebay.com/logview/pool/{pool}/machine/{machine}/rawLog'

SEARCH_URL="http://appmon.vip.ebay.com/regexui/request"
SEARCH_STATUS_URL="http://appmon.vip.ebay.com/regexui/request/{id}/status"
SEARCH_RESULT_URL="http://appmon.vip.ebay.com/regexui/request/{id}/output?index={index}&count={count}"

def getenv():
    r = requests.get(envurl)
    d = json.loads(r.text)
    cats=d['data']
    assert d['type'] == 'environment', 'results are environments'
    return cats

def getpool(env):
    if env is None:
        link = defaultpoolurl
    else:
        link = poolurl.format(env=env)

    r = requests.get(link)
    d = json.loads(r.text)
    cats=d['data']
    assert d['type'] == 'pool', 'results are pools'
    return cats

def getmachines(pool):
    link =machinesinpoolurl.format(pool=pool)
    r = requests.get(link)
    d = json.loads(r.text)
    logging.debug("url", r.url)
    cats=d['data']
    assert d['type'] == 'machine', 'results are of type machine'
    return cats

#BUGBUG:
# 1. allow search just by machine
# 2. paramater check of type in the right set by decorator
#Types
#ERROR
#URL_FAIL
#SQL_FAIL
#TRANSACTION_FAIL
#MARK_UP
#MARK_DOWN         EventData
#LONG_URL
#IP         EventData
#WARN         EventData
#UNFINISHED_URL
#ACTIVITY
#SUMMARY
#PERFMON_METRICS         PerfmonData
#USER_EVENT
#IIS_RESTART         EventData
#PUB_RECONNECT         EventData

def getoverview(machine, pool, types='SUMMARY', starttime = None, endtime = None):
    if isinstance(types, str):
        types=[types]
    typeCollection = list([{'type': t} for t in types])
    collectorTypeInput={}
    collectorTypeInput["collectorTypeInputList"] = typeCollection
    logging.debug(json.dumps(collectorTypeInput))
    c=base64.urlsafe_b64encode(json.dumps(collectorTypeInput).encode())
    logging.debug(c)
    # get start time and end time
    if not endtime:
        endtime = getcurrentebaytime()
    if not starttime:
        dt = datetime.utcnow()
        delta = timedelta(hours=-1)
        starttime = getebaytime(dt + delta)
    # verify
    logging.debug("starttime: %s", starttime)
    logging.debug("endtime: %s", endtime)

    if ebaytimetotime(starttime) > ebaytimetotime(endtime):
        raise IllegalArgumentError("startime {st} is later than endtime {et}".format(st=starttime, et=endtime))

    # have to manually build parameters to prevent requests url-encode collectorTypeInput.
    payload={}
    payload['collectorTypeInput']=c.decode()
    payload['starttime']=starttime
    payload['endtime']=endtime

    paras='&'.join(['%s=%s' %(k,v) for k,v in payload.items()])
    logging.debug(paras)

    r = requests.get(overviewurl.format(pool=pool, machine=machine) + '?' +  paras)
    logging.debug("url: %s", r.url)
    return r.text

def getevent(machine, pool, datetime, thread, timestamp):
    payload={}
    payload['datetime']=datetime
    payload['thread']=thread
    payload['evt']=timestamp
    r = requests.get(eventurl.format(pool=pool, machine=machine), params=payload)
    print(r.url)
    return r.text

def geteventbyrlogid(rlogid):
    r = requests.get(rlogideventurl.format(rlogid=rlogid))
    print(r.url)
    return r.text

def getrawlog(machine, pool, thread, starttime = None, timestamp = None):
    if not starttime:
        dt = datetime.utcnow()
        delta = timedelta(hours=-1)
        starttime = getebaytime(dt + delta)
    payload={}
    payload['datetime']=starttime
    payload['thread']=thread
    if timestamp:
        payload['evt']=timestamp
    # have to manually build parameters to prevent requests url-encode collectorTypeInput.
    r = requests.get(rawlogurl.format(pool=pool, machine=machine), params=payload)
    logging.debug("url: %s", r.url)
    return r.text

def getthreadIds(machine, pool, starttime = None, endtime = None):
    e = getoverview(machine, pool, 'ACTIVITY', starttime, endtime)
    d = json.loads(e)
    from jsonpath_rw import parse
    jsonpath_expr = parse(r"responseMap..threadId.`parent`")
    dl = [match.value for match in jsonpath_expr.find(d)]

    return set([hex(entry['threadId']) for entry in dl if entry['type'] == 'ACTIVITY'])

def getSearchTargets(pool, regex, count = 10000):
    r = getregex(pool, regex, count = count)
    d = json.loads(r)
    machines = []
    pool = []
    threads =[]
    for i in d['records']:
        s = i['url'].replace('\u0026', '&').replace('\u003d', '=')
        d = extractUrlPara(s)
        machinename= i['values']['Machine']

        machines.append(machinename + '.stratus.phx.ebay.com' if machinename.startswith("phx") else machinename + '.stratus.slc.ebay.com')
        pool.append(i['values']['Pool'])
        threads.append(d['thread'])

    paras = set(zip(machines, pool, threads))
    return paras



def splitrawlog(filestring):
    tranlist = []
    buf = io.StringIO(filestring)
    #seek to the first trans
    intran = False
    for line in buf:
        if not intran:
            if line.startswith('0'):
                if RawTransaction.split(line)[2] != 'Error':
                    tran = []
                    tran.append(line)
                    intran = True
        else:
            if not '------' in line:
                tran.append(line)
                if line.startswith('0'):
                    intran = False
                    tranlist.append(tran)

    return tranlist

def splitrawurllog(filestring):
    tranlist = []
    buf = io.StringIO(filestring)
    #seek to the first trans
    intran = False
    for line in buf:
        if not intran:
            if line.startswith('0'):
                t = RawTransaction.split(line)
                if len(t) == 5 and t[2] == 'URL' and t[1].startswith('t'):
                    tran = []
                    tran.append(line)
                    intran = True
        else:
            if not '------' in line:
                tran.append(line)
                if line.startswith('0'):
                    intran = False
                    tranlist.append(tran)

    return tranlist

def find(log, transtype, name):
    pass

class RawTransaction(object):

    def __init__(self, rawlines):
        self.name = None
        self.type = None
        self.starttime = None
        self.endtime = None
        self.raw = rawlines

    def analyze(self):
        # read the first line to get type, name, and stattine
        field = RawTransaction.split(self.raw[0])
        self.type = field[2]
        self.name = field[3]
        self.startime = field[1][1:]
        # read the last line to endtime
        field = RawTransaction.split(self.raw[-1])
        self.endtime=field[1][1:]

    def find(self, transtype, name):
        for l in self.raw:
            field = RawTransaction.split(l)
            if field[2] == transtype and field[3] == name:
                return field

    #split a line to segments
    @staticmethod
    def split(s):
        return re.split('\s+', s, maxsplit=7)


def getregex(pool, regex, starttime = None, endtime=None, startindex = 1, count = 1000):

    if not endtime:
        endtime = getcurrentebaytime()
    if not starttime:
        dt = datetime.utcnow()
        delta = timedelta(hours=-1)
        starttime = getebaytime(dt + delta)

    #send a request
    payload = {'environment': 'prod',
               'pool': pool,
               'startTime' : starttime,
               'endTime' : endtime,
               'regexs' : regex
               }
    r = requests.post(SEARCH_URL, data=json.dumps(payload))
    requestId=r.text

    #query status
    completed=True;
    while completed:
        logging.info('Peek request status...')
        time.sleep(10)  # Delay for 1 minute (60 seconds)
        r = requests.get( SEARCH_STATUS_URL.replace('{id}',requestId))
        logging.debug('status:' + r.text)
        if r.text == 'SUCCEEDED' or r.text == 'PARTIALLY_SUCCEEDED':
            completed=False

    #Now get the results
    r = requests.get(SEARCH_RESULT_URL.format(id=requestId, index =startindex, count= count))
    return r.text



if __name__ == '__main__':
    pass
    #ids = getthreadIds('phx6b02c-4637.stratus.phx.ebay.com', 'r1reco')
    #text = getrawlog('phx6b02c-4637.stratus.phx.ebay.com', 'r1reco', ids.pop())

    #print(geteventbyrlogid('t6pht%3D9un%7F4g65%60%280537-1424e97e155-0x20c3'))
    #tl = splitrawlog(text)
    #for t in tl:
    #    rt= RawTransaction(t)
    #    rt.analyze()
    #    print(rt.endtime)
