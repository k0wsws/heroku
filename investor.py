# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:58:06 2023

@author: user
"""
import streamlit as st
import fig_kor_2 as fp
import fig_glo_2 as fg

from PIL import Image
logo = Image.open('ace.jpg') 

def generate():
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Market purchaser</p>', unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=200 )
    option = st.selectbox("운용사", ("선택","ACE", "KODEX", "TIGER","KBSTAR","SOL"),key=1)
    
    if option=='ACE':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            st.plotly_chart(fp.fig_ace.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_ace.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_ace.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_ace.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_ace.alien(), theme="streamlit", use_conatiner_width=True)
        with tab2:
            st.plotly_chart(fg.fig_ace.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_ace.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_ace.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_ace.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_ace.alien(), theme="streamlit", use_conatiner_width=True)
        
     
    if option=='KODEX':
        
        tab1, tab2 = st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            st.plotly_chart(fp.fig_kodex.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kodex.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kodex.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kodex.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kodex.alien(), theme="streamlit", use_conatiner_width=True)
        with tab2:
            st.plotly_chart(fg.fig_kodex.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kodex.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kodex.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kodex.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kodex.alien(), theme="streamlit", use_conatiner_width=True)
        
    if option=='TIGER':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            st.plotly_chart(fp.fig_tiger.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_tiger.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_tiger.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_tiger.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_tiger.alien(), theme="streamlit", use_conatiner_width=True)
        with tab2:
            st.plotly_chart(fg.fig_tiger.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_tiger.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_tiger.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_tiger.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_tiger.alien(), theme="streamlit", use_conatiner_width=True)
    
    if option=='KBSTAR':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            st.plotly_chart(fp.fig_kbstar.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kbstar.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kbstar.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kbstar.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_kbstar.alien(), theme="streamlit", use_conatiner_width=True)
        with tab2:
            st.plotly_chart(fg.fig_kbstar.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kbstar.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kbstar.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kbstar.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_kbstar.alien(), theme="streamlit", use_conatiner_width=True)
    
    if option=='SOL':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            st.plotly_chart(fp.fig_sol.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_sol.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_sol.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_sol.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fp.fig_sol.alien(), theme="streamlit", use_conatiner_width=True)
        with tab2:
            st.plotly_chart(fg.fig_sol.ant(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_sol.finv(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_sol.bk(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_sol.invt(), theme="streamlit", use_conatiner_width=True)
            st.plotly_chart(fg.fig_sol.alien(), theme="streamlit", use_conatiner_width=True)