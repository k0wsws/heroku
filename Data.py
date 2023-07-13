# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 14:47:20 2023

@author: user
"""

import datetime
import pandas as pd
import pickle

now = datetime.datetime.now()
now = now.strftime('%Y-%m-%d')
root=''

def etf_nav():
    

    data=pickle.load(open(root+'nav.pkl','rb'))    
    data=pd.pivot(data=data, index='TRD_DT', values='ETF_NAV',columns=['FUND_CD','ETF_NM'])
    data.fillna("", inplace = True)
    data=data.sort_index(axis=1)
    
    
    return data
    


def fund_prc():
    
    data=pickle.load(open(root+'fund_prc.pkl','rb'))    
    data=pd.pivot(data=data, index='TRD_DT', values='STD_PRC',columns=['FUND_CD','FUND_NM'])
    data.fillna("", inplace = True)
    data=data.sort_index(axis=1)
    
    return data

def BM():
    data=pickle.load(open(root+'bm.pkl','rb'))    
    data=pd.pivot(data=data, index='TRD_DT', values='CLS_PRC',columns=['FUND_CD','IDX_CD'])
    data.fillna("", inplace = True)
    data=data.sort_index(axis=1)
    return data


def FX():
    data=pickle.load(open(root+'fx.pkl','rb'))    
    data=pd.pivot(data=data, index='TRD_DT', values='CLS_PRC',columns=['IDX_CD'])
    data.fillna("", inplace = True)
    data=data.sort_index(axis=1)
    return data