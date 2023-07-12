# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:47:20 2023

@author: user
"""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import DB_ETF as DB
import seaborn as sns
from datetime import date,timedelta,datetime
from PIL import Image

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
#now = now.strftime('%Y-%m-%d')
pweek = pweek.strftime('%Y-%m-%d')
#pmonth = pmonth.strftime('%Y-%m-%d')



def news(trd_dt=now):
    
    col1, col2 = st.columns( [0.8, 0.2])
    
    with col1:   
       
        start = st.date_input(
            "시작일",pmonth)
        start=str(start).replace("-", "")[0:8]  
        end = st.date_input(
            "기준일",now)
        end=str(end).replace("-", "")[0:8]
    with col2:               # To display brand log
            st.image(logo, width=200 )
               


    sql="""
    SELECT DISTINCT CONVERT(VARCHAR(20),CONVERT(datetime,trd_dt,1),120) TRD_DT,
    COMPANY,
    COUNT(TITLE) OVER (PARTITION BY TRD_DT,
    COMPANY) '개수'
    fROM
    ES_NEWS_DATA
    WHERE
    TRD_DT BETWEEN '#{START_DT}' AND '#{END_DT}' ORDER BY TRD_DT desc,COMPANY asc
    """
    
    sql = sql.replace('#{START_DT}', start) 
    sql = sql.replace('#{END_DT}', end) 
    
    sql2="""
    SELECT * fROM ES_NEWS_DATA WHERE
    TRD_DT >= '20220719' order by trd_dt desc, company asc
    """
    
    sql3="""
    SELECT DISTINCT CONVERT(VARCHAR(20),CONVERT(datetime,trd_dt,1),120) TRD_DT,
    COMPANY,
    COUNT(TITLE) OVER (PARTITION BY TRD_DT,
    COMPANY) '개수'
    fROM
    ES_NEWS_DATA
    WHERE
    TRD_DT >= '#{START_DT}' ORDER BY COMPANY,TRD_DT
    """
    
    sql3 = sql3.replace('#{START_DT}', pweek) 
    
    sql4="""
    SELECT TRD_DT,COMPANY,SUM(CNT) OVER (PARTITION BY COMPANY ORDER BY TRD_DT) '누적개수' FROM (SELECT DISTINCT CONVERT(VARCHAR(20),CONVERT(datetime,trd_dt,1),120) TRD_DT,
    COMPANY,
    COUNT(TITLE) OVER (PARTITION BY TRD_DT,
    COMPANY) CNT
    fROM
    ES_NEWS_DATA
    WHERE
    TRD_DT BETWEEN '#{START_DT}' AND '#{END_DT}') A ORDER BY TRD_DT ASC,COMPANY asc
    """
    
    sql4 = sql4.replace('#{START_DT}', start) 
    sql4 = sql4.replace('#{END_DT}', end) 
    
    
    conn=DB.conn()

    data=DB.read(sql,conn)
    data2=DB.read(sql2,conn)
    data3=DB.read(sql3,conn)
    data4=DB.read(sql4,conn)
    
    daily=pd.pivot(data=data, index='TRD_DT', values='개수',columns='COMPANY')
    daily=daily.fillna(0)
    daily=daily.sort_values(by='TRD_DT',ascending=False)
    

    fig_daily=px.line(data4,x="TRD_DT",y='누적개수',color="COMPANY",title="뉴스" )
    fig_daily.update_layout(title='누적개수')
    
    fig=px.line(data,x="TRD_DT",y="개수",color="COMPANY",title="뉴스" )
    fig.update_layout(title='전체')
    
    fig_7=px.line(data3,x="TRD_DT",y="개수",color="COMPANY",title="뉴스" )
    fig_7.update_layout(title='최근1주일')
    
    conn.close()
    
    return fig,data2,fig_7,daily,fig_daily
 
