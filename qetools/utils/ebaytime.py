'''
Created on Nov 12, 2013

@author: hcao1
'''
from datetime import datetime
from pytz import timezone
import pytz
import logging

def getebaytime(utctime):
    ebaytimezone = timezone('US/Pacific')
    ebaytime = utctime.replace(tzinfo=pytz.utc).astimezone(ebaytimezone)
    return ebaytime.strftime('%Y/%m/%d %H:%M') 
    
def getcurrentebaytime():
    dt = datetime.utcnow()
    return getebaytime(dt)

def ebaytimetotime(timestr):
    logging.debug(timestr)
    # assume in Y/M/D H:M format
    timetuple = timestr.split(' ')
    
    date = timetuple[0].split('/')
    time = timetuple[1].split(':')
    return datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), 0)
    
