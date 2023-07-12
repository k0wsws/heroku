import streamlit as st
#import DB
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle

logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
root=''
print(pd.__version__)
print("Streamlit version:", st.__version__)

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
        


        aum_ace_raw=pickle.load(open(root+'aum_ace.pkl','rb'))   
        investor_ace=pickle.load(open(root+'investor_ace.pkl','rb'))   
        ace_overview=pickle.load( open(root+'ace_overview.pkl', 'rb')) 
        etf_map=pickle.load( open(root+'etf_map.pkl', 'rb')) 
        trd_amt=pickle.load( open(root+'trd_amt.pkl', 'rb')) 
        
        start=max(ace_overview[ace_overview['TR_YMD']<=start_t]['TR_YMD'])
        start_net=min(ace_overview[ace_overview['TR_YMD']>=start_t]['TR_YMD'])
        end=max(ace_overview[ace_overview['TR_YMD']<=end_t]['TR_YMD'])
        
        

        ace_overview=pd.merge(left = ace_overview[ace_overview['TR_YMD']=='20230428'] , right = etf_map, how = "left", on = ["ETF_CD"])
        
        ##개인순매수 상위
        ant_ace=investor_ace[(investor_ace['INVEST_GB']==8)& (investor_ace['TR_YMD']>='20230401')& (investor_ace['TR_YMD']<='20230428')]
        ant_ace=ant_ace.groupby(['ETF_NM']).sum('NET_AMT').reset_index()
        ant_ace.rename(columns={'NET_AMT':'개인(억)'},inplace=True)

        
        ##보험순매수 상위
        ins_ace=investor_ace[(investor_ace['INVEST_GB']==2)& (investor_ace['TR_YMD']>='20230401')& (investor_ace['TR_YMD']<='20230428')]
        ins_ace=ins_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
        ins_ace.rename(columns={'NET_AMT':'보험(억)'},inplace=True)

        
        ##은행순매수 상위
        bnk_ace=investor_ace[(investor_ace['INVEST_GB']==4)& (investor_ace['TR_YMD']>='20230401')& (investor_ace['TR_YMD']<='20230428')]
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
  
        
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">ACE ETF 현황</p>', unsafe_allow_html=True) 
           
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
                             { 'headerName': 'ACEETF','headerClass': 'all', 'children': [{'field': 'ΔAUM','width':70,'valueFormatter':"x.toLocaleString()","cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'AUM(억원)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': 'Δ거래대금(억)','width':105,'valueFormatter':"x.toLocaleString()"},{'field': '거래대금(억)','width':100,'valueFormatter':"x.toLocaleString()"},{'field': '거래량','width':80,'valueFormatter':"x.toLocaleString()"},{'field': '보수','width':70},{'field': '매출액(억원)' ,'width':100,'valueFormatter':"x.toLocaleString()"},{'field': '개인(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '보험(억)','width':90,'valueFormatter':"x.toLocaleString()"},{'field': '은행(억)','width':90 ,'valueFormatter':"x.toLocaleString()"}] }, ] 
              
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(ace_overview, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)
