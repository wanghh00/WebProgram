'''
Created on Nov 13, 2013

@author: hcao1
'''
import logging
import gevent
from urllib.parse import unquote_plus
import re

from .cal import *
from .urlutils import *
#split raw log into a list of lines
class PlmtTransaction(RawTransaction):    

    def __init__(self, rawlines):        
        super(PlmtTransaction, self).__init__(rawlines)
        super(PlmtTransaction, self).analyze()
        if self.type != 'URL' or not self.name.startswith('100'):
            self.valid = False
        else:
            self.valid = True
        
        # filter out unfinished transaction
        field = RawTransaction.split(self.raw[-1])
        self.completeness=field[4]
        if self.completeness == 'UNFINISHED':
            self.valid = False
        
    def analyze(self):
        try:      
            # read payload
            f=self.find('URL', 'Payload')
            self.payload=f[5]
            logging.debug("payload: %s", self.payload)

            # find cguid
            f=self.find('URL', 'Request')
            p = extractUrlPara(f[5])
            self.si = p['si']
            logging.debug("site: %s", self.si)      
            if 'cguid' in p:
                self.cguid = p['cguid']
            else:
                f=self.find('URL', 'RequestHeaders')
                if f and '^cguid/' in f[4]:
                    cguid=f[4].split('^cguid/')[1]
                    self.cguid = cguid.split('^tguid')[0][:-8]
                else:
                    self.cguid = None
                                
            logging.debug("cguid: %s", self.cguid)                    
            
            # read  soj
            f=self.find('SOJ', 'a')
            #need to hack into the string to get plmt
            sojA = f[5].split('&plmt=')
            if len(sojA) > 1:
                soj = sojA[1]        
                self.soj=unquote_plus(soj.split('&')[0])
            else:
                self.soj = None
            logging.debug("soj: %s", self.soj)
            # get user
            if '&u=' in f[5]:
                user = f[5].split('&u=')[1]        
                self.user= user.split('&')[0]
            else:
                self.user= None
  
            if self.user is None:                
                self.user= p.get('usr')                            
            logging.debug("user: %s", self.user)
   
            # read rlogid
            f=self.find('URL', 'ResponseHeaders')
            d = spliturlparameters(f[6])        
            self.rlogid = d.get('RlogId')
            logging.debug("rlogid: %s", self.rlogid)
        except:
            print (self.raw)
            raise
    def find(self, transtype, name):
        for l in self.raw:
            field = RawTransaction.split(l)
            if field[2] == transtype and field[3] == name:
                return field 
              
    #split a line to segments
    @staticmethod
    def split(s):
        return re.split('\s+', s, maxsplit=7)

# construct a plmt from the exact level of activities.
# a transcation record may have several plmts.
class PlmtJsonTransaction(object):
    def __init__(self, raw):        
        self.name = raw['calActivitesResp'][0]['name']
        self.type = raw['calActivitesResp'][0]['type']
        self.starttime = raw['calActivitesResp'][0]['messageClass'][1:]
        self.endtime = raw['calActivitesResp'][-1]['messageClass'][1:]
        self.raw = raw

        if self.type != 'URL' or not self.name.startswith('100'):
            self.valid = False
        else:
            self.valid = True
        
        # filter out unfinished transaction
        self.completeness = raw['calActivitesResp'][-1]['status']
        if self.completeness == 'UNFINISHED':
            self.valid = False
        
    def analyze(self):
        try:      
            # read payload
            f=self.find('URL', 'Payload')
            self.payload=f['data']
            logging.debug("payload: %s", self.payload)

            # find cguid
            f=self.find('URL', 'Request')
            p = extractUrlPara(f['data'])
            self.si = p['si']
            logging.debug("site: %s", self.si)      
            if 'cguid' in p:
                self.cguid = p['cguid']
            else:
                f=self.find('URL', 'RequestHeaders')
                if f and '^cguid/' in f['data']:
                    cguid=f['data'].split('^cguid/')[1]
                    self.cguid = cguid.split('^tguid')[0][:-8]
                else:
                    self.cguid = None
                                
            logging.debug("cguid: %s", self.cguid)                    
            
            # read  soj
            f=self.find('SOJ', 'a')
            #need to hack into the string to get plmt
            sojA = f['data'].split('&plmt=')
            if len(sojA) > 1:
                soj = sojA[1]        
                self.soj=unquote_plus(soj.split('&')[0])
            else:
                self.soj = None
            logging.debug("soj: %s", self.soj)
            # get user
            if '&u=' in f['data']:
                user = f['data'].split('&u=')[1]        
                self.user= user.split('&')[0]
            else:
                self.user= None
  
            if self.user is None:                
                self.user= p.get('usr')                            
            logging.debug("user: %s", self.user)
   
            # read rlogid
            f=self.find('URL', 'ResponseHeaders') 
            d = dict(item.split("=") for item in re.split("&| ", f['data']))     
            self.rlogid = d.get('RlogId')
            logging.debug("rlogid: %s", self.rlogid)
        except:
            print (self.raw)
            raise
    def find(self, transtype, name):
        for l in self.raw['calActivitesResp']:
            if l.get('type') == transtype and l.get('name') == name:
                return l
    
def worker(machine, pool, myid):
    text = getrawlog(machine, pool, myid)    
    tl = splitrawurllog(text)
    if not tl or not PlmtTransaction(tl[0]).valid:
        return None
    else:
        users = []
        for t in tl:            
            rt= PlmtTransaction(t)
            if rt.valid:
                rt.analyze()
                if rt.user or rt.cguid:
                    users.append({'user' : rt.user, 'cguid':rt.cguid, 'si' : rt.si})
        
        return users

def analyzelog(paras):
    jobs = [gevent.spawn(worker, p[0], p[1], p[2]) for p in paras]
    gevent.joinall(jobs)


if __name__ == '__main__':
    pass
    
    #worker('slc4b01c-3bc4.stratus.slc.ebay.com', 'r1reco', '0x55')
     
     
#     text = getrawlog(u'phx6b02c-4637.stratus.phx.ebay.com', u'r1reco', u'0xc6e', u'2013/11/13 16:14')   
#     tl = splitrawlog(text)
#     
#     if not PlmtTransaction(tl[0]).valid:
#         pass
#     else:
#         users = []
#         for t in tl:            
#             rt= PlmtTransaction(t)
#             if rt.valid:
#                 print(rt.name)
#                 rt.analyze()  
    
#     import gevent
#     from gevent import monkey
#     monkey.patch_all()
#     
#     r = regex('r1reco',["^.*\tURL\t1000.*$"])
#     print(r)
#     d = json.loads(r)
#     machines = []
#     pool = []
#     threads =[]
#     for i in d['records']:
#         s = i['url'].replace('\u0026', '&').replace('\u003d', '=')
#         d = extractUrlPara(s)
#         machinename= i['values']['Machine']
#         
#         machines.append(machinename + '.stratus.phx.ebay.com' if machinename.startswith("phx") else machinename + '.stratus.slc.ebay.com')
#         pool.append(i['values']['Pool'])
#         threads.append(d['thread'])
#         
#     paras = set(zip(machines, pool, threads))  
#     analyzelog(paras)


