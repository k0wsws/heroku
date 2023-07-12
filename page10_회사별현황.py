# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 10:17:53 2023

@author: user
"""

import streamlit as st
#import DB
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle
import plotly.express as px
import load as ld

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
#conn=DB.conn()
root=''

#데이터불러오기
comp_map,comp_overview,comp_investor,ant_ret=ld.load_data_p11()

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
        
        # comp_map=pickle.load( open(root+'comp_map.pkl', 'rb')) 
        # comp_overview=pickle.load( open(root+'comp_overview.pkl', 'rb')) 
        # comp_investor=pickle.load( open(root+'comp_investor.pkl', 'rb')) 
        # ant_ret=pickle.load(open(root+'ant_ret.pkl','rb')) 
        
        
        start=max(comp_overview[comp_overview['TR_YMD']<=start_t]['TR_YMD'])
        start_net=min(comp_overview[comp_overview['TR_YMD']>=start_t]['TR_YMD'])
        end=max(comp_overview[comp_overview['TR_YMD']<=end_t]['TR_YMD'])
        d1=max(comp_overview[comp_overview['TR_YMD']<end]['TR_YMD'])

        
        comp_fin=comp_overview[comp_overview['TR_YMD']==end]
        comp_start=comp_overview[comp_overview['TR_YMD']==start]
        comp_start.rename(columns={'순자산':'순자산n'},inplace=True)
        comp_start.rename(columns={'펀드수':'펀드수_y'},inplace=True)
        comp=pd.merge(left = comp_map[comp_map['TR_YMD']==start] , right = comp_map[comp_map['TR_YMD']==end], how = "right", on = ["ETF_CD","CO_NM"])
        comp=pd.merge(left = comp , right = comp_map.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        comp=pd.merge(left = comp , right = comp_map.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        comp['Δ설정액']=round(comp['AUM_y']-comp['AUM_x'].fillna(comp['AUM'])*comp['ETF_NAV_y']/comp['ETF_NAV_x'].fillna(comp['ETF_NAV']),2)
        comp['Δ설정액(초기시딩포함)']=round(comp['AUM_y']-comp['AUM_x'].fillna(0)*comp['ETF_NAV_y']/comp['ETF_NAV_x'].fillna(comp['ETF_NAV']),2)
        comp2=pd.merge(left = comp_map[comp_map['TR_YMD']==d1] , right = comp_map[comp_map['TR_YMD']==end], how = "left", on = ["ETF_CD","ETF_NM","CO_NM"])
        comp2=pd.merge(left = comp2 , right = comp_map.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        comp2=pd.merge(left = comp2 , right = comp_map.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
        comp2['Δ설정액(D1)']=round(comp2['AUM_y']-comp2['AUM_x'].fillna(comp2['AUM'])*comp2['ETF_NAV_y']/comp2['ETF_NAV_x'].fillna(comp2['ETF_NAV']),2)
       
        #투자자별
        comp_inv=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==8)]
        comp_ins=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==2)]
        comp_bnk=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==4)]
        comp_alien=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==9)]
        comp_trust=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==3)]
        comp_corp=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==7)]
        comp_pef=comp_investor[(comp_investor['TR_YMD']>=start_net)&(comp_investor['TR_YMD']<=end)&(comp_investor['INVEST_GB']==31)]
       
        comp_fin=pd.merge(left=comp_fin,right=comp.groupby('CO_NM')['Δ설정액'].sum(),how="left",on=['CO_NM'])
        comp_fin=pd.merge(left=comp_fin,right=comp.groupby('CO_NM')['Δ설정액(초기시딩포함)'].sum(),how="left",on=['CO_NM'])
        comp_fin=pd.merge(left=comp_fin,right=comp.groupby('CO_NM')['AUM_x'].sum(),how="left",on=['CO_NM'])
        comp_fin=pd.merge(left=comp_fin,right=comp2.groupby('CO_NM')['Δ설정액(D1)'].sum(),how="left",on=['CO_NM'])
        comp_fin=pd.merge(left=comp_fin,right=comp2.groupby('CO_NM')['AUM_x'].sum(),how="left",on=['CO_NM'])
        comp_fin=pd.merge(left=comp_fin,right=comp2.groupby('CO_NM')['MANG_FEE_y'].mean(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'MANG_FEE_y':'평균보수'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_start,how="left",on=['CO_NM'])
        
        comp_fin=pd.merge(left=comp_fin,right=comp_inv.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'개인'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_ins.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'보험'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_bnk.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'은행'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_alien.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'외국인'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_trust.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'투신'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_corp.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'기타법인'},inplace=True)
        comp_fin=pd.merge(left=comp_fin,right=comp_pef.groupby('CO_NM')['NET_AMT'].sum(),how="left",on=['CO_NM'])
        comp_fin.rename(columns={'NET_AMT':'사모펀드'},inplace=True)
        
        ant=ant_ret[ant_ret['TR_YMD']==end]
        ant=ant.drop('ETF_NM',axis=1)
        ant=ant.drop('TR_YMD',axis=1)
        ant['ant_amt']=ant['CNT']*ant['CLS_PRC']
        
        comp_fin=pd.merge(left=comp_fin,right=ant.groupby('CO_NM')['ant_amt'].sum(),how="left",on=['CO_NM'])
        comp_fin['ant_amt']=round(comp_fin['ant_amt']/100000000,2)
        comp_fin.rename(columns={'ant_amt':'개인잔고(억)'},inplace=True)
        comp_fin.rename(columns={'매출액(억원)_x':'매출액(억원)'},inplace=True)
        
        comp_fin['평균보수']=round(comp_fin['평균보수'],2)
        comp_fin['개인']=round(comp_fin['개인']/10000,0)
        comp_fin['보험']=round(comp_fin['보험']/10000,0)
        comp_fin['은행']=round(comp_fin['은행']/10000,0)
        comp_fin['외국인']=round(comp_fin['외국인']/10000,0)
        comp_fin['기타법인']=round(comp_fin['기타법인']/10000,0)
        comp_fin['사모펀드']=round(comp_fin['사모펀드']/10000,0)
        comp_fin['투신']=round(comp_fin['투신']/10000,0)

        comp_fin['순자산']=round(comp_fin['순자산']/100000000,0)
        comp_fin['Δ순자산']=comp_fin['순자산']-round(comp_fin['AUM_x_x']/100000000,0)
        comp_fin['Δ순자산(D1)']=comp_fin['순자산']-round(comp_fin['AUM_x_y']/100000000,0)
        comp_fin['Δ설정액']=round(comp_fin['Δ설정액']/100000000,0)
        comp_fin['Δ설정액(초기시딩포함)']=round(comp_fin['Δ설정액(초기시딩포함)']/100000000,0)
        comp_fin['Δ설정액(D1)']=round(comp_fin['Δ설정액(D1)']/100000000,0)
        comp_fin['M/S(%)']=round(100*comp_fin['순자산']/comp_fin['순자산'].sum(),2)
        comp_fin['M/S']=100*comp_fin['순자산']/comp_fin['순자산'].sum()
        comp_fin['Δ펀드수']=comp_fin['펀드수']-comp_fin['펀드수_y']
        comp_fin['펀드수']=comp_fin['펀드수'].astype(float)
        comp_fin['Δ펀드수']=comp_fin['Δ펀드수'].astype(float)
        
        comp_fin=comp_fin.sort_values(by='M/S(%)',ascending=False)

        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">회사별 펀드 현황</p>', unsafe_allow_html=True) 
        
        ##성과분석차트
        # chart=comp_overview[(comp_overview['TR_YMD']>=start)& (comp_overview['TR_YMD']<=end)]
        # chart=chart.sort_values(by='TR_YMD')
        # chart['TR_YMD'] = pd.to_datetime(chart['TR_YMD'], format='%Y%m%d')
        # chart['TR_YMD'] = chart['TR_YMD'].dt.strftime('%Y-%m-%d')
        # chart=chart.sort_values(by='TR_YMD')
        # fig_daily=px.line(chart,x="TR_YMD",y='매출액(억원)',color="CO_NM",title="매출액비교차트" )
        # fig_daily.update_layout(title='매출액비교차트')

           
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(comp_fin,min_column_width=30)
        #gridOptions.configure_side_bar()
        
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
             if (params.row === '한국투자신탁운용') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
              }
            };
        """
        
        def get_row_style(params):
            salary = params["data"]["salary"]
            if salary > 60000:
                return {"background-color": "#90EE90"}  # Light green
            else:
                return {"background-color": "white"}  # White

        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value > 0) {
                return {
                    'color': 'black',
                    'backgroundColor': 'white'
                }
            } if (params.value < 0) {
                return {
                    'color': 'red',
                    'backgroundColor': 'white'
                }
            }
        };
        """)

    
        value=JsCode("""function(params) {
        if (params.value > 0){
         return '+' + (params.value.toLocaleString())}
        if (params.value == 0){
         return '-'}
        if (params.value < 0){
         return params.value.toLocaleString()}
                };""")
            
        value2=JsCode("""function(params) {
        if (params.value > 0){
         return (params.value.toLocaleString())}
        if (params.value == 0){
         return '-'}
        if (params.value < 0){
         return params.value.toLocaleString()}
                };""")   
        value3=JsCode("""function(params) {
        if (params.value > 0){
         return (params.value.toLocaleString()+'%')}
        if (params.value == 0){
         return '-'+'%'}
        if (params.value < 0){
         return params.value.toLocaleString()+'%'}
                };""")   
        
        #jscode = jscode.replace("#{length}", str(len(df_main)-1)) 
        

        jscode = JsCode(jscode)
       
        gb = gridOptions.build()

        
        gb['getRowStyle'] = jscode
        gb['pinnedBottomRowData'] = [{'CO_NM':'합계','펀드수':comp_fin['펀드수'].sum(),'Δ펀드수':comp_fin['Δ펀드수'].sum(),'순자산':comp_fin['순자산'].sum(),'M/S(%)':comp_fin['M/S'].sum(),'Δ순자산(D1)':comp_fin['Δ순자산(D1)'].sum(),'Δ순자산':comp_fin['Δ순자산'].sum(),'Δ설정액(D1)':comp_fin['Δ설정액(D1)'].sum(),'매출액(억원)':comp_fin['매출액(억원)'].sum(),'Δ설정액':comp_fin['Δ설정액'].sum(),'개인':comp_fin['개인'].sum(),'은행':comp_fin['은행'].sum(),'보험':comp_fin['보험'].sum(),'외국인':comp_fin['외국인'].sum(),'투신':comp_fin['투신'].sum(),'기타법인':comp_fin['기타법인'].sum(),'사모펀드':comp_fin['사모펀드'].sum()}]
        gb['columnDefs'] = [ {'headerClass': 'all', 'children': [{'field': 'CO_NM','width':170},{'field': '펀드수','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ펀드수','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '순자산','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'M/S(%)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ순자산(D1)','width':120,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': 'Δ순자산','width':100,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': 'Δ설정액(D1)','width':120,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': 'Δ설정액','width':100,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': 'Δ설정액(초기시딩포함)','width':200,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '평균보수','width':100,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '매출액(억원)','width':130,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '개인','width':80,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '은행','width':80,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '보험','width':80,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '외국인','width':90,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '투신','width':90,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '기타법인','width':90,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '사모펀드','width':90,'valueFormatter':value2,"cellStyle":cellsytle_jscode},{'field': '개인잔고(억)','width':130,'valueFormatter':value2,"cellStyle":cellsytle_jscode}] } ] 
              
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(comp_fin, gridOptions=gb ,allow_unsafe_jscode=True)
        col11, col22,col33 = st.columns( [0.1,0.8,0.1])
 
           
       # with col22:
                #st.plotly_chart(fig_daily, theme="streamlit", use_conatiner_width=True)
