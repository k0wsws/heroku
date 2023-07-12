# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:52:34 2023

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
import numpy as np
import plotly.express as px
#import load as ld
logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
root=''
aum1=pickle.load(open(root+'aum1.pkl','rb'))   
investor=pickle.load(open(root+'investor.pkl','rb'))   
overview=pickle.load( open(root+'overview.pkl', 'rb')) 
etf_map=pickle.load( open(root+'etf_map.pkl', 'rb')) 
trd_amt=pickle.load( open(root+'trd_amt.pkl', 'rb')) 
ant_ret=pickle.load(open(root+'ant_ret.pkl','rb'))  
comp_overview=pickle.load( open(root+'comp_overview.pkl', 'rb')) 
#aum1,investor,overview,etf_map,trd_amt,ant_ret2,comp_overview = ld.load_data_p10()
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
        comp_ov=comp_overview[comp_overview['CO_NM']==option1]
        ant_ret=ant_ret2[ant_ret2['CO_NM']==option1]
        
        ##성과분석차트
        chart=comp_ov[(comp_ov['TR_YMD']>=start)& (comp_ov['TR_YMD']<=end)]
        chart=chart.sort_values(by='TR_YMD')
        chart['순자산']=chart['순자산']/100000000
        chart.rename(columns={'순자산':'순자산(억)'},inplace=True)
        chart.rename(columns={'매출액(억원)':'매출액(억)'},inplace=True)
        #chart=pd.merge(left = chart , right = chart.groupby('CO_NM')['매출액(억원)'].agg('first').reset_index(), how = "left", on = ["CO_NM"])
        #chart['매출액(억원)']=chart['매출액(억원)_x']*1000/chart['매출액(억원)_y']
        chart['TR_YMD'] = pd.to_datetime(chart['TR_YMD'], format='%Y%m%d')
        chart['TR_YMD'] = chart['TR_YMD'].dt.strftime('%Y-%m-%d')
        chart=chart.sort_values(by='TR_YMD')
        fig_daily=px.line(chart,x="TR_YMD",y='매출액(억)',title="매출액추이" ,width=450)
        fig_daily.update_layout(title='매출액추이')
        fig_daily2=px.line(chart,x="TR_YMD",y='순자산(억)',title="순자산추이" ,width=450)
        fig_daily2.update_layout(title='순자산추이')
        col11, col22, col33 = st.columns( [0.2, 0.2,0.2])
        
        with col11:
            st.plotly_chart(fig_daily2, theme="streamlit", use_conatiner_width=True)
        with col22:
            st.plotly_chart(fig_daily, theme="streamlit", use_conatiner_width=True)
        
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

        ant=ant_ret[(ant_ret['TR_YMD']>=start)&(ant_ret['TR_YMD']<=end)]
        #ant=ant_ret[(ant_ret['TR_YMD']>='20230101')&(ant_ret['TR_YMD']<='20230301')]
        ant_df=pd.DataFrame()
        ant_df['NET_SUM']=ant.groupby(['ETF_CD']).NET_AMT.apply(lambda x: np.sum(np.abs(x)/2))

        ant_df=pd.merge(left=ant_df,right=ant.groupby(['ETF_CD'])['AUM'].mean(), how="inner",on=['ETF_CD'])
        ant_df=pd.merge(left=ant_df,right=ant_ret[ant_ret['TR_YMD']==end], how="inner",on=['ETF_CD'])
        ant_df=pd.merge(left=ant_df,right=ant_ret.groupby('ETF_CD')['CLS_PRC'].agg('first'), how="inner",on=['ETF_CD'])
        ant_df['개인잔고(억)']=round(ant_df['CNT']*ant_df['CLS_PRC_x']/100000000,2)
        
        ant_df=ant_df.drop('ETF_NM',axis=1)
        ant_df=ant_df.drop('TR_YMD',axis=1)
        
        ant_df2=ant
        ant_df2['개인잔고(억)']=round(ant_df2['CNT']*ant_df2['CLS_PRC']/100000000,2)
        ant_df2=ant_df2.groupby(['TR_YMD']).sum('개인잔고(억)').reset_index()
        
        ant_df2['TR_YMD'] = pd.to_datetime(ant_df2['TR_YMD'], format='%Y%m%d')
        ant_df2['TR_YMD'] = ant_df2['TR_YMD'].dt.strftime('%Y-%m-%d')
        ant_df2=ant_df2.sort_values(by='TR_YMD')
        fig_daily3=px.line(ant_df2,x="TR_YMD",y='개인잔고(억)',title="개인잔고추이",width=450 )
        fig_daily3.update_layout(title='개인잔고추이')

        with col33:
            st.plotly_chart(fig_daily3, theme="streamlit", use_conatiner_width=True)
        
        ace_overview=pd.merge(left = ace_overview , right = ant_df, how = "left", on = ['ETF_CD'])

        
        ace_overview=pd.merge(left = ace_overview , right = ant_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = ins_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = bnk_ace, how = "left", on = ['ETF_NM'])
        ace_overview=pd.merge(left = ace_overview , right = aum_chg_ace, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right = set_ace, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right = aum_chg_amt, how = "left", on = ["ETF_NM","ETF_CD"])
        ace_overview=pd.merge(left = ace_overview , right =  ace_trd_amt, how = "left", on = ["ETF_NM","ETF_CD","TR_YMD"])
        ace_overview=ace_overview.sort_values(by=['ETF_NM'],axis=0,ascending=True)
        ace_overview.rename(columns={'SET_DT':'설정일'},inplace=True)
        
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
        gb['pinnedBottomRowData'] = [{'구분(소)':'합계','ΔAUM':ace_overview['ΔAUM'].sum(),'Δ설정액(억)':ace_overview['Δ설정액(억)'].sum(),'AUM(억원)':ace_overview['AUM(억원)'].sum(),'매출액(억원)':ace_overview['매출액(억원)'].sum(),'개인(억)':ace_overview['개인(억)'].sum(),'보험(억)':ace_overview['보험(억)'].sum(),'은행(억)':ace_overview['은행(억)'].sum(),'font-weight': 'bold','개인잔고(억)':ace_overview['개인잔고(억)'].sum(),'font-weight': 'bold'}]
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': 'ETF_NM'},{ 'field': '자산군','width':70},  { 'field': '시장(소)','width':90},{ 'field': '구분(중)','width':90,'background-color': '#1b6d85 !important' }, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': 'ETF','headerClass': 'all', 'children': [{'field': 'ΔAUM','width':70,'valueFormatter':"x.toLocaleString()","cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '설정일','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'AUM(억원)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ거래대금(억)','width':105,'valueFormatter':"x.toLocaleString()"},{'field': '거래대금(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '거래량','width':80,'valueFormatter':"x.toLocaleString()"},{'field': '보수','width':70},{'field': '매출액(억원)' ,'width':100,'valueFormatter':"x.toLocaleString()"},{'field': '개인(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '보험(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '은행(억)','width':90 ,'valueFormatter':"x.toLocaleString()"},{'field': '개인잔고(억)','width':130 ,'valueFormatter':"x.toLocaleString()"}] }, ] 
              
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(ace_overview, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)
