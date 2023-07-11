# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 14:58:06 2023

@author: user
"""
import streamlit as st
import fig_kor_2 as fp
import fig_glo_2 as fg
import streamlit as st
import DB
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
import pandas as pd
from pday import Pday
import kmean_all as km
conn=DB.conn()

from PIL import Image
logo = Image.open('ace.jpg') 


def generate():
    col_1, col_2 = st.columns( [0.8, 0.2])
    with col_1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Investor</p>', unsafe_allow_html=True)    
    with col_2:               # To display brand log
        st.image(logo, width=200 )
    option = st.selectbox("선택", ("비교","ACE", "KODEX", "TIGER","KBSTAR","SOL"),key=1)
    col111, col222= st.columns( [0.2, 0.2])
     
    with col111:          
        start = st.date_input(
            "기초일",
            date(2023, 1, 2))
    with col222:          
        end = st.date_input(
            "기말일",
            Pday())
    
    start=str(start)[0:10]
    end=str(end)[0:10]
    
    if option=='비교':
        

        ace = """
         SELECT ETF_NM NM fROM FN_ETFDATA WHERE TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) AND ETF_CD IN (SELECT STk_CD FROM ES_fUND_MAP)
         """
        ace=DB.read(ace,conn)  

        all1 = """
        SELECT * FROM (SELECT '없음' NM
   UNION
    SELECT ETF_NM NM fROM FN_ETFDATA WHERE TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE())) A order BY (case when NM = '없음' THEN 0 
    																			WHEN NM LIKE 'KODEX%' THEN 1 ELSE 2 END) 
         """
        all1=DB.read(all1,conn)   
        

        

        
        col1, col2, col3, col4, col5 = st.columns( [0.2, 0.2,0.2,0.2,0.2])

        with col1:          
            st.markdown('비교 1(ACE)', unsafe_allow_html=True)  
            option1 = st.selectbox("", ace['NM'],key=11)
        with col2:   
            st.markdown('비교 2', unsafe_allow_html=True)  
            option2 = st.selectbox("", all1['NM'],key=12)
        with col3:   
            st.markdown('비교 3', unsafe_allow_html=True)  
            option3 = st.selectbox("", all1['NM'],key=13)
        with col4:    
            st.markdown('비교 4', unsafe_allow_html=True)  
            option4 = st.selectbox("", all1['NM'],key=14)
        with col5:   
            st.markdown('비교 5', unsafe_allow_html=True)  
            option5 = st.selectbox("", all1['NM'],key=15)
            
        col11, col22, col33 = st.columns( [0.2, 0.2,0.2])
        
        with col11:          
            st.plotly_chart(fp.fig_all.ant(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col22:          
            st.plotly_chart(fp.fig_all.alien(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col33:          
            st.plotly_chart(fp.fig_all.corp(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
 
        col111, col222, col333 = st.columns( [0.2, 0.2,0.2])
        
        with col111:          
            st.plotly_chart(fp.fig_all.bk(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col222:          
            st.plotly_chart(fp.fig_all.invt(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col333:          
            st.plotly_chart(fp.fig_all.trust(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
            
        col1111, col2222, col3333 = st.columns( [0.2, 0.2,0.2])
        
        with col1111:          
            st.plotly_chart(fp.fig_all.pens(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col2222:          
            st.plotly_chart(fp.fig_all.pef(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
        with col3333:          
            st.plotly_chart(fp.fig_all.finv(option1,option2,option3,option4,option5,start,end), theme="streamlit", use_conatiner_width=True)
            
        
    
    if option=='ACE':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fp.fig_ace.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fp.fig_ace.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fp.fig_ace.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_ace.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_ace.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fp.fig_ace.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_ace.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fp.fig_ace.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_ace.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_ace.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            
        

        with tab2:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fg.fig_ace.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fg.fig_ace.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fg.fig_ace.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_ace.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_ace.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fg.fig_ace.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_ace.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fg.fig_ace.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_ace.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_ace.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            
        
     
    if option=='KODEX':
        
        tab1, tab2 = st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fp.fig_kodex.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fp.fig_kodex.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fp.fig_kodex.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_kodex.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_kodex.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fp.fig_kodex.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kodex.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fp.fig_kodex.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kodex.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kodex.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
        with tab2:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fg.fig_kodex.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fg.fig_kodex.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fg.fig_kodex.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_kodex.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_kodex.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fg.fig_kodex.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kodex.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fg.fig_kodex.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kodex.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kodex.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            
    if option=='TIGER':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fp.fig_tiger.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fp.fig_tiger.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fp.fig_tiger.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_tiger.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_tiger.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fp.fig_tiger.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_tiger.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fp.fig_tiger.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_tiger.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_tiger.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
        with tab2:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fg.fig_tiger.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fg.fig_tiger.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fg.fig_tiger.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_tiger.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_tiger.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fg.fig_tiger.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_tiger.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fg.fig_tiger.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_tiger.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_tiger.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            
    
    if option=='KBSTAR':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fp.fig_kbstar.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fp.fig_kbstar.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fp.fig_kbstar.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_kbstar.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_kbstar.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fp.fig_kbstar.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kbstar.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fp.fig_kbstar.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kbstar.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_kbstar.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
         
        with tab2:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fg.fig_kbstar.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fg.fig_kbstar.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fg.fig_kbstar.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_kbstar.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_kbstar.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fg.fig_kbstar.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kbstar.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fg.fig_kbstar.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kbstar.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_kbstar.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            
    
    if option=='SOL':
        
        tab1, tab2= st.tabs(["국내(1)", "해외(1)"])
        with tab1:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fp.fig_sol.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fp.fig_sol.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fp.fig_sol.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_sol.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fp.fig_sol.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fp.fig_sol.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_sol.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fp.fig_sol.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_sol.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fp.fig_sol.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
         
        with tab2:
            col3, col4, col5,edge2 = st.columns( [0.4, 0.1,0.4,0.1])
            with col3:    
                

                st.plotly_chart(fg.fig_sol.ant(start,end)[0], theme="streamlit", use_conatiner_width=True) 
                st.plotly_chart(fg.fig_sol.finv(start,end)[0], theme="streamlit", use_conatiner_width=True)    
                st.plotly_chart(fg.fig_sol.bk(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_sol.invt(start,end)[0], theme="streamlit", use_conatiner_width=True)
                st.plotly_chart(fg.fig_sol.alien(start,end)[0], theme="streamlit", use_conatiner_width=True)     
            with col5:               # To display brand log

                 st.plotly_chart(fg.fig_sol.ant(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_sol.finv(start,end)[1], theme="streamlit", use_conatiner_width=True)   
                 st.plotly_chart(fg.fig_sol.bk(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_sol.invt(start,end)[1], theme="streamlit", use_conatiner_width=True)
                 st.plotly_chart(fg.fig_sol.alien(start,end)[1], theme="streamlit", use_conatiner_width=True)
         
            