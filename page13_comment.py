# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:46:18 2023

@author: user
"""

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

def NS_users_crawler(codes, page):
    # User-Agent 설정
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    result_df = pd.DataFrame([])

    n_ = 0
    breakfull = True
    for page in range(1, page):
        n_ += 1
        if (n_ % 10 == 0):
            print('================== Page ' + str(page) + ' is done ==================')
        url = "https://finance.naver.com/item/board.naver?code=%s&page=%s" % (codes, str(page))
        # html → parsing
        html = requests.get(url, headers=headers).content
        # 한글 깨짐 방지 decode
        soup = BeautifulSoup(html.decode('euc-kr', 'replace'), 'html.parser')
        table = soup.find('table', {'class': 'type2'})
        tb = table.select('tbody > tr')
        
        result_ck=pd.DataFrame([])
        for i in range(2, len(tb)):
            if len(tb[i].select('td > span')) > 0:
                date = tb[i].select('td > span')[0].text
                title = tb[i].select('td.title > a')[0]['title']
                views = tb[i].select('td > span')[1].text
                pos = tb[i].select('td > strong')[0].text
                neg = tb[i].select('td > strong')[1].text
                table = pd.DataFrame({'날짜': [date], '제목': [title], '조회': [views], '공감': [pos], '비공감': [neg]})
                
                result_df = result_df.append(table)
                result_ck = result_ck.append(table)
        if (len(result_ck)<20):
            breakfull = False
            break



    return result_df


logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(100)
root=''

fund_asset=pickle.load(open(root+'fund_asset.pkl','rb'))   
maxend=max(fund_asset[fund_asset['TRD_DT']<=str(Pday()).replace("-", "")[0:8]]['TRD_DT'])
maxend=datetime.strptime(maxend,'%Y%m%d')

class generate():

    
    # Streamlit 생성 메인 파트
    def __init__(self):  
        global start_t
        global end_t

        e1,col1,e2,e3, col2 = st.columns( [0.1,0.1,0.1,0.5, 0.2])
    
        with col2:               # To display brand log
                st.image(logo, width=200 )  

        self.kor_stk()

        

############################## 국내주식    ###########################

    def kor_stk(self):
        
        ##데이터 불러오기
       

        ace=pickle.load(open(root+'aceetf.pkl','rb'))   

        option1 = st.selectbox("펀드명", ace['NM'],key=13)
        
        df_comments=NS_users_crawler(ace[ace['NM']==option1]['ETF_CD'].reset_index()['ETF_CD'][0][1:],30)
        
        st.dataframe(df_comments,width=1000)
