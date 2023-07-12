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
import load as ld

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
conn=DB.conn()
root=''

master_comp=pickle.load(open(root+'master_comp.pkl','rb'))   
investor=pickle.load(open(root+'investor.pkl','rb'))   
ace_overview=pickle.load( open(root+'ace_overview.pkl', 'rb')) 

#master_comp,investor,ace_overview= ld.load_data_p8()

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
       
        start=max(ace_overview[ace_overview['TR_YMD']<=start_t]['TR_YMD'])
        start_net=min(ace_overview[ace_overview['TR_YMD']>=start_t]['TR_YMD'])
        end=max(ace_overview[ace_overview['TR_YMD']<=end_t]['TR_YMD'])
        

        ace=pickle.load(open(root+'ace.pkl','rb'))          
        comp=pickle.load(open(root+'comp.pkl','rb'))  
    
        col1, col2, col3, col4, col5 = st.columns( [0.2, 0.2,0.2,0.2,0.2])
    
        with col1:          
            option1 = st.selectbox("펀드명", ace['NM'],key=11)
    
        ##경쟁군맵핑
        try:
            comp_list=list(filter(lambda elem: re.match(r'^A\d', elem),list(set(comp[comp['ETF_NM']==option1].values.tolist()[0]))))      
        
            overview=master_comp[master_comp['ETF_CD'].isin(comp_list)]
            
            
            ##성과분석차트
            chart=overview[(overview['TR_YMD']>=start)& (overview['TR_YMD']<=end)]
            chart=chart.sort_values(by='TR_YMD')
            chart=pd.merge(left = chart , right = chart.groupby('ETF_CD')['NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
            chart=pd.merge(left = chart , right = chart.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
            chart['기준가']=chart['NAV_x']*1000/chart['NAV_y']
            chart['순자산']=chart['AUM_x']*1000/chart['AUM_y']
            chart['설정액(억)']=chart.groupby('ETF_CD')['설정액'].cumsum()
            chart['TR_YMD'] = pd.to_datetime(chart['TR_YMD'], format='%Y%m%d')
            chart['TR_YMD'] = chart['TR_YMD'].dt.strftime('%Y-%m-%d')
            chart=chart.sort_values(by='TR_YMD')
            fig_daily=px.line(chart,x="TR_YMD",y='기준가',color="ETF_NM",title="성과비교차트" )
            fig_daily.update_layout(title='성과비교차트')
            fig_daily2=px.line(chart,x="TR_YMD",y='순자산',color="ETF_NM",title="성과비교차트2" )
            fig_daily2.update_layout(title='AUM추이(1000환산기준)')
            fig_daily3=px.line(chart,x="TR_YMD",y='설정액(억)',color="ETF_NM",title="설정액차트" )
            fig_daily3.update_layout(title='설정액추이')
            
            overivew_f=pd.merge(left=overview[overview['TR_YMD']==start],right=overview[overview['TR_YMD']==end], how = "right", on = ["ETF_CD"])     
            overivew_f['ΔAUM']=round(overivew_f['AUM_y']/100000000-overivew_f['AUM_x'].fillna(0)/100000000,0)      
            overivew_f=pd.merge(left = overivew_f , right = overview.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
            overivew_f=pd.merge(left = overivew_f , right = overview.groupby('ETF_CD')['NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
            overivew_f['TRD_AMT_AVG_20_y']=round(overivew_f['TRD_AMT_AVG_20_y']/100000000,0)
            overivew_f['TRD_AMT_AVG_20_x']=round(overivew_f['TRD_AMT_AVG_20_x']/100000000,0)
            overivew_f['Δ설정액(억)']=round((overivew_f['AUM_y']-overivew_f['AUM_x'].fillna(overivew_f['AUM'])*overivew_f['NAV_y']/overivew_f['NAV_x'].fillna(overivew_f['NAV']))/100000000,0)
            overivew_f['Δ거래대금(억)']=round(overivew_f['TRD_AMT_AVG_20_y']-overivew_f['TRD_AMT_AVG_20_x'].fillna(0),0)
            overivew_f['AUM_y']=round(overivew_f['AUM_y']/100000000,0)       
        
            overivew_f.rename(columns={'MANG_FEE_y':'운용보수'},inplace=True)
            overivew_f.rename(columns={'ETF_NM_y':'ETF_NM'},inplace=True)
            overivew_f.rename(columns={'AUM_y':'AUM(억원)'},inplace=True)
            overivew_f.rename(columns={'ETF_CNT_y':'구성종목수'},inplace=True)
            overivew_f.rename(columns={'DISPARATE_RATIO_y':'괴리율'},inplace=True)
            overivew_f.rename(columns={'TRD_AMT_AVG_20_y':'거래대금(억)'},inplace=True)
            
            overivew_r=overivew_f.copy()
            overivew_r['수익률']=round((overivew_r['NAV_y']/overivew_r['NAV_x']-1)*100,2)
            overivew_r['순위'] = overivew_r['수익률'].rank(method='min',ascending=False)    
            overivew_r=overivew_r.sort_values(by=['순위','ETF_NM'],axis=0,ascending=True)
            
            ##개인순매수 상위
            ant_ace=investor[(investor['INVEST_GB']==8)& (investor['TR_YMD']>=start_net)& (investor['TR_YMD']<=end)]
            ant_ace=ant_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
            ant_ace.rename(columns={'NET_AMT':'개인(억)'},inplace=True)
    
            
            ##보험순매수 상위
            ins_ace=investor[(investor['INVEST_GB']==2)& (investor['TR_YMD']>=start_net)& (investor['TR_YMD']<=end)]
            ins_ace=ins_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
            ins_ace.rename(columns={'NET_AMT':'보험(억)'},inplace=True)
    
            
            ##은행순매수 상위
            bnk_ace=investor[(investor['INVEST_GB']==4)& (investor['TR_YMD']>=start_net)& (investor['TR_YMD']<=end)]
            bnk_ace=bnk_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
            bnk_ace.rename(columns={'NET_AMT':'은행(억)'},inplace=True)
            
            
            overivew_f=pd.merge(left = overivew_f , right = ant_ace, how = "left", on = ['ETF_NM'])
            overivew_f=pd.merge(left = overivew_f , right = ins_ace, how = "left", on = ['ETF_NM'])
            overivew_f=pd.merge(left = overivew_f , right = bnk_ace, how = "left", on = ['ETF_NM'])
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
            
            gridOptions2 = GridOptionsBuilder.from_dataframe(overivew_r)
            gb2 = gridOptions2.build()
            
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
    
            
            gb['getRowStyle'] = jscode
            #gb['pinnedBottomRowData'] = [{'구분(소)':'합계','ΔAUM':ace_overview['ΔAUM'].sum(),'Δ설정액(억)':ace_overview['Δ설정액(억)'].sum(),'AUM(억원)':ace_overview['AUM(억원)'].sum(),'매출액(억원)':ace_overview['매출액(억원)'].sum(),'개인(억)':ace_overview['개인(억)'].sum(),'보험(억)':ace_overview['보험(억)'].sum(),'은행(억)':ace_overview['은행(억)'].sum(),'font-weight': 'bold'}]
            gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': 'ETF_NM'} ] }, 
                                 { 'headerName': 'ACEETF','headerClass': 'ace', 'children': [{'field': 'ΔAUM','width':90,'valueFormatter':"x.toLocaleString()","cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(억)','width':120,'valueFormatter':"x.toLocaleString()"},{'field': 'AUM(억원)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ거래대금(억)','width':105,'valueFormatter':"x.toLocaleString()"},{'field': '거래대금(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '구성종목수','width':105,'valueFormatter':"x.toLocaleString()"},{'field': '운용보수','width':100},{'field': '괴리율' ,'width':100,'valueFormatter':"x.toLocaleString()"},{'field': '개인(억)','width':110,'valueFormatter':"x.toLocaleString()"},{'field': '보험(억)','width':110,'valueFormatter':"x.toLocaleString()"},{'field': '은행(억)','width':110 ,'valueFormatter':"x.toLocaleString()"}] }, ] 
            
            gb2['columnDefs'] = [{ 'headerName': '수익률순위','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': 'ETF_NM','width':250,'valueFormatter':value3,"cellStyle": {'border-left': 'solid black'}},{'field': '수익률','width':135,'valueFormatter':value3}]}] 
          
            
            #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
            AgGrid(overivew_f, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)
            col11, col22,col33 = st.columns( [0.5,0.1,0.4])
            col15, col25,col35 = st.columns( [0.5,0.1,0.4])
           
            with col11:
                st.plotly_chart(fig_daily, theme="streamlit", use_conatiner_width=True)
                with col15:
                    st.plotly_chart(fig_daily2, theme="streamlit", use_conatiner_width=True)
                with col35:
                    st.plotly_chart(fig_daily3, theme="streamlit", use_conatiner_width=True)        
            with col33:
                AgGrid(overivew_r, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True)
                #st.plotly_chart(fig_daily3, theme="streamlit", use_conatiner_width=True)
                
        except IndexError:
            st.write('경쟁상품 맵핑전')
