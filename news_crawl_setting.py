# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 15:23:44 2023

@author: user
"""
from bs4 import BeautifulSoup
import telegram
import requests
import datetime
import shutil

#필요한 라이브러리 
import pandas as pd 
import re
from datetime import datetime
import os
import time
import numpy as np
from datetime import date,timedelta,datetime

root='C:\\Users\\user\\Desktop\\파이썬\\투자자별 현황\\dataset\\'

def read_by_keyword(keyword, news_num=10) :
    query = keyword
    news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&sm=tab_opt&sort=1&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Add%2Cp%3Aall&is_sug_officeid=0'
    req = requests.get(news_url.format(query))
    soup = BeautifulSoup(req.text, 'html.parser')

    news_dict = {}
    idx = 0
    cur_page = 1
    num=0

    while idx < news_num :
        table = soup.find('ul', {'class' : 'list_news'})
        li_list = table.find_all('li', {'id' : re.compile('sp_nws.*')})
        area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
        time = [li.find_all('span', {'class' : 'info'}) for li in li_list]
        a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]
        


        for n in a_list[:min(len(a_list), news_num - idx)] :
            if idx<10:
                num=idx
            else:
                num=idx-10*cur_page
            if len(time[num])>1:
                time[num]=time[num][1]
            news_dict[idx] = {'title' : n.get('title'),
                              'url' : n.get('href'),
                             'time': str(time[num]).replace('<span class="info">','').replace('</span>','').replace('[','').replace(']',''),
                             'Update_dt':datetime.now()}
            idx += 1

        cur_page += 1

        pages = soup.find('div', {'class' : 'sc_page_inner'})
        next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')
        req = requests.get('https://search.naver.com/search.naver' + next_page_url)
        soup = BeautifulSoup(req.text, 'html.parser')
    

        

    return pd.DataFrame(news_dict).T

df=read_by_keyword('SOL ETF',1500)

df['trd_dt']=str(df['Update_dt'][0])[0:10]

for i in range(len(df)):
    if df['time'][i][-3:]=='분 전':
        df['trd_dt'][i]=str(df['Update_dt'][i])[0:10].replace('-','')
    elif df['time'][i][-3:]=='간 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(hours=int(df['time'][i][-6:-4])))[0:10].replace('-','')
    elif df['time'][i][-3:]=='일 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(days=int(df['time'][i][-5:-3])))[0:10].replace('-','')
    else:
        df['trd_dt'][i]=str(df['time'][i])[0:10].replace('.','')

df.to_csv(root+"SOL_news.csv", encoding="utf-8-sig")


df=read_by_keyword('ACE ETF',3900)

df['trd_dt']=str(df['Update_dt'][0])[0:10]

for i in range(len(df)):
    if df['time'][i][-3:]=='분 전':
        df['trd_dt'][i]=str(df['Update_dt'][i])[0:10].replace('-','')
    elif df['time'][i][-3:]=='간 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(hours=int(df['time'][i][-6:-4])))[0:10].replace('-','')
    elif df['time'][i][-3:]=='일 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(days=int(df['time'][i][-5:-3])))[0:10].replace('-','')
    else:
        df['trd_dt'][i]=str(df['time'][i])[0:10].replace('.','')

df.to_csv(root+"KINDEX_news.csv", encoding="utf-8-sig")


df=read_by_keyword('KODEX ETF',3900)

df['trd_dt']=str(df['Update_dt'][0])[0:10]

for i in range(len(df)):
    if df['time'][i][-3:]=='분 전':
        df['trd_dt'][i]=str(df['Update_dt'][i])[0:10].replace('-','')
    elif df['time'][i][-3:]=='간 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(hours=int(df['time'][i][-6:-4])))[0:10].replace('-','')
    elif df['time'][i][-3:]=='일 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(days=int(df['time'][i][-5:-3])))[0:10].replace('-','')
    else:
        df['trd_dt'][i]=str(df['time'][i])[0:10].replace('.','')

df.to_csv(root+"KODEX_news.csv", encoding="utf-8-sig")


df=read_by_keyword('TIGER ETF',3900)

df['trd_dt']=str(df['Update_dt'][0])[0:10]

for i in range(len(df)):
    if df['time'][i][-3:]=='분 전':
        df['trd_dt'][i]=str(df['Update_dt'][i])[0:10].replace('-','')
    elif df['time'][i][-3:]=='간 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(hours=int(df['time'][i][-6:-4])))[0:10].replace('-','')
    elif df['time'][i][-3:]=='일 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(days=int(df['time'][i][-5:-3])))[0:10].replace('-','')
    else:
        df['trd_dt'][i]=str(df['time'][i])[0:10].replace('.','')

df.to_csv(root+"TIGER_news.csv", encoding="utf-8-sig")

df=read_by_keyword('KBSTAR ETF',3900)

df['trd_dt']=str(df['Update_dt'][0])[0:10]

for i in range(len(df)):
    if df['time'][i][-3:]=='분 전':
        df['trd_dt'][i]=str(df['Update_dt'][i])[0:10].replace('-','')
    elif df['time'][i][-3:]=='간 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(hours=int(df['time'][i][-6:-4])))[0:10].replace('-','')
    elif df['time'][i][-3:]=='일 전':
        df['trd_dt'][i]=str(df['Update_dt'][i]-timedelta(days=int(df['time'][i][-5:-3])))[0:10].replace('-','')
    else:
        df['trd_dt'][i]=str(df['time'][i])[0:10].replace('.','')

df.to_csv(root+"KBSTAR_news.csv", encoding="utf-8-sig")