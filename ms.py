# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:47:20 2023

@author: user
"""
import plotly.express as px
import plotly.graph_objects as go
import DB
import datetime
import seaborn as sns
import pandas as pd
now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d')


def mschg(start_dt=now,end_dt=now):
    sql="""
    SELECT * fROM (SELECT TR_YMD,CO_NM,NAV,MS,RANK() OVER (PARTITION BY TR_YMD ORDER BY MS DESC) RK FROM (SELECT A.TR_YMD,CO_NM,MS NAV,MS/MS.NAV MS FROM
    (SELECT TR_YMD,
    	CO_NM,
    	SUM(NAV) MS
    FROM
    	(
    	SELECT A.TR_YMD,
    		A.ETF_CD,
    		A.ETF_NM,
    		A.CO_NM,
    		B.ETF_NA_AMT / 100 NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD BETWEEN '#{START_DT}' AND '#{end_DT}'
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD) A   GROUP BY CO_NM,TR_YMD )A , (SELECT DISTINCT A.TR_YMD,
    		SUM(B.ETF_NA_AMT / 100) OVER (PARTITION BY A.TR_YMD) NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD BETWEEN '#{START_DT}' AND '#{end_DT}'
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD) MS
    		WHERE A.TR_YMD=MS.TR_YMD) A ) A
    		WHERE A.RK<=8
    """
    
    sql = sql.replace('#{START_DT}', start_dt)  
    sql = sql.replace('#{end_DT}', end_dt)  
    
    conn=DB.conn()

    data=DB.read(sql,conn)
    data['TR_YMD'] = pd.to_datetime(data['TR_YMD'], format='%Y%m%d')
    data['TR_YMD'] = data['TR_YMD'].dt.strftime('%Y-%m-%d')
    
    fig_daily=px.line(data,x="TR_YMD",y='MS',color="CO_NM",title="MS추이" )
    fig_daily.update_layout(title='MS추이')
    
    
    return fig_daily

def msfig(trd_dt=now):
    sql="""
    SELECT TOP 8 CO_NM,MS NAV,MS*100/(SELECT
    		SUM(B.ETF_NA_AMT / 100) NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD) MS FROM
    (SELECT
    	CO_NM,
    	SUM(NAV) MS
    FROM
    	(
    	SELECT
    		A.ETF_CD,
    		A.ETF_NM,
    		A.CO_NM,
    		B.ETF_NA_AMT / 100 NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD) A   GROUP BY CO_NM )A 
    order by MS DESC
    """
    
    sql = sql.replace('#{START_DT}', trd_dt)  
    
    conn=DB.conn()

    data=DB.read(sql,conn)
    
    fig=px.bar(data,x='CO_NM',y='MS',color='CO_NM',text ='MS')
    fig.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    
    fig.update_layout(title='MS')
    
    
    return fig
    
def msfig_kor(trd_dt=now):
    sql="""
    SELECT TOP 8 CO_NM,MS NAV,MS*100/(SELECT
    		SUM(B.ETF_NA_AMT / 100) NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD AND (A.CLASS_BIG LIKE '%국내%' OR A.CLASS_BIG LIKE '%기타%')) MS FROM
    (SELECT
    	CO_NM,
    	SUM(NAV) MS
    FROM
    	(
    	SELECT
    		A.ETF_CD,
    		A.ETF_NM,
    		A.CO_NM,
    		B.ETF_NA_AMT / 100 NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD AND (A.CLASS_BIG LIKE '%국내%' OR A.CLASS_BIG LIKE '%기타%')) A   GROUP BY CO_NM )A 
    order by MS DESC
    """
    
    sql = sql.replace('#{START_DT}', trd_dt)  
    
    conn=DB.conn()

    data=DB.read(sql,conn)
    
    fig=px.bar(data,x='CO_NM',y='MS',color='CO_NM',text ='MS')
    fig.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    
    fig.update_layout(title='MS')
    
    
    return fig

def msfig_glo(trd_dt=now):
    sql="""
    SELECT TOP 8 CO_NM,MS NAV,MS*100/(SELECT
    		SUM(B.ETF_NA_AMT / 100) NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD AND A.CLASS_BIG LIKE '%해외%') MS FROM
    (SELECT
    	CO_NM,
    	SUM(NAV) MS
    FROM
    	(
    	SELECT
    		A.ETF_CD,
    		A.ETF_NM,
    		A.CO_NM,
    		B.ETF_NA_AMT / 100 NAV
    	FROM
    		FN_ETFINFO A,
    		FN_ETFDATA B
    	WHERE
    		A.TR_YMD = (SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<='#{START_DT}')
    		AND A.TR_YMD = B.TR_YMD
    		AND A.ETF_CD = B.ETF_CD AND A.CLASS_BIG LIKE '%해외%') A   GROUP BY CO_NM )A 
    order by MS DESC
    """
    
    sql = sql.replace('#{START_DT}', trd_dt)  
    
    conn=DB.conn()

    data=DB.read(sql,conn)
    
    fig=px.bar(data,x='CO_NM',y='MS',color='CO_NM',text ='MS')
    fig.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    
    fig.update_layout(title='MS')
    
    
    return fig

