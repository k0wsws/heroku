# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:46:18 2023

@author: user
"""

import streamlit as st
#import DB_ETF as DB
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle
import re
import plotly.express as px

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(200)
#conn=DB.conn()
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
            maxend)
        end=str(end).replace("-", "")[0:8]
        return end
        

############################## 국내주식    ###########################

    def kor_stk(self):
        
        ##데이터 불러오기
       
        start=max(fund_asset[fund_asset['TRD_DT']<=start_t]['TRD_DT'])
        start_net=min(fund_asset[fund_asset['TRD_DT']>=start_t]['TRD_DT'])
        end=max(fund_asset[fund_asset['TRD_DT']<=end_t]['TRD_DT'])
        
        name=['ACE','타사']
        page=st.radio('',name,index=0)
        

        ace=pickle.load(open(root+'ace.pkl','rb'))

        ex_ace=pickle.load(open(root+'ex_ace.pkl','rb')) 
        
    
        col1, col2, col3, col4, col5 = st.columns( [0.2, 0.2,0.2,0.2,0.2])
        if page=='ACE':
            
            with col1:          
                option1 = st.selectbox("펀드명", ace['NM'],key=11)
            
        elif page=='타사':
            with col1:          
                option1 = st.selectbox("펀드명", ex_ace['NM'],key=12)
        
        overview=fund_asset[fund_asset['FUND_NM']==option1]
    
        ##경쟁군맵핑
       # overview=fund_asset[fund_asset['FUND_NM']==option1]
        
        
        ##성과분석차트
        #chart=overview[(overview['TRD_DT']>=start)& (overview['TRD_DT']<=end)]
        #chart=chart.sort_values(by='TRD_DT')
        #chart=pd.merge(left = chart , right = chart.groupby('ETF_CD')['NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        #chart=pd.merge(left = chart , right = chart.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        #chart['기준가']=chart['NAV_x']*1000/chart['NAV_y']
        #chart['순자산']=chart['AUM_x']*1000/chart['AUM_y']
        #chart['설정액(억)']=chart.groupby('ETF_CD')['설정액'].cumsum()
        #chart['TR_YMD'] = pd.to_datetime(chart['TR_YMD'], format='%Y%m%d')
        #chart['TR_YMD'] = chart['TR_YMD'].dt.strftime('%Y-%m-%d')
        #chart=chart.sort_values(by='TR_YMD')
        #fig_daily=px.line(chart,x="TR_YMD",y='기준가',color="ETF_NM",title="성과비교차트" )
        #fig_daily.update_layout(title='성과비교차트')
        #fig_daily2=px.line(chart,x="TR_YMD",y='순자산',color="ETF_NM",title="성과비교차트2" )
        #fig_daily2.update_layout(title='AUM추이')
        #fig_daily3=px.line(chart,x="TR_YMD",y='설정액(억)',color="ETF_NM",title="설정액차트" )
        #fig_daily3.update_layout(title='설정액추이')
        
        overivew_f=pd.merge(left=overview[overview['TRD_DT']==start],right=overview[overview['TRD_DT']==end], how = "right", on = ["STK_CD","FUND_FNM"])     
        overivew_f['Δ평가액']=round(overivew_f['EVAL_PRC_y']-overivew_f['EVAL_PRC_x'].fillna(0),0)      
        overivew_f['Δ주수']=round(overivew_f['STK_CNT_y']-overivew_f['STK_CNT_x'].fillna(0),0)  
        overivew_f.rename(columns={'FUND_NM_y':'ETF_NM'},inplace=True)
        overivew_f.rename(columns={'FUND_RT_y':'펀드내 비중'},inplace=True)
        overivew_f.rename(columns={'STK_CNT_y':'주수'},inplace=True)
        overivew_f.rename(columns={'EVAL_PRC_y':'평가액'},inplace=True)

    
        overivew_f=overivew_f.sort_values(by=['ETF_NM'],axis=0,ascending=True)
  
        
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(overivew_f,min_column_width=30)
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
        
        value3=JsCode("""function(params) {
        if (params.value > 0){
         return (params.value.toLocaleString()+'%')}
        if (params.value == 0){
         return '0'+'%'}
        if (params.value < 0){
         return params.value.toLocaleString()+'%'}
                };""")  
        
        #jscode = jscode.replace("#{length}", str(len(df_main)-1)) 
        

        jscode = JsCode(jscode)
       
        gb = gridOptions.build()
        gb['pinnedBottomRowData'] = [{'FUND_FNM':'전체(합계)','평가액':overivew_f['평가액'].sum(),'주수':overivew_f['주수'].sum(),'Δ주수':overivew_f['주수'].sum()}]
    

        
        gb['getRowStyle'] = jscode
        #gb['pinnedBottomRowData'] = [{'구분(소)':'합계','ΔAUM':ace_overview['ΔAUM'].sum(),'Δ설정액(억)':ace_overview['Δ설정액(억)'].sum(),'AUM(억원)':ace_overview['AUM(억원)'].sum(),'매출액(억원)':ace_overview['매출액(억원)'].sum(),'개인(억)':ace_overview['개인(억)'].sum(),'보험(억)':ace_overview['보험(억)'].sum(),'은행(억)':ace_overview['은행(억)'].sum(),'font-weight': 'bold'}]
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': 'ETF_NM'},{ 'field': 'FUND_FNM','width':500}  ] }, 
                             { 'headerName': 'ACEETF','headerClass': 'ace', 'children': [{'field': 'Δ평가액','width':120,'valueFormatter':"x.toLocaleString()","cellStyle": {'border-left': 'solid black'}},{'field': '평가액','width':120,'valueFormatter':"x.toLocaleString()"},{'field': '펀드내 비중','width':120,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ주수','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '주수','width':100,'valueFormatter':"x.toLocaleString()"}] }, ] 
        
   
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(overivew_f, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)
        col11, col22,col33 = st.columns( [0.5,0.1,0.4])
        col15, col25,col35 = st.columns( [0.5,0.1,0.4])
       
      #  with col11:
           # st.plotly_chart(fig_daily, theme="streamlit", use_conatiner_width=True)
     #       with col15:
                #st.plotly_chart(fig_daily2, theme="streamlit", use_conatiner_width=True)
      #      with col35:
                #st.plotly_chart(fig_daily3, theme="streamlit", use_conatiner_width=True)        
