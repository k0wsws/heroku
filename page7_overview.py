# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 07:57:18 2023

@author: user
"""

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme
import pickle
from PIL import Image
from datetime import date,timedelta,datetime
from pday import Pday
import load 
logo = Image.open('ace.jpg') 
now = datetime.now()
pweek = now-timedelta(7)
pmonth = now-timedelta(30)
root='C:\\Users\\user\\Dashboard\\dataset\\'

   

###데이터 불러오기
investor, aum_raw, aum_ace_raw, investor_ace, aum_ace_all, aum_rev = load.load_data()


def aum_load():
    
    # ##데이터 불러오기
    # investor=pickle.load(open(root+'investor.pkl','rb'))   
    # aum_raw=pickle.load(open(root+'aum_raw.pkl','rb'))   
    # aum_ace_raw=pickle.load(open(root+'aum_ace.pkl','rb'))   
    # investor_ace=pickle.load(open(root+'investor_ace.pkl','rb'))   
    # aum_ace_all=pickle.load(open(root+'aum_ace_all.pkl','rb')) 
    # aum_rev=pickle.load(open(root+'aum_rev.pkl','rb'))  
    # aum_rev=aum_rev.sort_values(by='TR_YMD',axis=0)
    
    
    
    e1,col1,e2,e3, col2 = st.columns( [0.1,0.1,0.1,0.5, 0.2])
    
    with col1:   
       
        start = st.date_input(
            "기초일",pmonth)
        start=str(start).replace("-", "")[0:8]  
    with e2:
        end = st.date_input(
            "기말일",Pday())
        end=str(end).replace("-", "")[0:8]
    with col2:               # To display brand log
            st.image(logo, width=200 )


    aum=pickle.load(open(root+'aum.pkl','rb'))  
    start=max(aum[aum['TR_YMD']<=start]['TR_YMD'])
    end=max(aum[aum['TR_YMD']<=end]['TR_YMD'])
    
    ##전체 오버뷰
    final=pd.merge(left = aum_rev[aum_rev['TR_YMD']==start] , right = aum_rev[aum_rev['TR_YMD']==end], how = "right", on = ["ETF_CD","CLASS"])
    final=pd.merge(left = final , right = aum_rev.groupby('ETF_CD')['기초AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    final=pd.merge(left = final , right = aum_rev.groupby('ETF_CD')['NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    final['Δ설정액(조)']=round(final['기초AUM_y']-final['기초AUM_x'].fillna(final['기초AUM'])*final['NAV_y']/final['NAV_x'].fillna(final['NAV']),2) 
    final2=pd.DataFrame()
    final2['기초AUM(조)']=round(final.groupby('CLASS')['기초AUM_x'].sum()/1000000000000,2)
    final2['기말AUM(조)']=round(final.groupby('CLASS')['기초AUM_y'].sum()/1000000000000,2)
    final2['ΔAUM(조)']=final2['기말AUM(조)']-final2['기초AUM(조)'].fillna(0)    
    final2['Δ설정액(조)']=round(final.groupby('CLASS')['Δ설정액(조)'].sum()/1000000000000,2)
    final2=final2.sort_values(by=['기말AUM(조)'],axis=0,ascending=False).reset_index()
    
    
    ##############전체#############
    ##순자산 상위
    aum=aum_raw.copy()
    aum['순위'] = aum.groupby('TR_YMD')['AUM'].rank(method='min',ascending=False)    
    aum.rename(columns={'ETF_NM':'펀드명'},inplace=True)
   # aum=aum[(aum['TR_YMD']==end)&(aum['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    aum=aum[(aum['TR_YMD']==end)].sort_values(by=['순위'],axis=0,ascending=True)
    
    ##수익률 상위
    prc_chg=pd.merge(left = aum_raw[aum_raw['TR_YMD']==start] , right = aum_raw[aum_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])  
    prc_chg=pd.merge(left = prc_chg , right = aum_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    prc_chg['수익률']=round(100*(prc_chg['ETF_NAV_y']/prc_chg['ETF_NAV_x'].fillna(prc_chg['ETF_NAV'])-1),2)
    prc_chg.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    prc_chg['순위'] = prc_chg['수익률'].rank(method='min',ascending=False)    
   # aum_chg=aum_chg[(aum_chg['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    prc_chg=prc_chg.sort_values(by=['순위'],axis=0,ascending=True)  
    
       ##순자산증감 상위
    aum_chg=pd.merge(left = aum_raw[aum_raw['TR_YMD']==start] , right = aum_raw[aum_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])  
    aum_chg=pd.merge(left = aum_chg , right = aum_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    aum_chg['Δ순자산']=round(aum_chg['AUM_y']-aum_chg['AUM_x'].fillna(aum_chg['AUM']),2)
    aum_chg.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    aum_chg['순위'] = aum_chg['Δ순자산'].rank(method='min',ascending=False)    
   # aum_chg=aum_chg[(aum_chg['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    aum_chg=aum_chg.sort_values(by=['순위'],axis=0,ascending=True)  
    
    ##순자산증감율%상위
  
    aum_chg_p=pd.merge(left = aum_raw[aum_raw['TR_YMD']==start] , right = aum_raw[aum_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    aum_chg_p=pd.merge(left = aum_chg_p , right = aum_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    aum_chg_p['Δ순자산(%)']=100*round((aum_chg_p['AUM_y']-aum_chg_p['AUM_x'].fillna(aum_chg_p['AUM']))/aum_chg_p['AUM_x'].fillna(aum_chg_p['AUM']),2)
    aum_chg_p.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    aum_chg_p['순위'] = aum_chg_p['Δ순자산(%)'].rank(method='min',ascending=False)    
    #aum_chg_p=aum_chg_p[(aum_chg_p['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    aum_chg_p=aum_chg_p.sort_values(by=['순위'],axis=0,ascending=True)  
   
    ##설정액 상위
    set_raw=pd.merge(left = aum_raw[aum_raw['TR_YMD']==start] , right = aum_raw[aum_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    set_raw=pd.merge(left = set_raw , right = aum_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    set_raw=pd.merge(left = set_raw , right = aum_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    set_raw['Δ설정액']=round(set_raw['AUM_y']-set_raw['AUM_x'].fillna(set_raw['AUM'])*set_raw['ETF_NAV_y']/set_raw['ETF_NAV_x'].fillna(set_raw['ETF_NAV']),2)
    set_raw.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    set_raw['순위'] = set_raw['Δ설정액'].rank(method='min',ascending=False)    
    #set_raw=set_raw[(set_raw['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    set_raw=set_raw.sort_values(by=['순위'],axis=0,ascending=True)  
    
    ##설정액증감률 상위
    set_raw_p=pd.merge(left = aum_raw[aum_raw['TR_YMD']==start] , right = aum_raw[aum_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    set_raw_p=pd.merge(left = set_raw_p , right = aum_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    set_raw_p=pd.merge(left = set_raw_p , right = aum_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    set_raw_p['Δ설정액(%)']=round(100*(round(set_raw_p['AUM_y']-set_raw_p['AUM_x'].fillna(set_raw_p['AUM'])*set_raw_p['ETF_NAV_y']/set_raw_p['ETF_NAV_x'].fillna(set_raw_p['ETF_NAV']),2))/set_raw_p['AUM_x'].fillna(set_raw_p['AUM']),0)
    set_raw_p.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    set_raw_p['순위'] = set_raw_p['Δ설정액(%)'].rank(method='min',ascending=False)    
    #set_raw_p=set_raw_p[(set_raw_p['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    set_raw_p=set_raw_p.sort_values(by=['순위'],axis=0,ascending=True)
    
    ##개인순매수 상위
    ant=investor[(investor['INVEST_GB']==8)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    ant=ant.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    ant['순위'] = ant['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    ant=ant.sort_values(by=['순위'],axis=0,ascending=True)
    ant.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    ant.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##외국인순매수 상위
    alien=investor[(investor['INVEST_GB']==9)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    alien=alien.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    alien['순위'] = alien['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    alien=alien.sort_values(by=['순위'],axis=0,ascending=True)
    alien.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    alien.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##기관순매수 상위
    corp=investor[(investor['INVEST_GB']==0)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    corp=corp.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    corp['순위'] = corp['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    corp=corp.sort_values(by=['순위'],axis=0,ascending=True)
    corp.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    corp.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##금융투자순매수 상위
    finv=investor[(investor['INVEST_GB']==1)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    finv=finv.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    finv['순위'] = finv['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    finv=finv.sort_values(by=['순위'],axis=0,ascending=True)
    finv.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    finv.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##보험순매수 상위
    ins=investor[(investor['INVEST_GB']==2)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    ins=ins.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    ins['순위'] = ins['NET_AMT'].rank(method='min',ascending=False)    
    #ins=ins[(ins['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    ins=ins.sort_values(by=['순위'],axis=0,ascending=True)
    ins.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    ins.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##투신순매수 상위
    trust=investor[(investor['INVEST_GB']==3)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    trust=trust.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    trust['순위'] = trust['NET_AMT'].rank(method='min',ascending=False)    
    #ins=ins[(ins['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    trust=trust.sort_values(by=['순위'],axis=0,ascending=True)
    trust.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    trust.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##은행순매수 상위
    bnk=investor[(investor['INVEST_GB']==4)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    bnk=bnk.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    bnk['순위'] = bnk['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    bnk=bnk.sort_values(by=['순위'],axis=0,ascending=True)
    bnk.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    bnk.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##연기금순매수 상위
    pens=investor[(investor['INVEST_GB']==6)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    pens=pens.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    pens['순위'] = pens['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    pens=pens.sort_values(by=['순위'],axis=0,ascending=True)
    pens.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    pens.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##연기금순매수 상위
    pef=investor[(investor['INVEST_GB']==31)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    pef=pef.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    pef['순위'] = pef['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    pef=pef.sort_values(by=['순위'],axis=0,ascending=True)
    pef.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    pef.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##기타법인순매수 상위
    etc=investor[(investor['INVEST_GB']==7)& (investor['TR_YMD']>=start)& (investor['TR_YMD']<=end)]
    etc=etc.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    etc['순위'] = etc['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    etc=etc.sort_values(by=['순위'],axis=0,ascending=True)
    etc.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    etc.rename(columns={'NET_AMT':'순매수'},inplace=True)
    ##############ACE################
    
    #final_ace=pd.merge(left = aum_ace_all[aum_ace_all['TR_YMD']=='20220106'] , right = aum_ace_all[aum_ace_all['TR_YMD']=='20230220'], how = "right", on = ["ETF_CD","CLASS"])
   
   ##ACE전체 오버뷰
    final_ace=pd.merge(left = aum_ace_all[aum_ace_all['TR_YMD']==start] , right = aum_ace_all[aum_ace_all['TR_YMD']==end], how = "right", on = ["ETF_CD","CLASS"])
    final_ace['Δ설정액(조)']=final_ace['기초AUM_y']-final_ace['기초AUM_x'].fillna(0)*final_ace['NAV_y']/final_ace['NAV_x'].fillna(1)
    final_ace2=pd.DataFrame()
    final_ace2['기초AUM(조)']=round(final_ace.groupby('CLASS')['기초AUM_x'].sum()/1000000000000,2)
    final_ace2['기말AUM(조)']=round(final_ace.groupby('CLASS')['기초AUM_y'].sum()/1000000000000,2)
    final_ace2['ΔAUM(조)']=final_ace2['기말AUM(조)']-final_ace2['기초AUM(조)'].fillna(0)  
    final_ace2['Δ설정액(조)']=round(final_ace.groupby('CLASS')['Δ설정액(조)'].sum()/1000000000000,2)
    final_ace2=final_ace2.sort_values(by=['기말AUM(조)'],axis=0,ascending=False).reset_index()
    
    ##ACE 순자산 상위
    aum_ace=aum_ace_raw.copy()
    aum_ace['순위'] = aum_ace.groupby('TR_YMD')['AUM'].rank(method='min',ascending=False) 
    aum_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    #aum_ace=aum_ace[(aum_ace['TR_YMD']==end)&(aum_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    aum_ace=aum_ace[(aum_ace['TR_YMD']==end)].sort_values(by=['순위'],axis=0,ascending=True)
    
    ##수익률 상위
    prc_chg_ace=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])  
    prc_chg_ace=pd.merge(left = prc_chg_ace , right = aum_ace_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    prc_chg_ace['수익률']=round(100*(prc_chg_ace['ETF_NAV_y']/prc_chg_ace['ETF_NAV_x'].fillna(prc_chg_ace['ETF_NAV'])-1),2)
    prc_chg_ace.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    prc_chg_ace['순위'] = prc_chg_ace['수익률'].rank(method='min',ascending=False)    
   # aum_chg=aum_chg[(aum_chg['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    prc_chg_ace=prc_chg_ace.sort_values(by=['순위'],axis=0,ascending=True) 
    
    ##ACE 순자산증감 상위
    aum_chg_ace=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    aum_chg_ace=pd.merge(left = aum_chg_ace , right = aum_ace_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])  
    aum_chg_ace['Δ순자산']=round(aum_chg_ace['AUM_y']-aum_chg_ace['AUM_x'].fillna(aum_chg_ace['AUM']),2)
    aum_chg_ace.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    aum_chg_ace['순위'] = aum_chg_ace['Δ순자산'].rank(method='min',ascending=False)    
    #aum_chg_ace=aum_chg_ace[(aum_chg_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True) 
    aum_chg_ace=aum_chg_ace.sort_values(by=['순위'],axis=0,ascending=True)
    
    ##순자산증감율%상위
    aum_chg_ace_p=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    aum_chg_ace_p=pd.merge(left = aum_chg_ace_p , right = aum_ace_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    aum_chg_ace_p['Δ순자산(%)']=100*round((aum_chg_ace_p['AUM_y']-aum_chg_ace_p['AUM_x'].fillna(aum_chg_ace_p['AUM']))/aum_chg_ace_p['AUM_x'].fillna(aum_chg_ace_p['AUM']),2)
    aum_chg_ace_p.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    aum_chg_ace_p['순위'] = aum_chg_ace_p['Δ순자산(%)'].rank(method='min',ascending=False)    
    #aum_chg_ace_p=aum_chg_ace_p[(aum_chg_ace_p['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    aum_chg_ace_p=aum_chg_ace_p.sort_values(by=['순위'],axis=0,ascending=True)
   
    ##설정액 상위
    set_ace=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    set_ace=pd.merge(left = set_ace , right = aum_ace_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    set_ace=pd.merge(left = set_ace , right = aum_ace_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
   
    set_ace['Δ설정액']=round(set_ace['AUM_y']-set_ace['AUM_x'].fillna(set_ace['AUM'])*set_ace['ETF_NAV_y']/set_ace['ETF_NAV_x'].fillna(set_ace['ETF_NAV']),2)
    set_ace.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    set_ace['순위'] = set_ace['Δ설정액'].rank(method='min',ascending=False)    
    #set_ace=set_ace[(set_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    set_ace=set_ace.sort_values(by=['순위'],axis=0,ascending=True)
    
    ##설정액증감률 상위
    set_ace_p=pd.merge(left = aum_ace_raw[aum_ace_raw['TR_YMD']==start] , right = aum_ace_raw[aum_ace_raw['TR_YMD']==end], how = "right", on = ["ETF_CD"])
    set_ace_p=pd.merge(left = set_ace_p , right = aum_ace_raw.groupby('ETF_CD')['AUM'].agg('first').reset_index(), how = "left", on = ["ETF_CD"])
    set_ace_p=pd.merge(left = set_ace_p , right = aum_ace_raw.groupby('ETF_CD')['ETF_NAV'].agg('first').reset_index(), how = "left", on = ["ETF_CD"]) 
    set_ace_p['Δ설정액(%)']=round(100*(round(set_ace_p['AUM_y']-set_ace_p['AUM_x'].fillna(set_ace_p['AUM'])*set_ace_p['ETF_NAV_y']/set_ace_p['ETF_NAV_x'].fillna(set_ace_p['ETF_NAV']),2))/set_ace_p['AUM_x'].fillna(set_ace_p['AUM']),0)
    set_ace_p.rename(columns={'ETF_NM_y':'펀드명'},inplace=True)
    set_ace_p['순위'] = set_ace_p['Δ설정액(%)'].rank(method='min',ascending=False)    
    #set_ace_p=set_ace_p[(set_ace_p['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)  
    set_ace_p=set_ace_p.sort_values(by=['순위'],axis=0,ascending=True)
    
    ##개인순매수 상위
    ant_ace=investor_ace[(investor_ace['INVEST_GB']==8)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    ant_ace=ant_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    ant_ace['순위'] = ant_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ant_ace=ant_ace[(ant_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    ant_ace=ant_ace.sort_values(by=['순위'],axis=0,ascending=True)
    ant_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    ant_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##외국인순매수 상위
    alien_ace=investor_ace[(investor_ace['INVEST_GB']==9)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    alien_ace=alien_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    alien_ace['순위'] = alien_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    alien_ace=alien_ace.sort_values(by=['순위'],axis=0,ascending=True)
    alien_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    alien_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##기관순매수 상위
    corp_ace=investor_ace[(investor_ace['INVEST_GB']==0)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    corp_ace=corp_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    corp_ace['순위'] = corp_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    corp_ace=corp_ace.sort_values(by=['순위'],axis=0,ascending=True)
    corp_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    corp_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##금융투자순매수 상위
    finv_ace=investor_ace[(investor_ace['INVEST_GB']==1)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    finv_ace=finv_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    finv_ace['순위'] = finv_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ant=ant[(ant['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    finv_ace=finv_ace.sort_values(by=['순위'],axis=0,ascending=True)
    finv_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    finv_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    
    ##보험순매수 상위
    ins_ace=investor_ace[(investor_ace['INVEST_GB']==2)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    ins_ace=ins_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    ins_ace['순위'] = ins_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ins_ace=ins_ace[(ins_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    ins_ace=ins_ace.sort_values(by=['순위'],axis=0,ascending=True)
    ins_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    ins_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##투신순매수 상위
    trust_ace=investor_ace[(investor_ace['INVEST_GB']==3)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    trust_ace=trust_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    trust_ace['순위'] = trust_ace['NET_AMT'].rank(method='min',ascending=False)    
    #ins=ins[(ins['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    trust_ace=trust_ace.sort_values(by=['순위'],axis=0,ascending=True)
    trust_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    trust_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##은행순매수 상위
    bnk_ace=investor_ace[(investor_ace['INVEST_GB']==4)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    bnk_ace=bnk_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    bnk_ace['순위'] = bnk_ace['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    bnk_ace=bnk_ace.sort_values(by=['순위'],axis=0,ascending=True)
    bnk_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    bnk_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##연기금순매수 상위
    pens_ace=investor_ace[(investor_ace['INVEST_GB']==6)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    pens_ace=pens_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    pens_ace['순위'] = pens_ace['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    pens_ace=pens_ace.sort_values(by=['순위'],axis=0,ascending=True)
    pens_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    pens_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##연기금순매수 상위
    pef_ace=investor_ace[(investor_ace['INVEST_GB']==31)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    pef_ace=pef_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    pef_ace['순위'] = pef_ace['NET_AMT'].rank(method='min',ascending=False)    
    #bnk=bnk[(bnk['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    pef_ace=pef_ace.sort_values(by=['순위'],axis=0,ascending=True)
    pef_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    pef_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
    ##기타법인순매수 상위
    etc_ace=investor_ace[(investor_ace['INVEST_GB']==7)& (investor_ace['TR_YMD']>=start)& (investor_ace['TR_YMD']<=end)]
    etc_ace=etc_ace.groupby(['ETF_NM','INVEST_GB']).sum().reset_index()
    etc_ace['순위'] = etc_ace['NET_AMT'].rank(method='min',ascending=False)    
    #bnk_ace=bnk_ace[(bnk_ace['순위']<=10)].sort_values(by=['순위'],axis=0,ascending=True)
    etc_ace=etc_ace.sort_values(by=['순위'],axis=0,ascending=True)
    etc_ace.rename(columns={'ETF_NM':'펀드명'},inplace=True)
    etc_ace.rename(columns={'NET_AMT':'순매수'},inplace=True)
    
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
            
    gridOptions = GridOptionsBuilder.from_dataframe(final2)
  #  gridOptions.configure_side_bar()

    gb = gridOptions.build()
    
    gridOptions2 = GridOptionsBuilder.from_dataframe(aum)
    gb2 = gridOptions2.build()
    
    gridOptions3 = GridOptionsBuilder.from_dataframe(ant)
    gb3 = gridOptions3.build()
    
    gridOptions4 = GridOptionsBuilder.from_dataframe(ins)
    gb4 = gridOptions4.build()
    
    gridOptions5 = GridOptionsBuilder.from_dataframe(bnk)
    gb5 = gridOptions5.build()
    
    gridOptions6 = GridOptionsBuilder.from_dataframe(aum_ace)
    gb6 = gridOptions6.build()
    
    gridOptions7 = GridOptionsBuilder.from_dataframe(ant_ace)
    gb7 = gridOptions7.build()
    
    gridOptions8 = GridOptionsBuilder.from_dataframe(ins_ace)
    gb8 = gridOptions8.build()
    
    gridOptions9 = GridOptionsBuilder.from_dataframe(bnk_ace)
    gb9 = gridOptions9.build()
    
    gridOptions10 = GridOptionsBuilder.from_dataframe(set_raw)
    gb10 = gridOptions10.build()
    
    gridOptions11 = GridOptionsBuilder.from_dataframe(set_ace)
    gb11 = gridOptions11.build()
    
    gridOptions12 = GridOptionsBuilder.from_dataframe(final_ace2)
    gb12 = gridOptions12.build()
    
    gridOptions13 = GridOptionsBuilder.from_dataframe(aum_chg)
    gb13 = gridOptions13.build()
    
    gridOptions14 = GridOptionsBuilder.from_dataframe(aum_chg_ace)
    gb14 = gridOptions14.build()
    
    gridOptions15 = GridOptionsBuilder.from_dataframe(aum_chg_p)
    gb15 = gridOptions15.build()
    
    gridOptions16 = GridOptionsBuilder.from_dataframe(aum_chg_ace_p)
    gb16 = gridOptions16.build()
    
    gridOptions17 = GridOptionsBuilder.from_dataframe(set_raw_p)
    gb17 = gridOptions17.build()
    
    gridOptions18 = GridOptionsBuilder.from_dataframe(set_ace_p)
    gb18 = gridOptions18.build()
    
    gridOptions19 = GridOptionsBuilder.from_dataframe(etc)
    gb19 = gridOptions19.build()
    
    gridOptions20 = GridOptionsBuilder.from_dataframe(etc_ace)
    gb20 = gridOptions20.build()
    
    gridOptions21 = GridOptionsBuilder.from_dataframe(alien)
    gb21 = gridOptions21.build()
    
    gridOptions22 = GridOptionsBuilder.from_dataframe(alien_ace)
    gb22 = gridOptions22.build()
    
    gridOptions23 = GridOptionsBuilder.from_dataframe(corp)
    gb23 = gridOptions23.build()
    
    gridOptions24 = GridOptionsBuilder.from_dataframe(corp_ace)
    gb24 = gridOptions24.build()
    
    gridOptions25 = GridOptionsBuilder.from_dataframe(finv)
    gb25 = gridOptions25.build()
    
    gridOptions26 = GridOptionsBuilder.from_dataframe(finv_ace)
    gb26 = gridOptions26.build()
    
    gridOptions27 = GridOptionsBuilder.from_dataframe(trust)
    gb27 = gridOptions27.build()
    
    gridOptions28 = GridOptionsBuilder.from_dataframe(trust_ace)
    gb28 = gridOptions28.build()
    
    gridOptions29 = GridOptionsBuilder.from_dataframe(pens)
    gb29 = gridOptions29.build()
    
    gridOptions30 = GridOptionsBuilder.from_dataframe(pens_ace)
    gb30 = gridOptions30.build()

    gridOptions31 = GridOptionsBuilder.from_dataframe(pef)
    gb31 = gridOptions31.build()
    
    gridOptions32 = GridOptionsBuilder.from_dataframe(pef_ace)
    gb32 = gridOptions32.build()
    
    gridOptions33 = GridOptionsBuilder.from_dataframe(prc_chg)
    gb33 = gridOptions33.build()
    
    gridOptions34 = GridOptionsBuilder.from_dataframe(prc_chg_ace)
    gb34 = gridOptions34.build()
    
    custom_css = {
            #".ag-row-hover": {"background-color": "red !important"},
            #".ag-header-cell-label": {"background-color": "orange !important"},
            #".ag-header":{"background-color": "#d0cece !important"},
            ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
            ".all": {"background-color": "#d0cece !important","color":"black !important"},
            ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
            ".blank": {"background-color": "#ffffff !important","color":"black !important"}}
    
    gb['pinnedBottomRowData'] = [{'CLASS':'전체(합계)','기초AUM(조)':final2['기초AUM(조)'].sum(),'기말AUM(조)':final2['기말AUM(조)'].sum(),'ΔAUM(조)':final2['ΔAUM(조)'].sum(),'Δ설정액(조)':final2['Δ설정액(조)'].sum(),'font-weight': 'bold'}]
    gb12['pinnedBottomRowData'] = [{'CLASS':'전체(합계)','기초AUM(조)':final_ace2['기초AUM(조)'].sum(),'기말AUM(조)':final_ace2['기말AUM(조)'].sum(),'ΔAUM(조)':final_ace2['ΔAUM(조)'].sum(),'Δ설정액(조)':final_ace2['Δ설정액(조)'].sum(),'font-weight': 'bold'}]
  
    
    gb['columnDefs'] = [{ 'headerName': '전체 시장 현황','headerClass': 'all', 'children': [{'field': 'CLASS','width':100},{'field': '기초AUM(조)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말AUM(조)','width':100,'valueFormatter':value2},{'field': 'ΔAUM(조)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': 'Δ설정액(조)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
    gb2['columnDefs'] = [{ 'headerName': '순자산상위(억,기말일기준)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'AUM','width':135,'valueFormatter':value2}]}] 
    gb3['columnDefs'] = [{ 'headerName': '개인순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb4['columnDefs'] = [{ 'headerName': '보험순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb5['columnDefs'] = [{ 'headerName': '은행순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb10['columnDefs'] = [{ 'headerName': '설정액증감(억)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액','width':135,'valueFormatter':value2}]}] 
    gb13['columnDefs'] = [{ 'headerName': '순자산증감(억)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ순자산','width':135,'valueFormatter':value2}]}] 
    gb15['columnDefs'] = [{ 'headerName': '순자산증감률(%)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ순자산(%)','width':135,'valueFormatter':value3}]}]
    gb17['columnDefs'] = [{ 'headerName': '설정액증감률(%)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(%)','width':135,'valueFormatter':value3}]}]
    gb19['columnDefs'] = [{ 'headerName': '기타법인순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb21['columnDefs'] = [{ 'headerName': '외국인순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb23['columnDefs'] = [{ 'headerName': '기관순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb25['columnDefs'] = [{ 'headerName': '금융투자순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb27['columnDefs'] = [{ 'headerName': '투신순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb29['columnDefs'] = [{ 'headerName': '연기금순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb31['columnDefs'] = [{ 'headerName': '사모펀드순매수(억,누적)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb33['columnDefs'] = [{ 'headerName': '수익률상위(%)','headerClass': 'all', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '수익률','width':135,'valueFormatter':value2}]}] 
   

    gb6['columnDefs'] = [{ 'headerName': 'ACE순자산상위(억,기말일기준)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'AUM','width':135,'valueFormatter':value2}]}] 
    gb7['columnDefs'] = [{ 'headerName': 'ACE개인순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb8['columnDefs'] = [{ 'headerName': 'ACE보험순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb9['columnDefs'] = [{ 'headerName': 'ACE은행순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb11['columnDefs'] = [{ 'headerName': 'ACE설정액증감(억)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액','width':135,'valueFormatter':value2}]}] 
    gb12['columnDefs'] = [{ 'headerName': 'ACE 시장 현황','headerClass': 'ace', 'children': [{'field': 'CLASS','width':100},{'field': '기초AUM(조)','width':100,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '기말AUM(조)','width':100,'valueFormatter':value2},{'field': 'ΔAUM(조)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode},{'field': 'Δ설정액(조)','width':100,'valueFormatter':value,"cellStyle":cellsytle_jscode}] }] 
    gb14['columnDefs'] = [{ 'headerName': 'ACE순자산증감(억)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ순자산','width':135,'valueFormatter':value2}]}] 
    gb16['columnDefs'] = [{ 'headerName': 'ACE순자산증감률(%)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ순자산(%)','width':135,'valueFormatter':value3}]}]
    gb18['columnDefs'] = [{ 'headerName': 'ACE설정액증감률(%)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': 'Δ설정액(%)','width':135,'valueFormatter':value3}]}]
    gb20['columnDefs'] = [{ 'headerName': 'ACE기타법인순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb22['columnDefs'] = [{ 'headerName': 'ACE외국인순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb24['columnDefs'] = [{ 'headerName': 'ACE기관순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb26['columnDefs'] = [{ 'headerName': 'ACE금융투자순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb28['columnDefs'] = [{ 'headerName': 'ACE투신순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb30['columnDefs'] = [{ 'headerName': 'ACE연기금순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb32['columnDefs'] = [{ 'headerName': 'ACE사모펀드순매수(억,누적)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '순매수','width':135,'valueFormatter':value2}]}] 
    gb34['columnDefs'] = [{ 'headerName': 'ACE수익률상위(%)','headerClass': 'ace', 'children': [{'field': '순위','width':100},{'field': '펀드명','width':250,'valueFormatter':value2,"cellStyle": {'border-left': 'solid black'}},{'field': '수익률','width':135,'valueFormatter':value2}]}] 
   

    edge3,col11,edge4, col22,edge5 = st.columns([0.1,0.4,0.05,0.4,0.05])
    with col11:
        AgGrid(final2, gridOptions=gb ,custom_css=custom_css,allow_unsafe_jscode=True,height=180)      
    with col22:
        AgGrid(final_ace2, gridOptions=gb12 ,custom_css=custom_css,allow_unsafe_jscode=True,height=180)      

    edge,col3, col4, col5,edge2 = st.columns( [0.1,0.4, 0.05,0.4,0.05])
    with col3:    
        

        AgGrid(aum, gridOptions=gb2,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
        AgGrid(prc_chg, gridOptions=gb33 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
        AgGrid(aum_chg, gridOptions=gb13 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
        AgGrid(aum_chg_p, gridOptions=gb15 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
        AgGrid(set_raw, gridOptions=gb10 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
        AgGrid(set_raw_p, gridOptions=gb17 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350) 
        AgGrid(ant, gridOptions=gb3,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)    
        AgGrid(alien, gridOptions=gb21,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)     
        AgGrid(corp, gridOptions=gb23,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)     
        AgGrid(finv, gridOptions=gb25,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)     
        AgGrid(ins, gridOptions=gb4 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
        AgGrid(trust, gridOptions=gb27,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
        AgGrid(bnk, gridOptions=gb5 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)    
        AgGrid(pens, gridOptions=gb29,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
        AgGrid(pef, gridOptions=gb31,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
        AgGrid(etc, gridOptions=gb19 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
    with col5:               # To display brand log

         AgGrid(aum_ace, gridOptions=gb6,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)
         AgGrid(prc_chg_ace, gridOptions=gb34 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
         AgGrid(aum_chg_ace, gridOptions=gb14 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350) 
         AgGrid(aum_chg_ace_p, gridOptions=gb16 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
         AgGrid(set_ace, gridOptions=gb11 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350)  
         AgGrid(set_ace_p, gridOptions=gb18 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350) 
         AgGrid(ant_ace, gridOptions=gb7,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)      
         AgGrid(alien_ace, gridOptions=gb22,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(corp_ace, gridOptions=gb24,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(finv_ace, gridOptions=gb26,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(ins_ace, gridOptions=gb8,custom_css=custom_css ,allow_unsafe_jscode=True,height=350) 
         AgGrid(trust_ace, gridOptions=gb28,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(bnk_ace, gridOptions=gb9,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(pens_ace, gridOptions=gb30,custom_css=custom_css ,allow_unsafe_jscode=True,height=350)  
         AgGrid(pef_ace, gridOptions=gb32,custom_css=custom_css ,allow_unsafe_jscode=True,height=350) 
         AgGrid(etc_ace, gridOptions=gb20 ,custom_css=custom_css,allow_unsafe_jscode=True,height=350) 
      