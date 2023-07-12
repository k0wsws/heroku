# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:17:37 2023

@author: user
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import urllib.request
import datetime
import json
import glob
import sys
import os
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle
import re
import plotly.express as px
import requests
from bs4 import BeautifulSoup


import warnings
warnings.filterwarnings(action='ignore')
logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(100)
root=''

#%matplotlib inline
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.grid'] = False

pd.set_option('display.max_columns', 250)
pd.set_option('display.max_rows', 250)
pd.set_option('display.width', 100)

pd.options.display.float_format = '{:.2f}'.format

class NaverDataLabOpenAPI():
    """
    네이버 데이터랩 오픈 API 컨트롤러 클래스
    """
    def __init__(self, client_id, client_secret):
        """
        인증키 설정 및 검색어 그룹 초기화
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"
        
    def add_keyword_groups(self, group_dict):
        """
        검색어 그룹 추가
        """

        keyword_gorup = {
            'groupName': group_dict['groupName'],
            'keywords': group_dict['keywords']
        }
        
        self.keywordGroups.append(keyword_gorup)
        print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")
        
    def get_data(self, startDate, endDate, timeUnit, device, ages, gender):
        """
        요청 결과 반환
        """

        # Request body
        body = json.dumps({
            "startDate": startDate,
            "endDate": endDate,
            "timeUnit": timeUnit,
            "keywordGroups": self.keywordGroups,
            "device": device,
            "ages": ages,
            "gender": gender
        }, ensure_ascii=False)
        
        # Results
        request = urllib.request.Request(self.url)
        request.add_header("X-Naver-Client-Id",self.client_id)
        request.add_header("X-Naver-Client-Secret",self.client_secret)
        request.add_header("Content-Type","application/json")
        response = urllib.request.urlopen(request, data=body.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            # Json Result
            result = json.loads(response.read())
            
            df = pd.DataFrame(result['results'][0]['data'])[['period']]
            for i in range(len(self.keywordGroups)):
                tmp = pd.DataFrame(result['results'][i]['data'])
                tmp = tmp.rename(columns={'ratio': result['results'][i]['title']})
                df = pd.merge(df, tmp, how='left', on=['period'])
            self.df = df.rename(columns={'period': '날짜'})
            self.df['날짜'] = pd.to_datetime(self.df['날짜'])
            
        else:
            print("Error Code:" + rescode)
            
        return self.df
    
    def plot_daily_trend(self):
        """
        일 별 검색어 트렌드 그래프 출력
        """
        colList = self.df.columns[1:]
        n_col = len(colList)

        fig = plt.figure(figsize=(12,6))
        plt.title('일 별 검색어 트렌드', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=self.df['날짜'], y=self.df[colList[i]], label=colList[i])
        plt.legend(loc='upper right')
        
        return fig
    
    def plot_monthly_trend(self):
        """
        월 별 검색어 트렌드 그래프 출력
        """
        df = self.df.copy()
        df_0 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(0).reset_index().rename(columns={'날짜': '월'})
        df_1 = df.groupby(by=[df['날짜'].dt.year, df['날짜'].dt.month]).mean().droplevel(1).reset_index().rename(columns={'날짜': '년도'})

        df = pd.merge(df_1[['년도']], df_0, how='left', left_index=True, right_index=True)
        df['날짜'] = pd.to_datetime(df[['년도','월']].assign(일=1).rename(columns={"년도": "year", "월":'month','일':'day'}))
        
        colList = df.columns.drop(['날짜','년도','월'])
        n_col = len(colList)
                
        fig = plt.figure(figsize=(12,6))
        plt.title('월 별 검색어 트렌드', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=df['날짜'], y=df[colList[i]], label=colList[i])
        plt.legend(loc='upper right')
        
        return fig
    
class generate():

    
    # Streamlit 생성 메인 파트
    def __init__(self):  
        global start_t
        global end_t

        e1,col1,e2,e3, col2 = st.columns( [0.1,0.1,0.1,0.5, 0.2])
    
        with e1:   
           
            start_t=self.start_dt()
        with col1:
            end_t=self.end_dt()
        with col2:               # To display brand log
                st.image(logo, width=200 )  

        
        self.kor_stk()
        
    def start_dt(self):
        start = st.date_input(
            "기초일",
            pmonth)
        start=str(start)
        
        return start
        

    def end_dt(self):
        end = st.date_input(
            "기말일",
            Pday())
        end=str(end)
        return end

        

############################## 국내주식    ###########################

    def kor_stk(self):
        
        ##데이터 불러오기
        #st.write("검색어를 입력하세요")
        
        e1,col1,e2,e3, col2 = st.columns( [0.1,0.1,0.1,0.1, 0.6])
    
        with e1:   
           
            input1=st.text_input("검색어1",'ACE ETF',key=1)
        with col1:
            input2=st.text_input("검색어2",'KODEX ETF',key=2)
        with e2:
            input3=st.text_input("검색어3",'',key=3)
        with e3:
            input4=st.text_input("검색어4",'',key=4)
        
        
        if input2=='':
            keyword_group_set = {
    'keyword_group_1': {'groupName': input1, 'keywords': [input1]}
        }
        elif input3=='':
                  
            keyword_group_set = {
        'keyword_group_1': {'groupName': input1, 'keywords': [input1]},
        'keyword_group_2': {'groupName': input2, 'keywords': [input2]}
            }
        elif input4=='':
                  
            keyword_group_set = {
        'keyword_group_1': {'groupName': input1, 'keywords': [input1]},
        'keyword_group_2': {'groupName': input2, 'keywords': [input2]},
        'keyword_group_3': {'groupName': input3, 'keywords': [input3]}
            }
        else:
            keyword_group_set = {
        'keyword_group_1': {'groupName': input1, 'keywords': [input1]},
        'keyword_group_2': {'groupName': input2, 'keywords': [input2]},
        'keyword_group_3': {'groupName': input3, 'keywords': [input3]},
        'keyword_group_4': {'groupName': input4, 'keywords': [input4]}
            }
        
 
        
        # API 인증 정보 설정
        client_id = "YOgYiNw3999zNprIPIIO"
        client_secret = "jwW4hIXpfN"
        
        # 요청 파라미터 설정
        startDate = start_t
        endDate = end_t
        timeUnit = 'date'
        device = ''
        ages = []
        gender = ''
        
        # 데이터 프레임 정의
        naver = NaverDataLabOpenAPI(client_id=client_id, client_secret=client_secret)
        
        if input2=='':
            naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
        elif input3=='':
            naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
            naver.add_keyword_groups(keyword_group_set['keyword_group_2'])
        elif input4=='':
            naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
            naver.add_keyword_groups(keyword_group_set['keyword_group_2'])
            naver.add_keyword_groups(keyword_group_set['keyword_group_3'])
        else :
            naver.add_keyword_groups(keyword_group_set['keyword_group_1'])
            naver.add_keyword_groups(keyword_group_set['keyword_group_2'])
            naver.add_keyword_groups(keyword_group_set['keyword_group_3'])      
            naver.add_keyword_groups(keyword_group_set['keyword_group_4'])  
            
        df = naver.get_data(startDate, endDate, timeUnit, device, ages, gender)
        
        fig_1 = naver.plot_daily_trend()
        fig_2 = naver.plot_monthly_trend()
        
        
        st.plotly_chart(fig_1)
        st.plotly_chart(fig_2)

        
