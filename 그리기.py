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
dong = Image.open('thumb.png') 
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
aum1=pd.read_pickle(root+'aum1.pkl') #pickle.load(open('aum1.pkl','rb'))   
#investor=pd.read_pickle(root+'news_df_eco.pkl') #pickle.load(open('investor.pkl','rb'))   
overview=pd.read_pickle(root+'overview.pkl') #pickle.load( open('overview.pkl', 'rb')) 
etf_map=pd.read_pickle(root+'etf_map.pkl') #pickle.load( open('etf_map.pkl', 'rb')) 
trd_amt=pd.read_pickle(root+'trd_amt.pkl') #pickle.load( open('trd_amt.pkl', 'rb')) 
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
        start=str(start).replace("-", "")[0:8]
        
        return start
        

    def end_dt(self):
        end = st.date_input(
            "기말일",
            Pday())
        end=str(end).replace("-", "")[0:8]
        return end
        

############################## 국내주식    ###########################

    def kor_stk(self):
        ##데이터 불러오기
        
   
        col1, col2, col3, col4, col5 = st.columns( [0.2, 0.2,0.2,0.2,0.2])
    
        with col1:          
            option1 = st.selectbox("회사명", ["한국투자신탁운용","삼성자산운용","미래에셋자산운용","케이비자산운용","신한자산운용","키움투자자산운용","한화자산운용","엔에이치아문디자산운용"],key=11)
        
        start=max(overview[overview['TR_YMD']<=start_t]['TR_YMD'])
        start_net=min(overview[overview['TR_YMD']>=start_t]['TR_YMD'])
        end=max(overview[overview['TR_YMD']<=end_t]['TR_YMD'])
        
        aum_ace_raw=aum1[aum1['CO_NM']==option1]
        ace_overview=overview[overview['CO_NM']==option1]
        investor_ace=investor[investor['CO_NM']==option1]

        ace_overview=pd.merge(left = ace_overview[ace_overview['TR_YMD']==end] , right = etf_map, how = "left", on = ["ETF_CD"])
        
        
        ##개인순매수 상위
        ant_ace=investor_ace[(investor_ace['INVEST_GB']==8)& (investor_ace['TR_YMD']>=start_net)& (investor_ace['TR_YMD']<=end)]
        ant_ace=ant_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
        ant_ace.rename(columns={'NET_AMT':'개인(억)'},inplace=True)

        
        ##보험순매수 상위
        ins_ace=investor_ace[(investor_ace['INVEST_GB']==2)& (investor_ace['TR_YMD']>=start_net)& (investor_ace['TR_YMD']<=end)]
        ins_ace=ins_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
        ins_ace.rename(columns={'NET_AMT':'보험(억)'},inplace=True)

        
        ##은행순매수 상위
        bnk_ace=investor_ace[(investor_ace['INVEST_GB']==4)& (investor_ace['TR_YMD']>=start_net)& (investor_ace['TR_YMD']<=end)]
        bnk_ace=bnk_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
        bnk_ace.rename(columns={'NET_AMT':'은행(억)'},inplace=True)
        
        ##ACE 순자산증감 상위
        aum_chg_ace=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
        aum_chg_ace['ΔAUM']=round(aum_chg_ace['AUM_y']-aum_chg_ace['AUM_x'].fillna(0),2)
        aum_chg_ace.rename(columns={'ETF_NM_y':'ETF_NM'},inplace=True)
        
        ##ACE 거래량 상위
        aum_chg_amt=pd.merge(left = trd_amt[trd_amt['TR_YMD']==start] , right = trd_amt[trd_amt['TR_YMD']==end], how = "right", on = ["ETF_CD"])
        aum_chg_amt['Δ거래대금(억)']=round(aum_chg_amt['거래대금(억)_y']-aum_chg_amt['거래대금(억)_x'].fillna(0),2)
        aum_chg_amt.rename(columns={'ETF_NM_y':'ETF_NM'},inplace=True)

        ##ACE 거래량 상위
       
        ace_trd_amt=trd_amt[trd_amt['TR_YMD']==end]

        
        ##설정액 상위
        set_ace=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
        set_ace=pd.merge(left = set_ace , right = aum_ace_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        set_ace=pd.merge(left = set_ace , right = aum_ace_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
  
        set_ace['Δ설정액(억)']=round(set_ace['AUM_y']-set_ace['AUM_x'].fillna(set_ace['AUM'])*set_ace['ETF_NAV_y']/set_ace['ETF_NAV_x'].fillna(set_ace['ETF_NAV']),2)
        set_ace.rename(columns={'ETF_NM_y':'ETF_NM'},inplace=True)



        
        ace_overview=pd.merge(left = ace_overview , right = ant_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = ins_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = bnk_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = aum_chg_ace, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right = set_ace, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right = aum_chg_amt, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right =  ace_trd_amt, how = "left", on = ["ETF_NM","ETF_CD","TR_YMD"])
        ace_overview=ace_overview.sort_values(by=['ETF_NM'],axis=0,ascending=True)
  
        
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(ace_overview,min_column_width=30)
        gridOptions.configure_side_bar()
        
        #jscode="""
        #function(params) {
        #    if (params.node.rowIndex  === parseFloat("#{length}")) {
        #        return {
        #            'color': 'black',
        #            'backgroundColor': 'white',
        #            'font-weight': 'bold'
        #        }
        #    }
        #};
        #"""
        
        jscode="""
        function(params) {

            if (params.node.rowPinned === 'bottom') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
              }
            };
        """
        
        #jscode = jscode.replace("#{length}", str(len(df_main)-1)) 
        

        jscode = JsCode(jscode)
       
        gb = gridOptions.build()

        
        gb['getRowStyle'] = jscode
        gb['pinnedBottomRowData'] = [{'구분(소)':'합계','ΔAUM':ace_overview['ΔAUM'].sum(),'Δ설정액(억)':ace_overview['Δ설정액(억)'].sum(),'AUM(억원)':ace_overview['AUM(억원)'].sum(),'매출액(억원)':ace_overview['매출액(억원)'].sum(),'개인(억)':ace_overview['개인(억)'].sum(),'보험(억)':ace_overview['보험(억)'].sum(),'은행(억)':ace_overview['은행(억)'].sum(),'font-weight': 'bold'}]
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': 'ETF_NM'},{ 'field': '자산군','width':70},  { 'field': '시장(소)','width':90},{ 'field': '구분(중)','width':90,'background-color': '#1b6d85 !important' }, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': 'ETF','headerClass': 'all', 'children': [{'field': 'ΔAUM','width':70,'valueFormatter':"x.toLocaleString()","cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'AUM(억원)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ거래대금(억)','width':105,'valueFormatter':"x.toLocaleString()"},{'field': '거래대금(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '거래량','width':80,'valueFormatter':"x.toLocaleString()"},{'field': '보수','width':70},{'field': '매출액(억원)' ,'width':100,'valueFormatter':"x.toLocaleString()"},{'field': '개인(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '보험(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '은행(억)','width':90 ,'valueFormatter':"x.toLocaleString()"}] }, ] 
              
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(ace_overview, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)

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
 
elif choose == "회사별 현황" :
    
    generate()
