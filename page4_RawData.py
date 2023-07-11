# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:07:53 2023

@author: user
"""
import streamlit as st
import pandas as pd
import Data as dt
import io
from datetime import date,timedelta,datetime
from PIL import Image
from pday import Pday
import pickle

logo = Image.open('ace.jpg') 
buffer = io.BytesIO()
root='C:\\Users\\user\\Dashboard\\dataset\\'


def generate():
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Raw Data</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=200 )
        
    option2 = st.selectbox("", ("선택","MASTER","NAV","펀드 기준가","BM","FX"),key=3)
    
    if option2 =="NAV":
        
        #st.dataframe(dt.etf_nav())
        df=dt.etf_nav()
        df=df.reset_index()
        
        start = st.date_input(
            "시작일",
            date(2018, 1, 3))
        
        end = st.date_input(
            "종료일",
            Pday())
        start=str(start).replace("-", "")[0:8]
        end=str(end).replace("-", "")[0:8]
        
        df2=df[df[df["TRD_DT"]==start].index[0]:df[df["TRD_DT"]==end].index[0]+1]
        df2.set_index("TRD_DT",inplace=True)
        st.dataframe(df2)
        
        down=df2.to_csv().encode('utf-8')
        
            # Close the Pandas Excel writer and output the Excel file to the buffer

        
        st.download_button(
          label='📥 CSV로 저장',
          data=down,
          file_name="data.csv"
    )
    
        
        
    elif option2 =="펀드 기준가":
               
        df=dt.fund_prc()
        df=df.reset_index()
        
        start = st.date_input(
            "시작일",
            date(2018, 1, 3))
        
        end = st.date_input(
            "종료일",
            Pday())
        start=str(start).replace("-", "")[0:8]
        end=str(end).replace("-", "")[0:8]
        
        df2=df[df[df["TRD_DT"]==start].index[0]:df[df["TRD_DT"]==end].index[0]+1]
        df2.set_index("TRD_DT",inplace=True)
        st.dataframe(df2)
        
        down=df2.to_csv().encode('utf-8')
        
            # Close the Pandas Excel writer and output the Excel file to the buffer

        
        st.download_button(
          label='📥 CSV로 저장',
          data=down,
          file_name="data.csv"
    )
    elif option2 =="BM":
        
        df=dt.BM()
        df=df.reset_index()
        
        start = st.date_input(
            "시작일",
            date(2020, 1, 3))
        
        end = st.date_input(
            "종료일",
            Pday())
        start=str(start).replace("-", "")[0:8]
        end=str(end).replace("-", "")[0:8]
        
        df2=df[df[df["TRD_DT"]==start].index[0]:df[df["TRD_DT"]==end].index[0]+1]
        df2.set_index("TRD_DT",inplace=True)
        st.dataframe(df2)
        
        down=df2.to_csv().encode('utf-8')
        
            # Close the Pandas Excel writer and output the Excel file to the buffer

        
        st.download_button(
          label='📥 CSV로 저장',
          data=down,
          file_name="data.csv"
    )
        
    elif option2 =="FX":
        
        df=dt.FX()
        df=df.reset_index()
        
        start = st.date_input(
            "시작일",
            date(2021, 1, 4))
        
        end = st.date_input(
            "종료일",
            Pday())
        start=str(start).replace("-", "")[0:8]
        end=str(end).replace("-", "")[0:8]
        
        df2=df[df[df["TRD_DT"]==start].index[0]:df[df["TRD_DT"]==end].index[0]+1]
        df2.set_index("TRD_DT",inplace=True)
        st.dataframe(df2)
        

        down=df2.to_csv().encode('utf-8')
        
            # Close the Pandas Excel writer and output the Excel file to the buffer

        
        st.download_button(
          label='📥 CSV로 저장',
          data=down,
          file_name="data.csv"
    )
        
    elif option2 =="MASTER":
            
        df=pickle.load(open(root+'master.pkl','rb'))    
        
        start = st.date_input(
            "시작일",
            date(2021, 1, 4))
        
        end = st.date_input(
            "종료일",
            Pday())
        start=str(start).replace("-", "")[0:8]
        end=str(end).replace("-", "")[0:8]
        
        df2=df[df[df["TR_YMD"]==start].index[0]:df[df["TR_YMD"]==end].index[0]+1]
        df2.set_index("TR_YMD",inplace=True)
        st.dataframe(df2)
        

        down=df2.to_csv().encode('utf-8')
        
            # Close the Pandas Excel writer and output the Excel file to the buffer

        
        st.download_button(
          label='📥 CSV로 저장',
          data=down,
          file_name="data.csv"
        )