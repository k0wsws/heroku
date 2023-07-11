# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:10:32 2023

@author: user
"""
import streamlit as st
from datetime import date,timedelta,datetime
from pandas.tseries.offsets import BDay
from PIL import Image

logo = Image.open('ace.jpg') 
import ms

now = str(date.today()-BDay(1))[0:10]

def generate():
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">MS</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=200 )
        
    date=st.text_input("조회날짜 입력(yyyymmdd):")
    if date=='':
        st.write("기준일: "+now)   
        st.write("전체")   
        st.plotly_chart(ms.msfig(), theme="streamlit", use_conatiner_width=True)
        st.write("국내")   
        st.plotly_chart(ms.msfig_kor(), theme="streamlit", use_conatiner_width=True)
        st.write("해외")   
        st.plotly_chart(ms.msfig_glo(), theme="streamlit", use_conatiner_width=True)
    else:
        st.write("기준일: "+str(datetime.strptime(date,'%Y%m%d'))[0:10])   
        st.write("전체")   
        st.plotly_chart(ms.msfig(date), theme="streamlit", use_conatiner_width=True)
        st.write("국내")  
        st.plotly_chart(ms.msfig_kor(date), theme="streamlit", use_conatiner_width=True)
        st.write("해외")   
        st.plotly_chart(ms.msfig_glo(date), theme="streamlit", use_conatiner_width=True)
        