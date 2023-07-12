# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:43:47 2023

@author: user
"""

import streamlit as st
import DB_ETF as DB
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import pandas as pd
import pickle 
root='C:\\Users\\user\\Dashboard\\dataset\\'
conn=DB.conn()
logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)


# act=pickle.load(open(root+'act.pkl', 'rb') )

# act.groupby(['TR_YMD','AP_GB'])['AUM'].sum()
# act.groupby(['TR_YMD','AP_GB'])['AUM'].sum()
# act[act['AP_GB']=='액티브'].groupby(['TR_YMD','AP_GB'])['AUM'].sum()

class generate():

    
    # Streamlit 생성 메인 파트
    def __init__(self):  
        global start_t
        global end_t
        col1, col2 = st.columns( [0.8, 0.2])
        
        with col2:               # To display brand log
            st.image(logo, width=200 )

        option3 = st.selectbox("시장구분", ("전체시장","국내 주식","국내 채권","해외 주식", "해외 채권","기타"),key=3)
        
        col3, col4 = st.columns( [0.5, 0.5]) 
        with col3:               # To display brand log
            start_t=self.start_dt()
        with col4:               # To display brand log
            end_t=self.end_dt()
        
        if option3== '국내 주식':
                self.kor_stk()
        elif option3== '국내 채권':
                self.kor_bond()
                
        elif option3== '해외 주식':
                self.glb_stk()
        elif option3== '해외 채권':
                self.glb_bond()
        elif option3== '기타':
                self.etc()
        elif option3== '전체시장':
                self.all()
                
    def start_dt(self):
        start = st.date_input(
            "시작일",pmonth)
        start=str(start).replace("-", "")[0:8]
        
        return start
        

    def end_dt(self):
        end = st.date_input(
            "기준일",
            Pday())
        end=str(end).replace("-", "")[0:8]
        return end
        

############################## 국내주식    ###########################

    def kor_stk(self):
        
        df_main="""
            SELECT A.ETF_MKT_BIG '구분(대)' ,A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,0) '평균AUM',ROUND(A.SELL_SUM,0) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "ACE M/S",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,0) " 평균AUM" FROM (SELECT
        	DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY 
            ETF_MKT_BIG,            
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
        	(SELECT
        		DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_MKT_BIG = B.ETF_MKT_BIG AND A.ETF_AST_MID = B.ETF_AST_MID AND A.ETF_AST_SML=B.ETF_AST_SML
            """
            
        df_main = df_main.replace('#{END_DT}', end_t)  
        
        
        df_main=DB.read(df_main,conn)
        
        
        
        df_inv="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND((A.AMT)/10000,0) '개인(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG,
                ETF_AST_MID,
                ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=8) A
            """
        df_inv = df_inv.replace('#{START_DT}', start_t)              
        df_inv = df_inv.replace('#{END_DT}', end_t)  
        df_inv=DB.read(df_inv,conn)
        
        df_isr="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG,
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=2) A
            """
        df_isr = df_isr.replace('#{START_DT}', start_t)              
        df_isr = df_isr.replace('#{END_DT}', end_t)  
        df_isr=DB.read(df_isr,conn)
        
        df_bnk="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG, 
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG,ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=4) A
            """
        df_bnk = df_bnk.replace('#{START_DT}', start_t)              
        df_bnk = df_bnk.replace('#{END_DT}', end_t)  
        df_bnk=DB.read(df_bnk,conn)
        
        df_inv_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',round((A.AMT)/10000,0) ' 개인(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG,
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG,ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=8
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
        df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
        df_inv_ace=DB.read(df_inv_ace,conn)

        df_isr_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG, 
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=2
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
        df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
        df_isr_ace=DB.read(df_isr_ace,conn)

        df_bnk_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG,
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=4
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
        df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
        df_bnk_ace=DB.read(df_bnk_ace,conn)

        
        df_aum="""
       	SELECT
    	DISTINCT 
    	ETF_AST_MID '구분(중)',
    	ETF_AST_SML '구분(소)',
    	ROUND(SUM(AUM) OVER (PARTITION BY 
    	ETF_AST_MID,
    	ETF_AST_SML)/100000000,0) '기초(AUM)',
    	COUNT(B.etf_cd) OVER (PARTITION BY 
    	ETF_AST_MID,
    	ETF_AST_SML) '기초(개수)'
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
            """
        df_aum = df_aum.replace('#{START_DT}', start_t)                          
        df_aum=DB.read(df_aum,conn)
        
        
        df_ace_aum="""
       	SELECT
        	DISTINCT 
        	ETF_AST_MID '구분(중)',
        	ETF_AST_SML '구분(소)',
        	ROUND(SUM(AUM) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000,0) ' 기초(AUM)',
        	COUNT(A.STK_CD) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum = df_ace_aum.replace('#{START_DT}', start_t)                          
        df_ace_aum=DB.read(df_ace_aum,conn)
        

        df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_ace_aum, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_inv_ace, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr_ace, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk_ace, how = "left", on = ["구분(중)","구분(소)"])     
        
        df_main=df_main.fillna(0)

        df_main['ΔAUM']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
        df_main[' ΔAUM']=round(df_main[' 기말(AUM)']-df_main[' 기초(AUM)'],0)
        df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)
        df_main[' Δ개수']=round(df_main[' 기말(개수)']-df_main[' 기초(개수)'],0)
        
        df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['기초(M/S)']=100*round(df_main[' 기초(AUM)']/df_main['기초(AUM)'].sum(),3)
        df_main['기말(M/S)']=100*round(df_main[' 기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['ΔM/S']=round(df_main['기말(M/S)']-df_main['기초(M/S)'],2)
        
        ##레버리지
        
        df_lev="""
            SELECT A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,2) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "기말(M/S)",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"  FROM (SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
    	(SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_AST_SML=B.ETF_AST_SML
            """
            
            #sql = sql.replace('#{START_DT}', trd_dt)  
            
        
        df_lev=DB.read(df_lev,conn)
        
        df_inv_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev = df_inv_lev.replace('#{START_DT}', start_t)              
        df_inv_lev = df_inv_lev.replace('#{END_DT}', end_t)  
        df_inv_lev = DB.read(df_inv_lev,conn)
        
        df_isr_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev = df_isr_lev.replace('#{START_DT}', start_t)              
        df_isr_lev = df_isr_lev.replace('#{END_DT}', end_t)  
        df_isr_lev = DB.read(df_isr_lev,conn)
        
        df_bnk_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev = df_bnk_lev.replace('#{START_DT}', start_t)              
        df_bnk_lev = df_bnk_lev.replace('#{END_DT}', end_t)  
        df_bnk_lev = DB.read(df_bnk_lev,conn)
        
        df_inv_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev_ace = df_inv_lev_ace.replace('#{START_DT}', start_t)              
        df_inv_lev_ace = df_inv_lev_ace.replace('#{END_DT}', end_t)  
        df_inv_lev_ace = DB.read(df_inv_lev_ace,conn)

        df_isr_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev_ace = df_isr_lev_ace.replace('#{START_DT}', start_t)              
        df_isr_lev_ace = df_isr_lev_ace.replace('#{END_DT}', end_t)  
        df_isr_lev_ace = DB.read(df_isr_lev_ace,conn)

        df_bnk_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{START_DT}', start_t)              
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{END_DT}', end_t)  
        df_bnk_lev_ace = DB.read(df_bnk_lev_ace,conn)

        
        df_aum_lev="""
            SELECT
         	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
         	ROUND(SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000,0) '기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) '기초(개수)'
         FROM
         	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
         WHERE
         	ETF_MKT_BIG = '국내'
         	AND ETF_AST_BIG ='주식'
         	AND ETF_MKT_MID <> ''
         	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
             AND B.ETF_CD = A.STK_CD
             AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
             AND B.ETF_CD = C.ETF_CD
             AND C.TR_YMD = B.TR_YMD
            """
        df_aum_lev = df_aum_lev.replace('#{START_DT}', start_t)                          
        df_aum_lev = DB.read(df_aum_lev,conn)
        
        
        df_ace_aum_lev="""
         SELECT
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 ' 기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum_lev = df_ace_aum_lev.replace('#{START_DT}', start_t)                          
        df_ace_aum_lev = DB.read(df_ace_aum_lev,conn)
        

        df_lev=pd.merge(left = df_lev , right = df_inv_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_aum_lev, how = "left", on =  ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_ace_aum_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_inv_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev_ace, how = "left", on = ["구분(소)"])
        
        
        df_lev=df_lev.fillna(0)
        
        df_lev['ΔAUM']=round(df_lev['기말(AUM)']-df_lev['기초(AUM)'],0)
        df_lev[' ΔAUM']=round(df_lev[' 기말(AUM)']-df_lev[' 기초(AUM)'],0)
        
        df_lev['Δ개수']=round(df_lev['기말(개수)']-df_lev['기초(개수)'],0)
        df_lev[' Δ개수']=round(df_lev[' 기말(개수)']-df_lev[' 기초(개수)'],0)
        
        df_lev['M/S']=100*round(df_lev['기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['기초(M/S)']=100*round(df_lev[' 기초(AUM)']/df_lev['기초(AUM)'].sum(),3)
        df_lev['기말(M/S)']=100*round(df_lev[' 기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['ΔM/S']=round(df_lev['기말(M/S)']-df_lev['기초(M/S)'],2)
        
        
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">국내 주식형 ETF 현황</p>', unsafe_allow_html=True) 
           
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions3 = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions2 = GridOptionsBuilder.from_dataframe(df_lev)
        gridOptions4 = GridOptionsBuilder.from_dataframe(df_lev)
        
        gridOptions.configure_side_bar()
        gridOptions2.configure_side_bar()
        gridOptions3.configure_side_bar()
        gridOptions4.configure_side_bar()
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value > 0) {
                return {
                    'color': 'blue',
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
 
        
        jscode=JsCode("""
        function(params) {
            if (params.node.rowPinned === 'bottom') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
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
        
       
        gb = gridOptions.build()
        gb2 = gridOptions2.build()
        gb3 = gridOptions3.build()
        gb4 = gridOptions4.build()

        
        gb['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb2['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb3['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb4['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        
        gb['getRowStyle'] = jscode
        gb2['getRowStyle'] = jscode
        gb3['getRowStyle'] = jscode
        gb4['getRowStyle'] = jscode
        
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important' }, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
        gb2['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
       
        gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important'}, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        gb4['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)      
        AgGrid(df_lev, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
        AgGrid(df_main, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        AgGrid(df_lev, gridOptions=gb4,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
    
    ############################## 국내채권    ###########################
    def kor_bond(self):
        df_main="""
            SELECT A.ETF_MKT_BIG '구분(대)' ,A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,0) '평균AUM',ROUND(A.SELL_SUM,0) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "ACE M/S",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,0) " 평균AUM" FROM (SELECT
        	DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
        	(SELECT
        		DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_MKT_BIG = B.ETF_MKT_BIG AND A.ETF_AST_MID = B.ETF_AST_MID AND A.ETF_AST_SML=B.ETF_AST_SML
            """
            
        df_main = df_main.replace('#{END_DT}', end_t)  
            
        
        df_main=DB.read(df_main,conn)
        
        df_inv="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND((A.AMT)/10000,0) '개인(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=8) A
            """
        df_inv = df_inv.replace('#{START_DT}', start_t)              
        df_inv = df_inv.replace('#{END_DT}', end_t)  
        df_inv=DB.read(df_inv,conn)
        
        df_isr="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=2) A
            """
        df_isr = df_isr.replace('#{START_DT}', start_t)              
        df_isr = df_isr.replace('#{END_DT}', end_t)  
        df_isr=DB.read(df_isr,conn)
        
        df_bnk="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=4) A
            """
        df_bnk = df_bnk.replace('#{START_DT}', start_t)              
        df_bnk = df_bnk.replace('#{END_DT}', end_t)  
        df_bnk=DB.read(df_bnk,conn)
        
        df_inv_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',round((A.AMT)/10000,0) ' 개인(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=8
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
        df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
        df_inv_ace=DB.read(df_inv_ace,conn)

        df_isr_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=2
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
        df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
        df_isr_ace=DB.read(df_isr_ace,conn)

        df_bnk_ace="""
            SELECT A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
            (select
            	DISTINCT ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_MKT_BIG = '국내'
            	AND ETF_AST_BIG = '채권'
                AND B.INVEST_GB=4
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
        df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
        df_bnk_ace=DB.read(df_bnk_ace,conn)

        
        df_aum="""
       	SELECT
    	DISTINCT 
    	ETF_AST_MID '구분(중)',
    	ETF_AST_SML '구분(소)',
    	ROUND(SUM(AUM) OVER (PARTITION BY 
    	ETF_AST_MID,
    	ETF_AST_SML)/100000000,0) '기초(AUM)',
    	COUNT(B.etf_cd) OVER (PARTITION BY 
    	ETF_AST_MID,
    	ETF_AST_SML) '기초(개수)'
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='채권'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
            """
        df_aum = df_aum.replace('#{START_DT}', start_t)                          
        df_aum=DB.read(df_aum,conn)
        
        
        df_ace_aum="""
       	SELECT
        	DISTINCT 
        	ETF_AST_MID '구분(중)',
        	ETF_AST_SML '구분(소)',
        	ROUND(SUM(AUM) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000,0) ' 기초(AUM)',
        	COUNT(A.STK_CD) OVER (PARTITION BY 
        	ETF_AST_MID,
        	ETF_AST_SML) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum = df_ace_aum.replace('#{START_DT}', start_t)                          
        df_ace_aum=DB.read(df_ace_aum,conn)
        

        df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_ace_aum, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_inv_ace, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr_ace, how = "left", on = ["구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk_ace, how = "left", on = ["구분(중)","구분(소)"])        

        df_main=df_main.fillna(0)
        
        df_main['ΔAUM']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
        df_main[' ΔAUM']=round(df_main[' 기말(AUM)']-df_main[' 기초(AUM)'],0)
        df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)
        df_main[' Δ개수']=round(df_main[' 기말(개수)']-df_main[' 기초(개수)'],0)
        
        df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['기초(M/S)']=100*round(df_main[' 기초(AUM)']/df_main['기초(AUM)'].sum(),3)
        df_main['기말(M/S)']=100*round(df_main[' 기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['ΔM/S']=round(df_main['기말(M/S)']-df_main['기초(M/S)'],2)
        
        ##레버리지
        
        df_lev="""
            SELECT A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,2) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "기말(M/S)",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"  FROM (SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='채권'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
    	(SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '국내'
    	AND ETF_AST_BIG ='채권'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_AST_SML=B.ETF_AST_SML
            """
            
            #sql = sql.replace('#{START_DT}', trd_dt)  
            
        
        df_lev=DB.read(df_lev,conn)
        
        df_inv_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev = df_inv_lev.replace('#{START_DT}', start_t)              
        df_inv_lev = df_inv_lev.replace('#{END_DT}', end_t)  
        df_inv_lev = DB.read(df_inv_lev,conn)
        
        df_isr_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev = df_isr_lev.replace('#{START_DT}', start_t)              
        df_isr_lev = df_isr_lev.replace('#{END_DT}', end_t)  
        df_isr_lev = DB.read(df_isr_lev,conn)
        
        df_bnk_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev = df_bnk_lev.replace('#{START_DT}', start_t)              
        df_bnk_lev = df_bnk_lev.replace('#{END_DT}', end_t)  
        df_bnk_lev = DB.read(df_bnk_lev,conn)
        
        df_inv_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev_ace = df_inv_lev_ace.replace('#{START_DT}', start_t)              
        df_inv_lev_ace = df_inv_lev_ace.replace('#{END_DT}', end_t)  
        df_inv_lev_ace = DB.read(df_inv_lev_ace,conn)

        df_isr_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev_ace = df_isr_lev_ace.replace('#{START_DT}', start_t)              
        df_isr_lev_ace = df_isr_lev_ace.replace('#{END_DT}', end_t)  
        df_isr_lev_ace = DB.read(df_isr_lev_ace,conn)

        df_bnk_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
        	AND ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG = '채권'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{START_DT}', start_t)              
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{END_DT}', end_t)  
        df_bnk_lev_ace = DB.read(df_bnk_lev_ace,conn)

        
        df_aum_lev="""
            SELECT
         	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
         	ROUND(SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000,0) '기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) '기초(개수)'
         FROM
         	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
         WHERE
         	ETF_MKT_BIG = '국내'
         	AND ETF_AST_BIG ='채권'
         	AND ETF_MKT_MID <> ''
         	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
             AND B.ETF_CD = A.STK_CD
             AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
             AND B.ETF_CD = C.ETF_CD
             AND C.TR_YMD = B.TR_YMD
            """
        df_aum_lev = df_aum_lev.replace('#{START_DT}', start_t)                          
        df_aum_lev = DB.read(df_aum_lev,conn)
        
        
        df_ace_aum_lev="""
         SELECT
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 ' 기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '국내'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum_lev = df_ace_aum_lev.replace('#{START_DT}', start_t)                          
        df_ace_aum_lev = DB.read(df_ace_aum_lev,conn)
        

        df_lev=pd.merge(left = df_lev , right = df_inv_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_aum_lev, how = "left", on =  ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_ace_aum_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_inv_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev_ace, how = "left", on = ["구분(소)"])
        
        df_lev=df_lev.fillna(0)
        
        df_lev['ΔAUM']=round(df_lev['기말(AUM)']-df_lev['기초(AUM)'],0)
        df_lev[' ΔAUM']=round(df_lev[' 기말(AUM)']-df_lev[' 기초(AUM)'],0)
        
        df_lev['Δ개수']=round(df_lev['기말(개수)']-df_lev['기초(개수)'],0)
        df_lev[' Δ개수']=round(df_lev[' 기말(개수)']-df_lev[' 기초(개수)'],0)
        
        df_lev['M/S']=100*round(df_lev['기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['기초(M/S)']=100*round(df_lev[' 기초(AUM)']/df_lev['기초(AUM)'].sum(),3)
        df_lev['기말(M/S)']=100*round(df_lev[' 기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['ΔM/S']=round(df_lev['기말(M/S)']-df_lev['기초(M/S)'],2)
        
        
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">국내 채권형 ETF 현황</p>', unsafe_allow_html=True) 
           
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions3 = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions2 = GridOptionsBuilder.from_dataframe(df_lev)
        gridOptions4 = GridOptionsBuilder.from_dataframe(df_lev)
        
        gridOptions.configure_side_bar()
        gridOptions2.configure_side_bar()
        gridOptions3.configure_side_bar()
        gridOptions4.configure_side_bar()
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value > 0) {
                return {
                    'color': 'blue',
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
 
        
        jscode=JsCode("""
        function(params) {
            if (params.node.rowPinned === 'bottom') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
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
        
       
        gb = gridOptions.build()
        gb2 = gridOptions2.build()
        gb3 = gridOptions3.build()
        gb4 = gridOptions4.build()

        
        gb['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb2['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb3['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb4['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        
        gb['getRowStyle'] = jscode
        gb2['getRowStyle'] = jscode
        gb3['getRowStyle'] = jscode
        gb4['getRowStyle'] = jscode
        
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important' }, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
        gb2['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
       
        gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important'}, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        gb4['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)      
        AgGrid(df_lev, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
        AgGrid(df_main, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        AgGrid(df_lev, gridOptions=gb4,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
    
    ############################해외 주식##################################
    
    def glb_stk(self):
        df_main="""
            SELECT A.ETF_MKT_MID '시장(중)' ,A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,2) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "기말(M/S)",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"    FROM (SELECT
    	DISTINCT ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML,
    	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD='#{END_DT}'
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
    	(SELECT
    		DISTINCT ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML,
    	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_MID,
    	ETF_MKT_SML,
    	ETF_AST_MID,
    	ETF_AST_SML)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD='#{END_DT}'
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_MKT_MID = B.ETF_MKT_MID AND A.ETF_MKT_SML=B.ETF_MKT_SML AND A.ETF_AST_MID = B.ETF_AST_MID AND A.ETF_AST_SML=B.ETF_AST_SML
            """
            
        
        df_main = df_main.replace('#{END_DT}', end_t)  
        df_main=DB.read(df_main,conn)
        
        df_inv="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',round((A.AMT)/10000,0) '개인(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=8) A
            """
        df_inv = df_inv.replace('#{START_DT}', start_t)              
        df_inv = df_inv.replace('#{END_DT}', end_t)  
        df_inv=DB.read(df_inv,conn)

        df_isr="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '보험(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=2) A
            """
        df_isr = df_isr.replace('#{START_DT}', start_t)              
        df_isr = df_isr.replace('#{END_DT}', end_t)  
        df_isr=DB.read(df_isr,conn)
        
        df_bnk="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '은행(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=4) A
            """
        df_bnk = df_bnk.replace('#{START_DT}', start_t)              
        df_bnk = df_bnk.replace('#{END_DT}', end_t)  
        df_bnk=DB.read(df_bnk,conn)
        
        df_inv_ace="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',round((A.AMT)/10000,0) ' 개인(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=8
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
        df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
        df_inv_ace=DB.read(df_inv_ace,conn)

        df_isr_ace="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 보험(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=2
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
        df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
        df_isr_ace=DB.read(df_isr_ace,conn)

        df_bnk_ace="""
            SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 은행(억)' FROM 
            (select
            	DISTINCT ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
                AND B.INVEST_GB=4
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
        df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
        df_bnk_ace=DB.read(df_bnk_ace,conn)
        
        df_aum="""
   		SELECT
    	DISTINCT ETF_MKT_MID '시장(중)' ,
            	ETF_MKT_SML '시장(소)' ,
            	ETF_AST_MID '자산(중)',
            	ETF_AST_SML '자산(소)',
    	ROUND(SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/100000000,0) '기초(AUM)',
            	COUNT(A.STK_CD) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) '기초(개수)'
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
            """
        df_aum = df_aum.replace('#{START_DT}', start_t)                          
        df_aum=DB.read(df_aum,conn)
        
        
        df_ace_aum="""
   		SELECT
    	DISTINCT ETF_MKT_MID '시장(중)' ,
            	ETF_MKT_SML '시장(소)' ,
            	ETF_AST_MID '자산(중)',
            	ETF_AST_SML '자산(소)',
    	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/100000000 ' 기초(AUM)',
        COUNT(A.STK_CD) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) ' 기초(개수)'
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum = df_ace_aum.replace('#{START_DT}', start_t)                          
        df_ace_aum=DB.read(df_ace_aum,conn)
        
        df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_ace_aum, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_inv_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_isr_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])

        
        df_main=df_main.fillna(0)
        
        df_main['ΔAUM']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
        df_main[' ΔAUM']=round(df_main[' 기말(AUM)']-df_main[' 기초(AUM)'],0)
        df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)
        df_main[' Δ개수']=round(df_main[' 기말(개수)']-df_main[' 기초(개수)'],0)
        
        df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['기초(M/S)']=100*round(df_main[' 기초(AUM)']/df_main['기초(AUM)'].sum(),3)
        df_main['기말(M/S)']=100*round(df_main[' 기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['ΔM/S']=round(df_main['기말(M/S)']-df_main['기초(M/S)'],2)
        
        
        
        df_lev="""
            SELECT A.ETF_AST_SML '자산(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,0) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "ACE M/S",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"     FROM (SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD='#{END_DT}'
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
    	(SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_MKT_BIG = '해외'
    	AND ETF_AST_BIG ='주식'
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD='#{END_DT}'
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_AST_SML=B.ETF_AST_SML
            """
            
        df_lev = df_lev.replace('#{END_DT}', end_t)       
        df_lev=DB.read(df_lev,conn)
        
        df_inv_lev="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
        	AND ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG = '주식'
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev = df_inv_lev.replace('#{START_DT}', start_t)              
        df_inv_lev = df_inv_lev.replace('#{END_DT}', end_t)  
        df_inv_lev = DB.read(df_inv_lev,conn)
        
        df_isr_lev="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '보험(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=2
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev = df_isr_lev.replace('#{START_DT}', start_t)              
        df_isr_lev = df_isr_lev.replace('#{END_DT}', end_t)  
        df_isr_lev = DB.read(df_isr_lev,conn)
        
        df_bnk_lev="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '은행(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=4
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev = df_bnk_lev.replace('#{START_DT}', start_t)              
        df_bnk_lev = df_bnk_lev.replace('#{END_DT}', end_t)  
        df_bnk_lev = DB.read(df_bnk_lev,conn)
        
        df_inv_lev_ace="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 개인(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=8
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev_ace = df_inv_lev_ace.replace('#{START_DT}', start_t)              
        df_inv_lev_ace = df_inv_lev_ace.replace('#{END_DT}', end_t)  
        df_inv_lev_ace = DB.read(df_inv_lev_ace,conn)

        df_isr_lev_ace="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 보험(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=2
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev_ace = df_isr_lev_ace.replace('#{START_DT}', start_t)              
        df_isr_lev_ace = df_isr_lev_ace.replace('#{END_DT}', end_t)  
        df_isr_lev_ace = DB.read(df_isr_lev_ace,conn)

        df_bnk_lev_ace="""
            SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 은행(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '주식'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=4
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{START_DT}', start_t)              
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{END_DT}', end_t)  
        df_bnk_lev_ace = DB.read(df_bnk_lev_ace,conn)


        df_aum_lev="""
            SELECT
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '자산(소)',
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 '기초(AUM)',
            	COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) '기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            """
        df_aum_lev = df_aum_lev.replace('#{START_DT}', start_t)                          
        df_aum_lev = DB.read(df_aum_lev,conn)


        df_ace_aum_lev="""
         SELECT
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '자산(소)',
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 ' 기초(AUM)',
            	COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='주식'
        	AND ETF_MKT_MID <> ''
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum_lev = df_ace_aum_lev.replace('#{START_DT}', start_t)                          
        df_ace_aum_lev = DB.read(df_ace_aum_lev,conn)

                  
        df_lev=pd.merge(left = df_lev , right = df_inv_lev, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_aum_lev, how = "left", on =  ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_ace_aum_lev, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_inv_lev_ace, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev_ace, how = "left", on = ["자산(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev_ace, how = "left", on = ["자산(소)"])
        
        df_lev=df_lev.fillna(0)
        
        df_lev['ΔAUM']=round(df_lev['기말(AUM)']-df_lev['기초(AUM)'],0)
        df_lev[' ΔAUM']=round(df_lev[' 기말(AUM)']-df_lev[' 기초(AUM)'],0)
        
        df_lev['Δ개수']=round(df_lev['기말(개수)']-df_lev['기초(개수)'],0)
        df_lev[' Δ개수']=round(df_lev[' 기말(개수)']-df_lev[' 기초(개수)'],0)
        
        df_lev['M/S']=100*round(df_lev['기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['기초(M/S)']=100*round(df_lev[' 기초(AUM)']/df_lev['기초(AUM)'].sum(),3)
        df_lev['기말(M/S)']=100*round(df_lev[' 기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['ΔM/S']=round(df_lev['기말(M/S)']-df_lev['기초(M/S)'],2)
        
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">해외 주식형 ETF 현황</p>', unsafe_allow_html=True) 
           
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions3 = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions2 = GridOptionsBuilder.from_dataframe(df_lev)
        gridOptions4 = GridOptionsBuilder.from_dataframe(df_lev)
        
        gridOptions.configure_side_bar()
        gridOptions2.configure_side_bar()
        gridOptions3.configure_side_bar()
        gridOptions4.configure_side_bar()
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value > 0) {
                return {
                    'color': 'blue',
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
 
        
        jscode=JsCode("""
        function(params) {
            if (params.node.rowPinned === 'bottom') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
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
        
   

       
        gb = gridOptions.build()
        gb2 = gridOptions2.build()
        gb3 = gridOptions3.build()
        gb4 = gridOptions4.build()

        
        gb['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb2['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb3['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb4['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        
        gb['getRowStyle'] = jscode
        gb2['getRowStyle'] = jscode
        gb3['getRowStyle'] = jscode
        gb4['getRowStyle'] = jscode
        
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ {'field': '시장(중)','background-color': '#1b6d85 !important' ,'width':100}, { 'field': '시장(소)' ,'width':100 }, { 'field': '자산(중)' ,'width':100 }, { 'field': '자산(소)' ,'width':100 } ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
        gb2['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100},{ 'field': '','width':100}  ,{ 'field': '','width':100} ,{ 'field': '자산(소)','width':100,'background-color': '#1b6d85 !important' } ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
       
        gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ {'field': '시장(중)','background-color': '#1b6d85 !important' ,'width':100}, { 'field': '시장(소)' ,'width':100 }, { 'field': '자산(중)' ,'width':100 }, { 'field': '자산(소)' ,'width':100 } ] }, 
                           { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)' ,'width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
      
        gb4['columnDefs'] = [  {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100},{ 'field': '','width':100}  ,{ 'field': '','width':100} ,{ 'field': '자산(소)','width':100,'background-color': '#1b6d85 !important' }] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)      
        AgGrid(df_lev, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
        AgGrid(df_main, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        AgGrid(df_lev, gridOptions=gb4,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
    
    
       
        

    ############################## 해외 채권    ###########################
    def glb_bond(self):
            df_main="""
                    SELECT A.ETF_MKT_MID '시장(중)' ,A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,2) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "기말(M/S)",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                                      WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                                      ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"    FROM (SELECT
            	DISTINCT ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/100000000 AUM_SUM,
            	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) ETF_CNT,
            	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) AVG_FEE,
            	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) AVG_AUM,
            	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/10000000000 SELL_SUM
            FROM
            	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
            WHERE
            	ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG ='채권'
            	AND ETF_MKT_MID <> ''
                AND B.ETF_CD = A.STK_CD
                AND B.TR_YMD='#{END_DT}'
                AND B.ETF_CD = C.ETF_CD
                AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
            	(SELECT
            		DISTINCT ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/100000000 AUM_SUM,
            	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) ETF_CNT,
            	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) AVG_FEE,
            	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML) AVG_AUM,
            	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_MID,
            	ETF_MKT_SML,
            	ETF_AST_MID,
            	ETF_AST_SML)/10000000000 SELL_SUM
            FROM
            	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
            WHERE
            	ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG ='채권'
            	AND ETF_MKT_MID <> ''
                AND B.ETF_CD = A.STK_CD
                AND B.TR_YMD='#{END_DT}'
                AND B.ETF_CD = C.ETF_CD
                AND C.TR_YMD = B.TR_YMD
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_MKT_MID = B.ETF_MKT_MID AND A.ETF_MKT_SML=B.ETF_MKT_SML AND A.ETF_AST_MID = B.ETF_AST_MID AND A.ETF_AST_SML=B.ETF_AST_SML
                    """
                    
                
            df_main = df_main.replace('#{END_DT}', end_t)  
            df_main=DB.read(df_main,conn)
            
            df_inv="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',round((A.AMT)/10000,0) '개인(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=8) A
                """
            df_inv = df_inv.replace('#{START_DT}', start_t)              
            df_inv = df_inv.replace('#{END_DT}', end_t)  
            df_inv=DB.read(df_inv,conn)

            df_isr="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '보험(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=2) A
                """
            df_isr = df_isr.replace('#{START_DT}', start_t)              
            df_isr = df_isr.replace('#{END_DT}', end_t)  
            df_isr=DB.read(df_isr,conn)
            
            df_bnk="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '은행(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=4) A
                """
            df_bnk = df_bnk.replace('#{START_DT}', start_t)              
            df_bnk = df_bnk.replace('#{END_DT}', end_t)  
            df_bnk=DB.read(df_bnk,conn)
            
            df_inv_ace="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',round((A.AMT)/10000,0) ' 개인(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=8
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
            df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
            df_inv_ace=DB.read(df_inv_ace,conn)

            df_isr_ace="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 보험(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=2
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
            df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
            df_isr_ace=DB.read(df_isr_ace,conn)

            df_bnk_ace="""
                SELECT A.ETF_MKT_MID '시장(중)',A.ETF_MKT_SML '시장(소)',A.ETF_AST_MID '자산(중)',A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 은행(억)' FROM 
                (select
                	DISTINCT ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_MID,
                    	ETF_MKT_SML,
                    	ETF_AST_MID,
                    	ETF_AST_SML) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                    AND B.INVEST_GB=4
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
            df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
            df_bnk_ace=DB.read(df_bnk_ace,conn)
            
            df_aum="""
        	SELECT
        	DISTINCT ETF_MKT_MID '시장(중)' ,
                	ETF_MKT_SML '시장(소)' ,
                	ETF_AST_MID '자산(중)',
                	ETF_AST_SML '자산(소)',
        	ROUND(SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML)/100000000,0) '기초(AUM)',
                	COUNT(A.STK_CD) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) '기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
                """
            df_aum = df_aum.replace('#{START_DT}', start_t)                          
            df_aum=DB.read(df_aum,conn)
            
            
            df_ace_aum="""
        	SELECT
        	DISTINCT ETF_MKT_MID '시장(중)' ,
                	ETF_MKT_SML '시장(소)' ,
                	ETF_AST_MID '자산(중)',
                	ETF_AST_SML '자산(소)',
        	SUM(AUM) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML)/100000000 ' 기초(AUM)',
            COUNT(A.STK_CD) OVER (PARTITION BY ETF_MKT_MID,
                	ETF_MKT_SML,
                	ETF_AST_MID,
                	ETF_AST_SML) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                """
            df_ace_aum = df_ace_aum.replace('#{START_DT}', start_t)                          
            df_ace_aum=DB.read(df_ace_aum,conn)
            
            df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_ace_aum, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_inv_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_isr_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
            df_main=pd.merge(left = df_main , right = df_bnk_ace, how = "left", on =  ["시장(중)","시장(소)","자산(중)","자산(소)"])
            
            df_main=df_main.fillna(0)
            
            df_main['ΔAUM']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
            df_main[' ΔAUM']=round(df_main[' 기말(AUM)']-df_main[' 기초(AUM)'],0)
            df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)
            df_main[' Δ개수']=round(df_main[' 기말(개수)']-df_main[' 기초(개수)'],0)
            
            df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)
            df_main['기초(M/S)']=100*round(df_main[' 기초(AUM)']/df_main['기초(AUM)'].sum(),3)
            df_main['기말(M/S)']=100*round(df_main[' 기말(AUM)']/df_main['기말(AUM)'].sum(),3)
            df_main['ΔM/S']=round(df_main['기말(M/S)']-df_main['기초(M/S)'],2)
            
            
            
            df_lev="""
                SELECT A.ETF_AST_SML '자산(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,0) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "ACE M/S",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                                  WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                                  ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"     FROM (SELECT
        	DISTINCT 
        	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
        	(SELECT
        	DISTINCT 
        	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_MKT_BIG = '해외'
        	AND ETF_AST_BIG ='채권'
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_AST_SML=B.ETF_AST_SML
                """
                
            df_lev = df_lev.replace('#{END_DT}', end_t)       
            df_lev=DB.read(df_lev,conn)
            
            df_inv_lev="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '개인(억)' FROM 
            (select
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B,
            	FN_ETFINFO C
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
            	AND ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG = '채권'
            	AND B.ETF_CD = C.ETF_CD
                AND B.INVEST_GB=8
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND C.TR_YMD = B.TR_YMD) A
                """
            df_inv_lev = df_inv_lev.replace('#{START_DT}', start_t)              
            df_inv_lev = df_inv_lev.replace('#{END_DT}', end_t)  
            df_inv_lev = DB.read(df_inv_lev,conn)
            
            df_isr_lev="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '보험(억)' FROM 
                (select
                	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B,
                	FN_ETFINFO C
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                	AND B.ETF_CD = C.ETF_CD
                    AND B.INVEST_GB=2
                	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                    AND C.TR_YMD = B.TR_YMD) A
                """
            df_isr_lev = df_isr_lev.replace('#{START_DT}', start_t)              
            df_isr_lev = df_isr_lev.replace('#{END_DT}', end_t)  
            df_isr_lev = DB.read(df_isr_lev,conn)
            
            df_bnk_lev="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 '은행(억)' FROM 
                (select
                	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B,
                	FN_ETFINFO C
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                	AND B.ETF_CD = C.ETF_CD
                    AND B.INVEST_GB=4
                	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                    AND C.TR_YMD = B.TR_YMD) A
                """
            df_bnk_lev = df_bnk_lev.replace('#{START_DT}', start_t)              
            df_bnk_lev = df_bnk_lev.replace('#{END_DT}', end_t)  
            df_bnk_lev = DB.read(df_bnk_lev,conn)
            
            df_inv_lev_ace="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 개인(억)' FROM 
                (select
                	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B,
                	FN_ETFINFO C
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                	AND B.ETF_CD = C.ETF_CD
                    AND B.INVEST_GB=8
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                    AND C.TR_YMD = B.TR_YMD) A
                """
            df_inv_lev_ace = df_inv_lev_ace.replace('#{START_DT}', start_t)              
            df_inv_lev_ace = df_inv_lev_ace.replace('#{END_DT}', end_t)  
            df_inv_lev_ace = DB.read(df_inv_lev_ace,conn)

            df_isr_lev_ace="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 보험(억)' FROM 
                (select
                	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B,
                	FN_ETFINFO C
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                	AND B.ETF_CD = C.ETF_CD
                    AND B.INVEST_GB=2
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                    AND C.TR_YMD = B.TR_YMD) A
                """
            df_isr_lev_ace = df_isr_lev_ace.replace('#{START_DT}', start_t)              
            df_isr_lev_ace = df_isr_lev_ace.replace('#{END_DT}', end_t)  
            df_isr_lev_ace = DB.read(df_isr_lev_ace,conn)

            df_bnk_lev_ace="""
                SELECT A.ETF_AST_SML '자산(소)',(A.AMT)/10000 ' 은행(억)' FROM 
                (select
                	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
                	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B,
                	FN_ETFINFO C
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}' 
                	AND ETF_MKT_BIG = '해외'
                	AND ETF_AST_BIG = '채권'
                	AND B.ETF_CD = C.ETF_CD
                    AND B.INVEST_GB=4
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                    AND C.TR_YMD = B.TR_YMD) A
                """
            df_bnk_lev_ace = df_bnk_lev_ace.replace('#{START_DT}', start_t)              
            df_bnk_lev_ace = df_bnk_lev_ace.replace('#{END_DT}', end_t)  
            df_bnk_lev_ace = DB.read(df_bnk_lev_ace,conn)


            df_aum_lev="""
                SELECT
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '자산(소)',
            	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 '기초(AUM)',
                	COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) '기초(개수)'
            FROM
            	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
            WHERE
            	ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG ='채권'
            	AND ETF_MKT_MID <> ''
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND B.ETF_CD = A.STK_CD
                AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
                AND B.ETF_CD = C.ETF_CD
                AND C.TR_YMD = B.TR_YMD
                """
            df_aum_lev = df_aum_lev.replace('#{START_DT}', start_t)                          
            df_aum_lev = DB.read(df_aum_lev,conn)


            df_ace_aum_lev="""
             SELECT
            	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '자산(소)',
            	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 ' 기초(AUM)',
                	COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ' 기초(개수)'
            FROM
            	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
            WHERE
            	ETF_MKT_BIG = '해외'
            	AND ETF_AST_BIG ='채권'
            	AND ETF_MKT_MID <> ''
            	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
                AND B.ETF_CD = A.STK_CD
                AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
                AND B.ETF_CD = C.ETF_CD
                AND C.TR_YMD = B.TR_YMD
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                """
            df_ace_aum_lev = df_ace_aum_lev.replace('#{START_DT}', start_t)                          
            df_ace_aum_lev = DB.read(df_ace_aum_lev,conn)

                      
            df_lev=pd.merge(left = df_lev , right = df_inv_lev, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_isr_lev, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_bnk_lev, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_aum_lev, how = "left", on =  ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_ace_aum_lev, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_inv_lev_ace, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_isr_lev_ace, how = "left", on = ["자산(소)"])
            df_lev=pd.merge(left = df_lev , right = df_bnk_lev_ace, how = "left", on = ["자산(소)"])
            
            df_lev=df_lev.fillna(0)
            
            df_lev['ΔAUM']=round(df_lev['기말(AUM)']-df_lev['기초(AUM)'],0)
            df_lev[' ΔAUM']=round(df_lev[' 기말(AUM)']-df_lev[' 기초(AUM)'],0)
            
            df_lev['Δ개수']=round(df_lev['기말(개수)']-df_lev['기초(개수)'],0)
            df_lev[' Δ개수']=round(df_lev[' 기말(개수)']-df_lev[' 기초(개수)'],0)
            
            df_lev['M/S']=100*round(df_lev['기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
            df_lev['기초(M/S)']=100*round(df_lev[' 기초(AUM)']/df_lev['기초(AUM)'].sum(),3)
            df_lev['기말(M/S)']=100*round(df_lev[' 기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
            df_lev['ΔM/S']=round(df_lev['기말(M/S)']-df_lev['기초(M/S)'],2)
            
            st.markdown(""" <style> .font {
            font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">해외 채권형 ETF 현황</p>', unsafe_allow_html=True) 
               
            custom_css = {
                #".ag-row-hover": {"background-color": "red !important"},
                #".ag-header-cell-label": {"background-color": "orange !important"},
                #".ag-header":{"background-color": "#d0cece !important"},
                ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
                ".all": {"background-color": "#d0cece !important","color":"black !important"},
                ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
                ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
            
            gridOptions = GridOptionsBuilder.from_dataframe(df_main)
            gridOptions3 = GridOptionsBuilder.from_dataframe(df_main)
            gridOptions2 = GridOptionsBuilder.from_dataframe(df_lev)
            gridOptions4 = GridOptionsBuilder.from_dataframe(df_lev)
            
            gridOptions.configure_side_bar()
            gridOptions2.configure_side_bar()
            gridOptions3.configure_side_bar()
            gridOptions4.configure_side_bar()
            
            cellsytle_jscode = JsCode("""
            function(params) {
                if (params.value > 0) {
                    return {
                        'color': 'blue',
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

            
            jscode=JsCode("""
            function(params) {
                if (params.node.rowPinned === 'bottom') {
                    return {  'color': 'black',
                              'backgroundColor': 'white',
                              'font-weight': 'bold' };
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
            
   

           
            gb = gridOptions.build()
            gb2 = gridOptions2.build()
            gb3 = gridOptions3.build()
            gb4 = gridOptions4.build()

            
            gb['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
            gb2['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
            gb3['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
            gb4['pinnedBottomRowData'] = [{'자산(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
            
            gb['getRowStyle'] = jscode
            gb2['getRowStyle'] = jscode
            gb3['getRowStyle'] = jscode
            gb4['getRowStyle'] = jscode
            
            gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ {'field': '시장(중)','background-color': '#1b6d85 !important' ,'width':100}, { 'field': '시장(소)' ,'width':100 }, { 'field': '자산(중)' ,'width':100 }, { 'field': '자산(소)' ,'width':100 } ] }, 
                                 { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
            
            gb2['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100},{ 'field': '','width':100}  ,{ 'field': '','width':100} ,{ 'field': '자산(소)','width':100,'background-color': '#1b6d85 !important' } ] }, 
                                 { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
            
           
            gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ {'field': '시장(중)','background-color': '#1b6d85 !important' ,'width':100}, { 'field': '시장(소)' ,'width':100 }, { 'field': '자산(중)' ,'width':100 }, { 'field': '자산(소)' ,'width':100 } ] }, 
                               { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)' ,'width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
          
            gb4['columnDefs'] = [  {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100},{ 'field': '','width':100}  ,{ 'field': '','width':100} ,{ 'field': '자산(소)','width':100,'background-color': '#1b6d85 !important' }] }, 
                                 { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
            
            
            #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
            AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)      
            AgGrid(df_lev, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
            AgGrid(df_main, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
            AgGrid(df_lev, gridOptions=gb4,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)

    ############################## 기타    ###########################
    
    def etc(self):
        
        df_main="""
            SELECT A.ETF_MKT_BIG '구분(대)' ,A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,0) '평균AUM',ROUND(A.SELL_SUM,0) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "ACE M/S",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,0) " 평균AUM" FROM (SELECT
        	DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	 ETF_AST_BIG NOT IN ('주식','채권')
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
        	(SELECT
        		DISTINCT ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML,
        	SUM(AUM) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000 AUM_SUM,
        	COUNT(STK_CD) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) ETF_CNT,
        	AVG(TOTAL_FEE) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_FEE,
        	AVG(AUM/100000000) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML) AVG_AUM,
        	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY ETF_MKT_BIG,
        	ETF_AST_MID,
        	ETF_AST_SML)/10000000000 SELL_SUM
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	 ETF_AST_BIG NOT IN ('주식','채권')
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_MKT_BIG = B.ETF_MKT_BIG AND A.ETF_AST_MID = B.ETF_AST_MID AND A.ETF_AST_SML=B.ETF_AST_SML
            """
            
        df_main = df_main.replace('#{END_DT}', end_t)  
        
        
        df_main=DB.read(df_main,conn)
        
        
        
        df_inv="""
            SELECT A.ETF_MKT_BIG '구분(대)',A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',ROUND((A.AMT)/10000,0) '개인(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG,ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG,ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=8) A
            """
        df_inv = df_inv.replace('#{START_DT}', start_t)              
        df_inv = df_inv.replace('#{END_DT}', end_t)  
        df_inv=DB.read(df_inv,conn)
        
        df_isr="""
            SELECT A.ETF_MKT_BIG '구분(대)', A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=2) A
            """
        df_isr = df_isr.replace('#{START_DT}', start_t)              
        df_isr = df_isr.replace('#{END_DT}', end_t)  
        df_isr=DB.read(df_isr,conn)
        
        df_bnk="""
            SELECT  A.ETF_MKT_BIG '구분(대)', A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=4) A
            """
        df_bnk = df_bnk.replace('#{START_DT}', start_t)              
        df_bnk = df_bnk.replace('#{END_DT}', end_t)  
        df_bnk=DB.read(df_bnk,conn)
        
        df_inv_ace="""
            SELECT A.ETF_MKT_BIG '구분(대)', A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',round((A.AMT)/10000,0) ' 개인(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=8
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
        df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
        df_inv_ace=DB.read(df_inv_ace,conn)
    
        df_isr_ace="""
            SELECT A.ETF_MKT_BIG '구분(대)', A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
            (select
            	DISTINCT ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=2
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
        df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
        df_isr_ace=DB.read(df_isr_ace,conn)
    
        df_bnk_ace="""
            SELECT A.ETF_MKT_BIG '구분(대)', A.ETF_AST_MID '구분(중)',A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
            (select
            	DISTINCT 
                ETF_MKT_BIG,
                ETF_AST_MID,
            	ETF_AST_SML,
            	SUM(NET_AMT) OVER (PARTITION BY ETF_MKT_BIG, ETF_AST_MID,
            	ETF_AST_SML) AMT
            From
            	ES_SECTOR_MASTER A,
            	FN_ETFINV B
            WHERE
            	A.STK_CD = B.ETF_CD
            	AND ETF_AST_BIG NOT IN ('주식','채권')
                AND B.INVEST_GB=4
                AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
            """
        df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
        df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
        df_bnk_ace=DB.read(df_bnk_ace,conn)
    
        
        df_aum="""
       	SELECT
    	DISTINCT 
        ETF_MKT_BIG '구분(대)',
    	ETF_AST_MID '구분(중)',
    	ETF_AST_SML '구분(소)',
    	ROUND(SUM(AUM) OVER (PARTITION BY 
        ETF_MKT_BIG,
    	ETF_AST_MID,
    	ETF_AST_SML)/100000000,0) '기초(AUM)',
    	COUNT(B.etf_cd) OVER (PARTITION BY 
        ETF_MKT_BIG,                 
    	ETF_AST_MID,
    	ETF_AST_SML) '기초(개수)'
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_AST_BIG NOT IN ('주식','채권')
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
        AND B.ETF_CD = C.ETF_CD
        AND C.TR_YMD = B.TR_YMD
            """
        df_aum = df_aum.replace('#{START_DT}', start_t)                          
        df_aum=DB.read(df_aum,conn)
        
        
        df_ace_aum="""
       	SELECT
        	DISTINCT 
            ETF_MKT_BIG '구분(대)',
        	ETF_AST_MID '구분(중)',
        	ETF_AST_SML '구분(소)',
        	ROUND(SUM(AUM) OVER (PARTITION BY 
            ETF_MKT_BIG,                
        	ETF_AST_MID,
        	ETF_AST_SML)/100000000,0) ' 기초(AUM)',
        	COUNT(A.STK_CD) OVER (PARTITION BY 
        	ETF_MKT_BIG,
            ETF_AST_MID,
        	ETF_AST_SML) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_AST_BIG NOT IN ('주식','채권')
        	AND ETF_MKT_MID <> ''
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum = df_ace_aum.replace('#{START_DT}', start_t)                          
        df_ace_aum=DB.read(df_ace_aum,conn)
        
    
        df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_ace_aum, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_inv_ace, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_isr_ace, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])
        df_main=pd.merge(left = df_main , right = df_bnk_ace, how = "left", on = ['구분(대)',"구분(중)","구분(소)"])     
        
        df_main=df_main.fillna(0)
    
        df_main['ΔAUM']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
        df_main[' ΔAUM']=round(df_main[' 기말(AUM)']-df_main[' 기초(AUM)'],0)
        df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)
        df_main[' Δ개수']=round(df_main[' 기말(개수)']-df_main[' 기초(개수)'],0)
        
        df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['기초(M/S)']=100*round(df_main[' 기초(AUM)']/df_main['기초(AUM)'].sum(),3)
        df_main['기말(M/S)']=100*round(df_main[' 기말(AUM)']/df_main['기말(AUM)'].sum(),3)
        df_main['ΔM/S']=round(df_main['기말(M/S)']-df_main['기초(M/S)'],2)
        
        ##레버리지
        
        df_lev="""
            SELECT A.ETF_AST_SML '구분(소)',ROUND(A.AUM_SUM,0) '기말(AUM)',A.ETF_CNT '기말(개수)',ROUND(A.AVG_FEE*100,0) '평균보수(BP)',ROUND(A.AVG_AUM,2) '평균AUM',ROUND(A.SELL_SUM,2) '매출액(합,억원)',ROUND(B.AUM_SUM,0) " 기말(AUM)" ,B.ETF_CNT " 기말(개수)" ,round(100*B.AUM_SUM/A.AUM_SUM,2) "기말(M/S)",ROUND(B.AVG_FEE*100,0) " 평균보수" ,CASE WHEN B.AVG_FEE IS NULL THEN '' ELSE (CASE WHEN A.AVG_FEE>B.AVG_FEE THEN '시장보다 낮음' 
                                                              WHEN A.AVG_FEE<B.AVG_FEE THEN '시장보다 높음'
                                                              ELSE '시장과 동일' END) END "ACE 평균보수율",ROUND(B.SELL_SUM,2) " 매출액(합,억원)",ROUND(B.AVG_AUM,2) " 평균AUM"  FROM (SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	 ETF_AST_BIG NOT IN ('주식','채권')
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD) A LEFT OUTER JOIN 
    	(SELECT
    	DISTINCT 
    	CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML ,
    	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 AUM_SUM,
    	COUNT(STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ETF_CNT,
    	AVG(TOTAL_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_FEE,
    	AVG(AUM/100000000) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AVG_AUM,
    	SUM(AUM*C.MANG_FEE) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/10000000000 SELL_SUM
    FROM
    	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
    WHERE
    	ETF_AST_BIG NOT IN ('주식','채권')
    	AND ETF_MKT_MID <> ''
        AND B.ETF_CD = A.STK_CD
        AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFDATA WHERE TR_YMD<=GETDATE())
        AND B.ETF_CD = C.ETF_CD
        AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
        AND C.TR_YMD = B.TR_YMD
        AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) B ON A.ETF_AST_SML=B.ETF_AST_SML
            """
            
            #sql = sql.replace('#{START_DT}', trd_dt)  
            
        
        df_lev=DB.read(df_lev,conn)
        
        df_inv_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
            AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev = df_inv_lev.replace('#{START_DT}', start_t)              
        df_inv_lev = df_inv_lev.replace('#{END_DT}', end_t)  
        df_inv_lev = DB.read(df_inv_lev,conn)
        
        df_isr_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
         	AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev = df_isr_lev.replace('#{START_DT}', start_t)              
        df_isr_lev = df_isr_lev.replace('#{END_DT}', end_t)  
        df_isr_lev = DB.read(df_isr_lev,conn)
        
        df_bnk_lev="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 '은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
         	AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev = df_bnk_lev.replace('#{START_DT}', start_t)              
        df_bnk_lev = df_bnk_lev.replace('#{END_DT}', end_t)  
        df_bnk_lev = DB.read(df_bnk_lev,conn)
        
        df_inv_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 개인(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
         	AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=8
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_inv_lev_ace = df_inv_lev_ace.replace('#{START_DT}', start_t)              
        df_inv_lev_ace = df_inv_lev_ace.replace('#{END_DT}', end_t)  
        df_inv_lev_ace = DB.read(df_inv_lev_ace,conn)
    
        df_isr_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 보험(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
         	AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=2
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_isr_lev_ace = df_isr_lev_ace.replace('#{START_DT}', start_t)              
        df_isr_lev_ace = df_isr_lev_ace.replace('#{END_DT}', end_t)  
        df_isr_lev_ace = DB.read(df_isr_lev_ace,conn)
    
        df_bnk_lev_ace="""
            SELECT A.ETF_AST_SML '구분(소)',(A.AMT)/10000 ' 은행(억)' FROM 
        (select
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END ETF_AST_SML,
        	SUM(NET_AMT) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) AMT
        From
        	ES_SECTOR_MASTER A,
        	FN_ETFINV B,
        	FN_ETFINFO C
        WHERE
        	A.STK_CD = B.ETF_CD
        	AND B.TR_YMD BETWEEN '#{START_DT}' AND '#{END_DT}'
         	AND ETF_AST_BIG NOT IN ('주식','채권')
        	AND B.ETF_CD = C.ETF_CD
            AND B.INVEST_GB=4
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND C.TR_YMD = B.TR_YMD) A
            """
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{START_DT}', start_t)              
        df_bnk_lev_ace = df_bnk_lev_ace.replace('#{END_DT}', end_t)  
        df_bnk_lev_ace = DB.read(df_bnk_lev_ace,conn)
    
        
        df_aum_lev="""
            SELECT
         	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
         	ROUND(SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000,0) '기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) '기초(개수)'
         FROM
         	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
         WHERE
         	ETF_AST_BIG NOT IN ('주식','채권')
         	AND ETF_MKT_MID <> ''
         	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
             AND B.ETF_CD = A.STK_CD
             AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
             AND B.ETF_CD = C.ETF_CD
             AND C.TR_YMD = B.TR_YMD
            """
        df_aum_lev = df_aum_lev.replace('#{START_DT}', start_t)                          
        df_aum_lev = DB.read(df_aum_lev,conn)
        
        
        df_ace_aum_lev="""
         SELECT
        	DISTINCT CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END '구분(소)',
        	SUM(AUM) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END)/100000000 ' 기초(AUM)',
             COUNT(A.STK_CD) OVER (PARTITION BY CASE WHEN (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%') THEN '레버리지/인버스ETF' ELSE '액티브 ETF' END) ' 기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	ETF_AST_BIG NOT IN ('주식','채권')
        	AND ETF_MKT_MID <> ''
        	AND (C.ETF_NM LIKE '%레버리지%' OR C.ETF_NM LIKE '%인버스%' OR C.ETF_NM LIKE '%액티브%' )
            AND B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
            """
        df_ace_aum_lev = df_ace_aum_lev.replace('#{START_DT}', start_t)                          
        df_ace_aum_lev = DB.read(df_ace_aum_lev,conn)
        
    
        df_lev=pd.merge(left = df_lev , right = df_inv_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_aum_lev, how = "left", on =  ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_ace_aum_lev, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_inv_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_isr_lev_ace, how = "left", on = ["구분(소)"])
        df_lev=pd.merge(left = df_lev , right = df_bnk_lev_ace, how = "left", on = ["구분(소)"])
        
        
        df_lev=df_lev.fillna(0)
        
        df_lev['ΔAUM']=round(df_lev['기말(AUM)']-df_lev['기초(AUM)'],0)
        df_lev[' ΔAUM']=round(df_lev[' 기말(AUM)']-df_lev[' 기초(AUM)'],0)
        
        df_lev['Δ개수']=round(df_lev['기말(개수)']-df_lev['기초(개수)'],0)
        df_lev[' Δ개수']=round(df_lev[' 기말(개수)']-df_lev[' 기초(개수)'],0)
        
        df_lev['M/S']=100*round(df_lev['기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['기초(M/S)']=100*round(df_lev[' 기초(AUM)']/df_lev['기초(AUM)'].sum(),3)
        df_lev['기말(M/S)']=100*round(df_lev[' 기말(AUM)']/df_lev['기말(AUM)'].sum(),3)
        df_lev['ΔM/S']=round(df_lev['기말(M/S)']-df_lev['기초(M/S)'],2)
        
        
        st.markdown(""" <style> .font {
        font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">국내 주식형 ETF 현황</p>', unsafe_allow_html=True) 
           
        custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
        
        gridOptions = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions3 = GridOptionsBuilder.from_dataframe(df_main)
        gridOptions2 = GridOptionsBuilder.from_dataframe(df_lev)
        gridOptions4 = GridOptionsBuilder.from_dataframe(df_lev)
        
        gridOptions.configure_side_bar()
        gridOptions2.configure_side_bar()
        gridOptions3.configure_side_bar()
        gridOptions4.configure_side_bar()
        
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value > 0) {
                return {
                    'color': 'blue',
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
    
        
        jscode=JsCode("""
        function(params) {
            if (params.node.rowPinned === 'bottom') {
                return {  'color': 'black',
                          'backgroundColor': 'white',
                          'font-weight': 'bold' };
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
        
       
        gb = gridOptions.build()
        gb2 = gridOptions2.build()
        gb3 = gridOptions3.build()
        gb4 = gridOptions4.build()
    
        
        gb['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb2['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb3['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_main['기초(AUM)'].sum(),'기말(AUM)':df_main['기말(AUM)'].sum(),'ΔAUM':df_main['ΔAUM'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),' 기초(개수)':df_main[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_main[' 기말(개수)'].sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),' Δ개수':df_main[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),' 기초(AUM)':df_main[' 기초(AUM)'].sum(),' 기말(AUM)':df_main[' 기말(AUM)'].sum(),' ΔAUM':df_main[' ΔAUM'].sum(),' 매출액(합,억원)':df_main[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_main[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_main['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_main['기말(M/S)'].sum(),'font-weight': 'bold'}]
        gb4['pinnedBottomRowData'] = [{'구분(소)':'합계','기초(AUM)':df_lev['기초(AUM)'].sum(),'기말(AUM)':df_lev['기말(AUM)'].sum(),'ΔAUM':df_lev['ΔAUM'].sum(),'기초(개수)':df_lev['기초(개수)'].astype(float).sum(),'기말(개수)':df_lev['기말(개수)'].astype(float).sum(),' 기초(개수)':df_lev[' 기초(개수)'].astype(float).sum(),' 기말(개수)':df_lev[' 기말(개수)'].astype(float).sum(),'Δ개수':df_lev['Δ개수'].astype(float).sum(),' Δ개수':df_lev[' Δ개수'].astype(float).sum(),'매출액(합,억원)':df_lev['매출액(합,억원)'].sum(),' 기초(AUM)':df_lev[' 기초(AUM)'].sum(),' 기말(AUM)':df_lev[' 기말(AUM)'].sum(),' ΔAUM':df_lev[' ΔAUM'].sum(),' 매출액(합,억원)':df_lev[' 매출액(합,억원)'].sum(),'font-weight': 'bold','개인(억)':df_lev['개인(억)'].sum(),'font-weight': 'bold',' 개인(억)':df_lev[' 개인(억)'].sum(),'font-weight': 'bold','기초(M/S)':df_lev['기초(M/S)'].sum(),'font-weight': 'bold','기말(M/S)':df_lev['기말(M/S)'].sum(),'font-weight': 'bold'}]
        
        gb['getRowStyle'] = jscode
        gb2['getRowStyle'] = jscode
        gb3['getRowStyle'] = jscode
        gb4['getRowStyle'] = jscode
        
        gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important' }, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
        gb2['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말(AUM)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':100,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
        
       
        gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분(대)','width':100}, { 'field': '구분(중)','width':100,'background-color': '#1b6d85 !important'}, { 'field': '구분(소)','width':100 } ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        gb4['columnDefs'] = [ {  'headerClass': 'blank', 'children': [ { 'field': '' ,'width':100} ,{ 'field': '','width':100} ,{ 'field': '구분(소)','width':100} ] }, 
                             { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': ' 기초(AUM)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': ' 기말(AUM)','width':100,'valueFormatter':value2},{'field': ' ΔAUM','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': '기초(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100},{ 'field': '기말(M/S)','valueFormatter':"x.toLocaleString()+'%'",'precision':2,'width':100 },{ 'field': 'ΔM/S','width':70,'valueFormatter':"x.toLocaleString()+'%'","cellStyle":cellsytle_jscode}, { 'field': ' 기초(개수)','width':90,"valueFormatter":value2 }, { 'field': ' 기말(개수)','width':90,"valueFormatter":value2 },{'field': ' Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode}, { 'field': ' 평균보수','width':100 ,"valueFormatter":value2 }, { 'field': ' 평균AUM' ,'width':100,"valueFormatter":value2}, { 'field': ' 매출액(합,억원)','width':100,"valueFormatter":value2},{'field': ' 개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode} ] }] 
        
        
        #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
        AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)      
        AgGrid(df_lev, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)
        AgGrid(df_main, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        AgGrid(df_lev, gridOptions=gb4,custom_css=custom_css ,allow_unsafe_jscode=True,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,height=170)

    def all(self):
            
            df_main="""
                SELECT
        	DISTINCT CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END '구분',
        	round(SUM(AUM) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/100000000,0)  '기말(AUM)',
        	COUNT(STK_CD) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)  '기말(개수)',
        	round(AVG(TOTAL_FEE) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)*100,0) '평균보수(BP)',
        	round(AVG(AUM/100000000) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END),0) '평균AUM',
        	round(SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/10000000000,0) '매출액(합,억원)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	--ETF_MKT_BIG = '국내'
        	--AND ETF_AST_BIG ='주식'
        	 --ETF_MKT_MID <> ''
             B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
                """
                
            df_main = df_main.replace('#{END_DT}', end_t)  
            
            
            df_main=DB.read(df_main,conn)
            
            
            
            df_inv="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '개인(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=8) A
                """
            df_inv = df_inv.replace('#{START_DT}', start_t)              
            df_inv = df_inv.replace('#{END_DT}', end_t)  
            df_inv=DB.read(df_inv,conn)
            
            df_isr="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '보험(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=2) A
                """
            df_isr = df_isr.replace('#{START_DT}', start_t)              
            df_isr = df_isr.replace('#{END_DT}', end_t)  
            df_isr=DB.read(df_isr,conn)
            
            df_bnk="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '은행(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=4) A
                """
            df_bnk = df_bnk.replace('#{START_DT}', start_t)              
            df_bnk = df_bnk.replace('#{END_DT}', end_t)  
            df_bnk=DB.read(df_bnk,conn)
            
            
            df_aum="""
           	SELECT
        	DISTINCT 
        	CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END '구분',
        	ROUND(SUM(AUM) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/100000000,0) '기초(AUM)',
        	COUNT(B.etf_cd) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) '기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	--ETF_MKT_BIG = '국내'
        	--AND ETF_AST_BIG ='주식'
        	 --ETF_MKT_MID <> ''
             B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
                """
            df_aum = df_aum.replace('#{START_DT}', start_t)                          
            df_aum=DB.read(df_aum,conn)
            
           
            df_main=pd.merge(left = df_main , right = df_inv, how = "left", on = ["구분"])
            df_main=pd.merge(left = df_main , right = df_isr, how = "left", on = ["구분"])
            df_main=pd.merge(left = df_main , right = df_bnk, how = "left", on = ["구분"])
            df_main=pd.merge(left = df_main , right = df_aum, how = "left", on =  ["구분"])

            df_main=df_main.fillna(0)
    
            df_main['ΔAUM(억)']=round(df_main['기말(AUM)']-df_main['기초(AUM)'],0)
            df_main['Δ개수']=round(df_main['기말(개수)']-df_main['기초(개수)'],0)          
            df_main['M/S']=100*round(df_main['기말(AUM)']/df_main['기말(AUM)'].sum(),3)

            df_main['기말(AUM)']=df_main['기말(AUM)']/10000
            df_main['기초(AUM)']=df_main['기초(AUM)']/10000

            
            df_main.rename(columns={'기말(AUM)':'기말AUM(조)'},inplace=True)
            df_main.rename(columns={'기초(AUM)':'기초AUM(조)'},inplace=True)
            
            df_ace="""
                SELECT
        	DISTINCT CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END '구분',
        	round(SUM(AUM) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/100000000,0)  '기말(AUM)',
        	COUNT(STK_CD) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)  '기말(개수)',
        	round(AVG(TOTAL_FEE) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)*100,0) '평균보수(BP)',
        	round(AVG(AUM/100000000) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END),0) '평균AUM',
        	round(SUM(AUM*C.MANG_FEE) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/10000000000,0) '매출액(합,억원)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	--ETF_MKT_BIG = '국내'
        	--AND ETF_AST_BIG ='주식'
        	 --ETF_MKT_MID <> ''
             B.ETF_CD = A.STK_CD
            AND B.TR_YMD='#{END_DT}'
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                """
                
            df_ace = df_ace.replace('#{END_DT}', end_t)  
            
            
            df_ace=DB.read(df_ace,conn)
            
            
            
            df_inv_ace="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '개인(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=8
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_inv_ace = df_inv_ace.replace('#{START_DT}', start_t)              
            df_inv_ace = df_inv_ace.replace('#{END_DT}', end_t)  
            df_inv_ace=DB.read(df_inv_ace,conn)
            
            df_isr_ace="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '보험(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=2
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_isr_ace = df_isr_ace.replace('#{START_DT}', start_t)              
            df_isr_ace = df_isr_ace.replace('#{END_DT}', end_t)  
            df_isr_ace=DB.read(df_isr_ace,conn)
            
            df_bnk_ace="""
                SELECT A.GB '구분',ROUND((A.AMT)/10000,0) '은행(억)' FROM 
                (select
                	DISTINCT 
                    CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END 'GB',
                	SUM(NET_AMT) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) AMT
                From
                	ES_SECTOR_MASTER A,
                	FN_ETFINV B
                WHERE
                	A.STK_CD = B.ETF_CD
                	AND B.TR_YMD between '#{START_DT}' and '#{END_DT}'
                	--AND ETF_MKT_BIG = '국내'
                	--AND ETF_AST_BIG = '주식'
                    AND B.INVEST_GB=4
                    AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)) A
                """
            df_bnk_ace = df_bnk_ace.replace('#{START_DT}', start_t)              
            df_bnk_ace = df_bnk_ace.replace('#{END_DT}', end_t)  
            df_bnk_ace=DB.read(df_bnk_ace,conn)
            
            
            df_aum_ace="""
           	SELECT
        	DISTINCT 
        	CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END '구분',
        	ROUND(SUM(AUM) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END)/100000000,0) '기초(AUM)',
        	COUNT(B.etf_cd) OVER (PARTITION BY 
            CASE WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='주식' THEN '국내주식'
        	              WHEN ETF_MKT_BIG='국내' AND ETF_AST_BIG ='채권' THEN '국내채권'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='주식' THEN '해외주식'
        	              WHEN ETF_MKT_BIG='해외' AND ETF_AST_BIG ='채권' THEN '해외채권'
        	              ELSE '기타' END) '기초(개수)'
        FROM
        	ES_SECTOR_MASTER A, FN_ETFDATA B, FN_ETFINFO C
        WHERE
        	--ETF_MKT_BIG = '국내'
        	--AND ETF_AST_BIG ='주식'
        	 --ETF_MKT_MID <> ''
             B.ETF_CD = A.STK_CD
            AND B.TR_YMD= (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
            AND B.ETF_CD = C.ETF_CD
            AND C.TR_YMD = B.TR_YMD
            AND A.STK_CD IN (SELECT STK_CD FROM ES_FUND_MAP)
                """
            df_aum_ace = df_aum_ace.replace('#{START_DT}', start_t)                          
            df_aum_ace=DB.read(df_aum_ace,conn)
            
           
            df_ace=pd.merge(left = df_ace , right = df_inv_ace, how = "left", on = ["구분"])
            df_ace=pd.merge(left = df_ace , right = df_isr_ace, how = "left", on = ["구분"])
            df_ace=pd.merge(left = df_ace , right = df_bnk_ace, how = "left", on = ["구분"])
            df_ace=pd.merge(left = df_ace , right = df_aum_ace, how = "left", on =  ["구분"])

            df_ace=df_ace.fillna(0)
    
            df_ace['ΔAUM(억)']=round((df_ace['기말(AUM)']-df_ace['기초(AUM)']),0)
            df_ace['Δ개수']=round(df_ace['기말(개수)']-df_ace['기초(개수)'],0)          
            df_ace['M/S']=100*round(df_ace['기말(AUM)']/df_ace['기말(AUM)'].sum(),3)  
            df_ace['기말(AUM)']=df_ace['기말(AUM)']/10000
            df_ace['기초(AUM)']=df_ace['기초(AUM)']/10000

            
            df_ace.rename(columns={'기말(AUM)':'기말AUM(조)'},inplace=True)
            df_ace.rename(columns={'기초(AUM)':'기초AUM(조)'},inplace=True)
            #df_ace=df_ace.sort_values(by=['기말AUM(조)'],axis=0,ascending=False).reset_index()
            
            st.markdown(""" <style> .font {
            font-size:20px ; font-family: 'Cooper Black'; color: #000000;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">시장 현황</p>', unsafe_allow_html=True) 
               
            custom_css = {
                #".ag-row-hover": {"background-color": "red !important"},
                #".ag-header-cell-label": {"background-color": "orange !important"},
                #".ag-header":{"background-color": "#d0cece !important"},
                ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
                ".all": {"background-color": "#d0cece !important","color":"black !important"},
                ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
                ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
            
            gridOptions = GridOptionsBuilder.from_dataframe(df_main)
            gridOptions3 = GridOptionsBuilder.from_dataframe(df_ace)

            
            gridOptions.configure_side_bar()
            gridOptions3.configure_side_bar()
            
            cellsytle_jscode = JsCode("""
            function(params) {
                if (params.value > 0) {
                    return {
                        'color': 'blue',
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
     
            
            jscode=JsCode("""
            function(params) {
                if (params.node.rowPinned === 'bottom') {
                    return {  'color': 'black',
                              'backgroundColor': 'white',
                              'font-weight': 'bold' };
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
            
           
            gb = gridOptions.build()
            gb3 = gridOptions3.build()
    
            
            gb['pinnedBottomRowData'] = [{'구분':'합계','기초AUM(조)':df_main['기초AUM(조)'].sum(),'기말AUM(조)':df_main['기말AUM(조)'].sum(),'ΔAUM(억)':df_main['ΔAUM(억)'].sum(),'기초(개수)':df_main['기초(개수)'].astype(float).sum(),'기말(개수)':df_main['기말(개수)'].astype(float).sum(),'Δ개수':df_main['Δ개수'].astype(float).sum(),'매출액(합,억원)':df_main['매출액(합,억원)'].sum(),'개인(억)':df_main['개인(억)'].sum(),'font-weight': 'bold','은행(억)':df_main['은행(억)'].sum(),'font-weight': 'bold','보험(억)':df_main['보험(억)'].sum(),'font-weight': 'bold'}]
            gb3['pinnedBottomRowData'] = [{'구분':'합계','기초AUM(조)':df_ace['기초AUM(조)'].sum(),'기말AUM(조)':df_ace['기말AUM(조)'].sum(),'ΔAUM(억)':df_ace['ΔAUM(억)'].sum(),'기초(개수)':df_ace['기초(개수)'].astype(float).sum(),'기말(개수)':df_ace['기말(개수)'].astype(float).sum(),'Δ개수':df_ace['Δ개수'].astype(float).sum(),'매출액(합,억원)':df_ace['매출액(합,억원)'].sum(),'개인(억)':df_ace['개인(억)'].sum(),'font-weight': 'bold','은행(억)':df_ace['은행(억)'].sum(),'font-weight': 'bold','보험(억)':df_ace['보험(억)'].sum(),'font-weight': 'bold'}]
             
            gb['getRowStyle'] = jscode
            gb3['getRowStyle'] = jscode
          
            gb['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분','width':100} ] }, 
                        { 'headerName': '전체ETF','headerClass': 'all', 'children': [{'field': '기초AUM(조)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말AUM(조)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':120,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '은행(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '보험(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
            
        
           
            gb3['columnDefs'] = [ { 'headerClass': 'blank', 'children': [ { 'field': '구분','width':100} ] }, 
                                  { 'headerName': 'ACE ETF','headerClass': 'ace', 'children': [{'field': '기초AUM(조)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말AUM(조)','width':100,'valueFormatter':value2},{ 'field': 'M/S','width':70,'valueFormatter':"x.toLocaleString()+'%'",'precision':2},{'field': 'ΔAUM(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '기초(개수)','width':90,"valueFormatter":value2},{'field': '기말(개수)','width':90,"valueFormatter":value2},{'field': 'Δ개수','width':70,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '평균보수(BP)','width':100,"valueFormatter":value2},{'field': '평균AUM','width':100,'valueFormatter':value2},{'field': '매출액(합,억원)' ,'width':120,'valueFormatter':value2},{'field': '개인(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '은행(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': '보험(억)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
            
            #gb.configure_column("ACE M/S", type=["numericColumn"], precision=2, aggFunc='sum')                    
            AgGrid(df_main, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True,height=250)      
            AgGrid(df_ace, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,height=250)
