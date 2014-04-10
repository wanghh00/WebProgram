'''
Created on Nov 13, 2013

@author: hcao1
'''
from urllib.parse import unquote_plus

def spliturlparameters(s):
    d = dict(item.split("=") for item in s.split("&"))
    return d

def decodeandspliturlparameters(s):
    urldecoded = unquote_plus(s)
    return spliturlparameters(urldecoded)

def extractUrlPara(url):
    urldecoded = unquote_plus(url)
    payload = urldecoded.split("?", 1)[1]
    trunks = payload.split("&")
    for t in trunks:
        if not '=' in t:
            trunks.remove(t) 
    d = dict(item.split("=", 1) for item in trunks)
    return d


