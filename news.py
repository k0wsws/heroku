# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:47:20 2023

@author: user
"""
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import date,timedelta,datetime
from PIL import Image
import pickle

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
#now = now.strftime('%Y-%m-%d')
pweek = pweek.strftime('%Y-%m-%d')
#pmonth = pmonth.strftime('%Y-%m-%d')

root=''

def news(trd_dt=now):
    
    col1, col2 = st.columns( [0.8, 0.2])
    
    with col1:   
       
        start = st.date_input(
            "시작일",pmonth)
        #start=str(start).replace("-", "")[0:8]  
        end = st.date_input(
            "기준일",now)
        #end=str(end).replace("-", "")[0:8]
    with col2:               # To display brand log
            st.image(logo, width=200 )
               


    sql=pickle.load( open(root+'news1.pkl', 'rb')) 
    data=sql[(sql['TRD_DT']>=start)& (sql['TRD_DT']<=end)]


    sql2=pickle.load( open(root+'news2.pkl', 'rb')) 
    data2=sql2[(sql2['TRD_DT']>=start)& (sql2['TRD_DT']<=end)]
    
    data3 = sql[sql['TRD_DT']>=pweek]
    
    data4=sql.sort_values(by='TRD_DT')
    data4['누적개수']= data4.groupby(['COMPANY'])['개수'].cumsum()
    
    
    daily=pd.pivot(data=data, index='TRD_DT', values='개수',columns='COMPANY')
    daily=daily.fillna(0)
    daily=daily.sort_values(by='TRD_DT',ascending=False)
    

    fig_daily=px.line(data4,x="TRD_DT",y='누적개수',color="COMPANY",title="뉴스" )
    fig_daily.update_layout(title='누적개수')
    
    fig=px.line(data,x="TRD_DT",y="개수",color="COMPANY",title="뉴스" )
    fig.update_layout(title='전체')
    
    fig_7=px.line(data3,x="TRD_DT",y="개수",color="COMPANY",title="뉴스" )
    fig_7.update_layout(title='최근1주일')
    
 
    return fig,data2,fig_7,daily,fig_daily
 
