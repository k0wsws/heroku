# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 08:32:06 2023

@author: user
"""

from datetime import date
from pandas.tseries.offsets import BDay
import exchange_calendars as ecals


XKRX = ecals.get_calendar("XKRX") # 한국 코드


def Pday(): 
    
    day=date.today()-BDay(1)
    while XKRX.is_session(day) is False:
        day=day-BDay(1)
    return day
