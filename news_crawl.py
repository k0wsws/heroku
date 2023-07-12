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
from datetime import date,timedelta,datetime
import DB_ETF as DB
import numpy as np

root='C:\\Users\\user\\Dashboard\\dataset\\'
conn=DB.conn()
cursor = conn.cursor()

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

def crawl(num_news=100):
    df=read_by_keyword('ACE ETF',num_news)
    
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
    
    df.to_csv(root+"ACE_news_new.csv", encoding="utf-8-sig")
    
    
    df=read_by_keyword('KODEX ETF',num_news)
    
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
    
    df.to_csv(root+"KODEX_news_new.csv", encoding="utf-8-sig")
    
    
    df=read_by_keyword('TIGER ETF',num_news)
    
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
    
    df.to_csv(root+"TIGER_news_new.csv", encoding="utf-8-sig")
    
    df=read_by_keyword('KBSTAR ETF',num_news)
    
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
    
    df.to_csv(root+"KBSTAR_news_new.csv", encoding="utf-8-sig")
    
    df=read_by_keyword('SOL ETF',num_news)
    
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
    
    df.to_csv(root+"SOL_news_new.csv", encoding="utf-8-sig")
    
    
    ################################데이터 불러오기##########################################
    
    ##ACE
    df = pd.read_csv(root+"ACE_news_new.csv",encoding='utf-8-sig')
    
    ## KODEX
    df2 = pd.read_csv(root+"KODEX_news_new.csv",encoding='utf-8-sig') 
    
    # TIGER   
    df3 = pd.read_csv(root+"TIGER_news_new.csv",encoding='utf-8-sig')
        
    # KBSTAR  
    df4 = pd.read_csv(root+"KBSTAR_news_new.csv",encoding='utf-8-sig')      
    
    # SOL  
    df5 = pd.read_csv(root+"SOL_news_new.csv",encoding='utf-8-sig')  
    
    ##################################데이터 전처리##############################################
    
    df=df.iloc[:,1:]
    df=df.drop_duplicates(['title','url','trd_dt'])
    
    df2=df2.iloc[:,1:]
    df2.drop_duplicates(['title','url','trd_dt'])
    
    df3=df3.iloc[:,1:]
    df3.drop_duplicates(['title','url','trd_dt'])
    
    df4=df4.iloc[:,1:]
    df4.drop_duplicates(['title','url','trd_dt'])
    
    df5=df5.iloc[:,1:]
    df5.drop_duplicates(['title','url','trd_dt'])
    
    df_all = pd.read_csv(root+"ACE_news.csv",encoding='utf-8-sig')
    df_all=df_all.iloc[:,1:]
    
    df_all2 = pd.read_csv(root+"KODEX_news.csv",encoding='utf-8-sig')
    df_all2=df_all2.iloc[:,1:]
    
    df_all3 = pd.read_csv(root+"TIGER_news.csv",encoding='utf-8-sig')
    df_all3=df_all3.iloc[:,1:]
    
    df_all4 = pd.read_csv(root+"KBSTAR_news.csv",encoding='utf-8-sig')
    df_all4=df_all4.iloc[:,1:]
    
    df_all5 = pd.read_csv(root+"SOL_news.csv",encoding='utf-8-sig')
    df_all5=df_all5.iloc[:,1:]
    
    
    # 2. 겹치는 데이터가 있는지 확인
    news_df = df['url'].values.tolist()
    news_all = df_all['url'].values.tolist()
    new_links = [link for link in news_df if link not in news_all]
    
    # 3. 새로운 데이터의 갯수
    cnt = 0
    for links in new_links :
        if links in news_df :
            cnt += 1
    print(cnt)
    
    # 5. 신규 뉴스
    #     news_df2 = pd.DataFrame(df2).T
    news_df = df[np.isin(df['url'], new_links)]
    news_df = news_df.drop_duplicates()
    
    
    # 5. 기존 데이터와 합치기
    final_news = pd.concat([news_df, df_all])
    final_news.to_csv(root+"ACE_news.csv",encoding='utf-8-sig')
    
    
    #############2222
    
    # 2. 겹치는 데이터가 있는지 확인
    news_df2 = df2['url'].values.tolist()
    news_all2 = df_all2['url'].values.tolist()
    new_links2 = [link for link in news_df2 if link not in news_all2]
    
    # 3. 새로운 데이터의 갯수
    cnt = 0
    for links in new_links2 :
        if links in news_df2 :
            cnt += 1
    print(cnt)
    
    # 5. 신규 뉴스
    #     news_df2 = pd.DataFrame(df2).T
    news_df2 = df2[np.isin(df2['url'], new_links2)]
    news_df2 = news_df2.drop_duplicates()
    
    # 5. 기존 데이터와 합치기
    final_news2 = pd.concat([news_df2, df_all2])
    final_news2.to_csv(root+"KODEX_news.csv",encoding='utf-8-sig')
    
    #############3333
    
    # 2. 겹치는 데이터가 있는지 확인
    news_df3 = df3['url'].values.tolist()
    news_all3 = df_all3['url'].values.tolist()
    new_links3 = [link for link in news_df3 if link not in news_all3]
    
    # 3. 새로운 데이터의 갯수
    cnt = 0
    for links in new_links3 :
        if links in news_df3 :
            cnt += 1
    print(cnt)
    
    # 5. 신규 뉴스
    #     news_df2 = pd.DataFrame(df2).T
    news_df3 = df3[np.isin(df3['url'], new_links3)]
    news_df3 = news_df3.drop_duplicates()
    
    # 5. 기존 데이터와 합치기
    final_news3 = pd.concat([news_df3, df_all3])
    final_news3.to_csv(root+"TIGER_news.csv",encoding='utf-8-sig')  
    
    #############3333
    
    # 2. 겹치는 데이터가 있는지 확인
    news_df4 = df4['url'].values.tolist()
    news_all4 = df_all4['url'].values.tolist()
    new_links4 = [link for link in news_df4 if link not in news_all4]
    
    # 3. 새로운 데이터의 갯수
    cnt = 0
    for links in new_links4 :
        if links in news_df4 :
            cnt += 1
    print(cnt)
    
    # 5. 신규 뉴스
    #     news_df2 = pd.DataFrame(df2).T
    news_df4 = df4[np.isin(df4['url'], new_links4)]
    news_df4 = news_df4.drop_duplicates()
    
    # 5. 기존 데이터와 합치기
    final_news4 = pd.concat([news_df4, df_all4])
    final_news4.to_csv(root+"KBSTAR_news.csv",encoding='utf-8-sig')  
    
    #############555555
    
    # 2. 겹치는 데이터가 있는지 확인
    news_df5 = df5['url'].values.tolist()
    news_all5 = df_all5['url'].values.tolist()
    new_links5 = [link for link in news_df5 if link not in news_all5]
    
    # 3. 새로운 데이터의 갯수
    cnt = 0
    for links in new_links5 :
        if links in news_df5 :
            cnt += 1
    print(cnt)
    
    # 5. 신규 뉴스
    #     news_df2 = pd.DataFrame(df2).T
    news_df5 = df5[np.isin(df5['url'], new_links5)]
    news_df5 = news_df5.drop_duplicates()
    
    # 5. 기존 데이터와 합치기
    final_news5 = pd.concat([news_df5, df_all5])
    final_news5.to_csv(root+"SOL_news.csv",encoding='utf-8-sig')  
    
    
        
    #############################인서트###########################
    
    #ACE
    for index,row in news_df.iterrows():
        cursor.execute("INSERT INTO ES_NEWS_DATA  values(?,?,?,?)", row.trd_dt, 'ACE', row.title,row.url)
    
    cursor.commit()
    
    #KODEX
    for index,row in news_df2.iterrows():
        cursor.execute("INSERT INTO ES_NEWS_DATA  values(?,?,?,?)", row.trd_dt, 'KODEX', row.title,row.url)
    
    cursor.commit()
    
    #TIGER
    for index,row in news_df3.iterrows():
        cursor.execute("INSERT INTO ES_NEWS_DATA  values(?,?,?,?)", row.trd_dt, 'TIGER', row.title,row.url)
    
    cursor.commit()
    
    #KBSTAR
    for index,row in news_df4.iterrows():
        cursor.execute("INSERT INTO ES_NEWS_DATA  values(?,?,?,?)", row.trd_dt, 'KBSTAR', row.title,row.url)
    
    cursor.commit()
    
    #SOL
    for index,row in news_df5.iterrows():
        cursor.execute("INSERT INTO ES_NEWS_DATA  values(?,?,?,?)", row.trd_dt, 'SOL', row.title,row.url)
    
    cursor.commit()
    
    
