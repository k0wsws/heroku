# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:26:04 2023

@author: user
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:16:29 2023

@author: user
"""

from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder,ColumnsAutoSizeMode
from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle

root=''
logo = Image.open('ace.jpg') 
#dong = Image.open('thumb.png') 
ACEETF = Image.open(root+'ACEETF.jpg') 
ETF = Image.open(root+'ETF.jpg') 
ECO = Image.open(root+'ECO.jpg') 

now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)

df_word_ace=pd.read_pickle(root+'df_word_ace.pkl')
df_wordcount=pd.read_pickle(root+'df_word_count.pkl') #pickle.load(open(root+'df_word_count.pkl','rb'))    
df_word_eco=pd.read_pickle(root+'df_word_eco.pkl') #pickle.load(open(root+'df_word_eco.pkl','rb'))   

df_etf=pd.read_pickle(root+'news_df_etf.pkl') #pickle.load(open(root+'news_df_etf.pkl','rb'))  
df_ace=pd.read_pickle(root+'news_df_ace.pkl') #pickle.load(open(root+'news_df_ace.pkl','rb'))  
df_eco=pd.read_pickle(root+'news_df_eco.pkl') #pickle.load(open(root+'news_df_eco.pkl','rb'))  

cds = ColumnDataSource(df_etf)
columns = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">🔗</a>')),
]
p = DataTable(source=cds, columns=columns, fit_columns=False, css_classes=["my_table"])

cds2 = ColumnDataSource(df_ace)
columns2 = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">🔗</a>')),
]
p2 = DataTable(source=cds2, columns=columns2, fit_columns=False, css_classes=["my_table"])

cds3 = ColumnDataSource(df_eco)
columns3 = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">🔗</a>')),
]
p3 = DataTable(source=cds3, columns=columns3, fit_columns=False, css_classes=["my_table"])

df_word_ace['순위'] = df_word_ace['value'].rank(method='min',ascending=False)    
df_word_ace=df_word_ace.head(10) 
df_word_ace['순위']=df_word_ace['순위'].astype('int')
df_word_ace=df_word_ace.set_index('순위')
df_word_ace.rename(columns={'value':'개수'},inplace=True)

df_wordcount['순위'] = df_wordcount['value'].rank(method='min',ascending=False) 
df_wordcount=df_wordcount.head(10)   
df_wordcount['순위']=df_wordcount['순위'].astype('int')
df_wordcount=df_wordcount.set_index('순위')
df_wordcount.rename(columns={'value':'개수'},inplace=True)

df_word_eco['순위'] = df_word_eco['value'].rank(method='min',ascending=False)    
df_word_eco=df_word_eco.head(10) 
df_word_eco['순위']=df_word_eco['순위'].astype('int') 
df_word_eco=df_word_eco.set_index('순위')
df_word_eco.rename(columns={'value':'개수'},inplace=True)

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
aum1=pickle.load(open('aum1.pkl','rb'))  #pd.read_pickle(root+'aum1.pkl') 
#investor=pd.read_pickle(root+'news_df_eco.pkl') #pickle.load(open('investor.pkl','rb'))   
overview=pd.read_pickle(root+'overview.pkl') #pickle.load( open('overview.pkl', 'rb')) 
#etf_map=pd.read_pickle(root+'etf_map.pkl') #pickle.load( open('etf_map.pkl', 'rb')) 
#trd_amt=pd.read_pickle(root+'trd_amt.pkl') #pickle.load( open('trd_amt.pkl', 'rb')) 

with st.sidebar:
    choose = option_menu("ACE DashBoard", ["ACE","OVERVIEW","회사별 현황","경쟁상품비교","INVESTOR","회사별 Overview","NEWS", "Cluster","시장점유율","DATA","chat"],
                         icons=['info-circle','view-stacked','briefcase','shop','bank','bar-chart','newspaper', 'collection', 'pie-chart','download','chat-dots'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "ACE":

        st.image(logo )
        st.write("“키워드로 검색한 뉴스내용에서 많이 언급되고 있는 단어”")
        with open(root+"last_updated_wc.txt", "r") as file:
                file_contents = file.read()
                st.write("Last updated: "+file_contents)                    
        col1, col2, col3, col4 = st.columns( [0.3, 0.3,0.3,0.1])
        with col1:  
            st.image(ACEETF)
            st.table(df_word_ace)
            st.bokeh_chart(p2)
        with col2:
            st.image(ETF)
            st.table(df_wordcount)
            st.bokeh_chart(p)

        with col3:
            st.image(ECO)
            st.table(df_word_eco)
            st.bokeh_chart(p3)
            
        #btn_clicked = st.button("Click")
        #st.write(btn_clicked)
        #if btn_clicked:
        #    col1, col2 = st.columns( [0.5, 0.5])
        #    with col1:  
        #        st.image(cookie)
        #    with col2:  
        #        st.image(bed)
 

