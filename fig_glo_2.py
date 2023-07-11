# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:26:04 2023

@author: user
"""


import plotly.express as px
import pandas as pd
import pickle
root='C:\\Users\\user\\Dashboard\\dataset\\'

####################################################해###############################################
############# ACE ############



class fig_ace:
    
    def ant(st_dt,end_dt):
        G_ACE_ant = pickle.load(open(root+'G_ACE_ANT.pkl','rb'))  
        
        G_ACE_ant=G_ACE_ant[(G_ACE_ant['TRD_DT']>=st_dt) & (G_ACE_ant['TRD_DT']<=end_dt )] 
        #G_ACE_ant=G_ACE_ant.reset_index()
        G_ACE_ant['SUM']=G_ACE_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_ACE_ant['순위'] = G_ACE_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_ACE_ant[G_ACE_ant['TRD_DT']==max(G_ACE_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=G_ACE_ant[G_ACE_ant['ETF_NM'].isin(ant1)]
        ant2=G_ACE_ant[G_ACE_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        G_ACE_FINV = pickle.load(open(root+'G_ACE_FINV.pkl','rb'))  
        
        G_ACE_FINV=G_ACE_FINV[(G_ACE_FINV['TRD_DT']>=st_dt) & (G_ACE_FINV['TRD_DT']<=end_dt )] 
        #G_ACE_FINV=G_ACE_FINV.reset_index()
        G_ACE_FINV['SUM']=G_ACE_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_ACE_FINV['순위'] = G_ACE_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_ACE_FINV[G_ACE_FINV['TRD_DT']==max(G_ACE_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=G_ACE_FINV[G_ACE_FINV['ETF_NM'].isin(FINV1)]
        FINV2=G_ACE_FINV[G_ACE_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        G_ACE_BK = pickle.load(open(root+'G_ACE_BK.pkl','rb'))  
        
        G_ACE_BK=G_ACE_BK[(G_ACE_BK['TRD_DT']>=st_dt) & (G_ACE_BK['TRD_DT']<=end_dt )] 
        #G_ACE_BK=G_ACE_BK.reset_index()
        G_ACE_BK['SUM']=G_ACE_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_ACE_BK['순위'] = G_ACE_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_ACE_BK[G_ACE_BK['TRD_DT']==max(G_ACE_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=G_ACE_BK[G_ACE_BK['ETF_NM'].isin(BK1)]
        BK2=G_ACE_BK[G_ACE_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        G_ACE_INVT = pickle.load(open(root+'G_ACE_INVT.pkl','rb'))  
        
        G_ACE_INVT=G_ACE_INVT[(G_ACE_INVT['TRD_DT']>=st_dt) & (G_ACE_INVT['TRD_DT']<=end_dt )] 
       # G_ACE_INVT=G_ACE_INVT.reset_index()
        G_ACE_INVT['SUM']=G_ACE_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_ACE_INVT['순위'] = G_ACE_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_ACE_INVT[G_ACE_INVT['TRD_DT']==max(G_ACE_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=G_ACE_INVT[G_ACE_INVT['ETF_NM'].isin(INVT1)]
        INVT2=G_ACE_INVT[G_ACE_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        G_ACE_ALIEN = pickle.load(open(root+'G_ACE_ALIEN.pkl','rb'))  
        
        G_ACE_ALIEN=G_ACE_ALIEN[(G_ACE_ALIEN['TRD_DT']>=st_dt) & (G_ACE_ALIEN['TRD_DT']<=end_dt )] 
        #G_ACE_ALIEN=G_ACE_ALIEN.reset_index()
        G_ACE_ALIEN['SUM']=G_ACE_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_ACE_ALIEN['순위'] = G_ACE_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_ACE_ALIEN[G_ACE_ALIEN['TRD_DT']==max(G_ACE_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=G_ACE_ALIEN[G_ACE_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=G_ACE_ALIEN[G_ACE_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )



############# KODEX ###########

class fig_kodex:
    
    def ant(st_dt,end_dt):
        G_KODEX_ant = pickle.load(open(root+'G_KODEX_ANT.pkl','rb'))  
        
        G_KODEX_ant=G_KODEX_ant[(G_KODEX_ant['TRD_DT']>=st_dt) & (G_KODEX_ant['TRD_DT']<=end_dt )] 
        #G_KODEX_ant=G_KODEX_ant.reset_index()
        G_KODEX_ant['SUM']=G_KODEX_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_KODEX_ant['순위'] = G_KODEX_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_KODEX_ant[G_KODEX_ant['TRD_DT']==max(G_KODEX_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=G_KODEX_ant[G_KODEX_ant['ETF_NM'].isin(ant1)]
        ant2=G_KODEX_ant[G_KODEX_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        G_KODEX_FINV = pickle.load(open(root+'G_KODEX_FINV.pkl','rb'))  
        
        G_KODEX_FINV=G_KODEX_FINV[(G_KODEX_FINV['TRD_DT']>=st_dt) & (G_KODEX_FINV['TRD_DT']<=end_dt )] 
        #G_KODEX_FINV=G_KODEX_FINV.reset_index()
        G_KODEX_FINV['SUM']=G_KODEX_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_KODEX_FINV['순위'] = G_KODEX_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_KODEX_FINV[G_KODEX_FINV['TRD_DT']==max(G_KODEX_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=G_KODEX_FINV[G_KODEX_FINV['ETF_NM'].isin(FINV1)]
        FINV2=G_KODEX_FINV[G_KODEX_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        G_KODEX_BK = pickle.load(open(root+'G_KODEX_BK.pkl','rb'))  
        
        G_KODEX_BK=G_KODEX_BK[(G_KODEX_BK['TRD_DT']>=st_dt) & (G_KODEX_BK['TRD_DT']<=end_dt )] 
        #G_KODEX_BK=G_KODEX_BK.reset_index()
        G_KODEX_BK['SUM']=G_KODEX_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_KODEX_BK['순위'] = G_KODEX_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_KODEX_BK[G_KODEX_BK['TRD_DT']==max(G_KODEX_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=G_KODEX_BK[G_KODEX_BK['ETF_NM'].isin(BK1)]
        BK2=G_KODEX_BK[G_KODEX_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        G_KODEX_INVT = pickle.load(open(root+'G_KODEX_INVT.pkl','rb'))  
        
        G_KODEX_INVT=G_KODEX_INVT[(G_KODEX_INVT['TRD_DT']>=st_dt) & (G_KODEX_INVT['TRD_DT']<=end_dt )] 
       # G_KODEX_INVT=G_KODEX_INVT.reset_index()
        G_KODEX_INVT['SUM']=G_KODEX_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_KODEX_INVT['순위'] = G_KODEX_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_KODEX_INVT[G_KODEX_INVT['TRD_DT']==max(G_KODEX_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=G_KODEX_INVT[G_KODEX_INVT['ETF_NM'].isin(INVT1)]
        INVT2=G_KODEX_INVT[G_KODEX_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        G_KODEX_ALIEN = pickle.load(open(root+'G_KODEX_ALIEN.pkl','rb'))  
        
        G_KODEX_ALIEN=G_KODEX_ALIEN[(G_KODEX_ALIEN['TRD_DT']>=st_dt) & (G_KODEX_ALIEN['TRD_DT']<=end_dt )] 
        #G_KODEX_ALIEN=G_KODEX_ALIEN.reset_index()
        G_KODEX_ALIEN['SUM']=G_KODEX_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_KODEX_ALIEN['순위'] = G_KODEX_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_KODEX_ALIEN[G_KODEX_ALIEN['TRD_DT']==max(G_KODEX_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=G_KODEX_ALIEN[G_KODEX_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=G_KODEX_ALIEN[G_KODEX_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# TIGER ###########



class fig_tiger:
    
    def ant(st_dt,end_dt):
        G_TIGER_ant = pickle.load(open(root+'G_TIGER_ANT.pkl','rb'))  
        
        G_TIGER_ant=G_TIGER_ant[(G_TIGER_ant['TRD_DT']>=st_dt) & (G_TIGER_ant['TRD_DT']<=end_dt )] 
        #G_TIGER_ant=G_TIGER_ant.reset_index()
        G_TIGER_ant['SUM']=G_TIGER_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_TIGER_ant['순위'] = G_TIGER_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_TIGER_ant[G_TIGER_ant['TRD_DT']==max(G_TIGER_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=G_TIGER_ant[G_TIGER_ant['ETF_NM'].isin(ant1)]
        ant2=G_TIGER_ant[G_TIGER_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        G_TIGER_FINV = pickle.load(open(root+'G_TIGER_FINV.pkl','rb'))  
        
        G_TIGER_FINV=G_TIGER_FINV[(G_TIGER_FINV['TRD_DT']>=st_dt) & (G_TIGER_FINV['TRD_DT']<=end_dt )] 
        #G_TIGER_FINV=G_TIGER_FINV.reset_index()
        G_TIGER_FINV['SUM']=G_TIGER_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_TIGER_FINV['순위'] = G_TIGER_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_TIGER_FINV[G_TIGER_FINV['TRD_DT']==max(G_TIGER_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=G_TIGER_FINV[G_TIGER_FINV['ETF_NM'].isin(FINV1)]
        FINV2=G_TIGER_FINV[G_TIGER_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        G_TIGER_BK = pickle.load(open(root+'G_TIGER_BK.pkl','rb'))  
        
        G_TIGER_BK=G_TIGER_BK[(G_TIGER_BK['TRD_DT']>=st_dt) & (G_TIGER_BK['TRD_DT']<=end_dt )] 
        #G_TIGER_BK=G_TIGER_BK.reset_index()
        G_TIGER_BK['SUM']=G_TIGER_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_TIGER_BK['순위'] = G_TIGER_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_TIGER_BK[G_TIGER_BK['TRD_DT']==max(G_TIGER_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=G_TIGER_BK[G_TIGER_BK['ETF_NM'].isin(BK1)]
        BK2=G_TIGER_BK[G_TIGER_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        G_TIGER_INVT = pickle.load(open(root+'G_TIGER_INVT.pkl','rb'))  
        
        G_TIGER_INVT=G_TIGER_INVT[(G_TIGER_INVT['TRD_DT']>=st_dt) & (G_TIGER_INVT['TRD_DT']<=end_dt )] 
       # G_TIGER_INVT=G_TIGER_INVT.reset_index()
        G_TIGER_INVT['SUM']=G_TIGER_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_TIGER_INVT['순위'] = G_TIGER_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_TIGER_INVT[G_TIGER_INVT['TRD_DT']==max(G_TIGER_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=G_TIGER_INVT[G_TIGER_INVT['ETF_NM'].isin(INVT1)]
        INVT2=G_TIGER_INVT[G_TIGER_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        G_TIGER_ALIEN = pickle.load(open(root+'G_TIGER_ALIEN.pkl','rb'))  
        
        G_TIGER_ALIEN=G_TIGER_ALIEN[(G_TIGER_ALIEN['TRD_DT']>=st_dt) & (G_TIGER_ALIEN['TRD_DT']<=end_dt )] 
        #G_TIGER_ALIEN=G_TIGER_ALIEN.reset_index()
        G_TIGER_ALIEN['SUM']=G_TIGER_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_TIGER_ALIEN['순위'] = G_TIGER_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_TIGER_ALIEN[G_TIGER_ALIEN['TRD_DT']==max(G_TIGER_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=G_TIGER_ALIEN[G_TIGER_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=G_TIGER_ALIEN[G_TIGER_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# KBSTAR ###########



class fig_kbstar:
    
    def ant(st_dt,end_dt):
        G_kbstar_ant = pickle.load(open(root+'G_kbstar_ANT.pkl','rb'))  
        
        G_kbstar_ant=G_kbstar_ant[(G_kbstar_ant['TRD_DT']>=st_dt) & (G_kbstar_ant['TRD_DT']<=end_dt )] 
        #G_kbstar_ant=G_kbstar_ant.reset_index()
        G_kbstar_ant['SUM']=G_kbstar_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_kbstar_ant['순위'] = G_kbstar_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_kbstar_ant[G_kbstar_ant['TRD_DT']==max(G_kbstar_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=G_kbstar_ant[G_kbstar_ant['ETF_NM'].isin(ant1)]
        ant2=G_kbstar_ant[G_kbstar_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        G_kbstar_FINV = pickle.load(open(root+'G_kbstar_FINV.pkl','rb'))  
        
        G_kbstar_FINV=G_kbstar_FINV[(G_kbstar_FINV['TRD_DT']>=st_dt) & (G_kbstar_FINV['TRD_DT']<=end_dt )] 
        #G_kbstar_FINV=G_kbstar_FINV.reset_index()
        G_kbstar_FINV['SUM']=G_kbstar_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_kbstar_FINV['순위'] = G_kbstar_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_kbstar_FINV[G_kbstar_FINV['TRD_DT']==max(G_kbstar_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=G_kbstar_FINV[G_kbstar_FINV['ETF_NM'].isin(FINV1)]
        FINV2=G_kbstar_FINV[G_kbstar_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        G_kbstar_BK = pickle.load(open(root+'G_kbstar_BK.pkl','rb'))  
        
        G_kbstar_BK=G_kbstar_BK[(G_kbstar_BK['TRD_DT']>=st_dt) & (G_kbstar_BK['TRD_DT']<=end_dt )] 
        #G_kbstar_BK=G_kbstar_BK.reset_index()
        G_kbstar_BK['SUM']=G_kbstar_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_kbstar_BK['순위'] = G_kbstar_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_kbstar_BK[G_kbstar_BK['TRD_DT']==max(G_kbstar_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=G_kbstar_BK[G_kbstar_BK['ETF_NM'].isin(BK1)]
        BK2=G_kbstar_BK[G_kbstar_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        G_kbstar_INVT = pickle.load(open(root+'G_kbstar_INVT.pkl','rb'))  
        
        G_kbstar_INVT=G_kbstar_INVT[(G_kbstar_INVT['TRD_DT']>=st_dt) & (G_kbstar_INVT['TRD_DT']<=end_dt )] 
       # G_kbstar_INVT=G_kbstar_INVT.reset_index()
        G_kbstar_INVT['SUM']=G_kbstar_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_kbstar_INVT['순위'] = G_kbstar_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_kbstar_INVT[G_kbstar_INVT['TRD_DT']==max(G_kbstar_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=G_kbstar_INVT[G_kbstar_INVT['ETF_NM'].isin(INVT1)]
        INVT2=G_kbstar_INVT[G_kbstar_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        G_kbstar_ALIEN = pickle.load(open(root+'G_kbstar_ALIEN.pkl','rb'))  
        
        G_kbstar_ALIEN=G_kbstar_ALIEN[(G_kbstar_ALIEN['TRD_DT']>=st_dt) & (G_kbstar_ALIEN['TRD_DT']<=end_dt )] 
        #G_kbstar_ALIEN=G_kbstar_ALIEN.reset_index()
        G_kbstar_ALIEN['SUM']=G_kbstar_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_kbstar_ALIEN['순위'] = G_kbstar_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_kbstar_ALIEN[G_kbstar_ALIEN['TRD_DT']==max(G_kbstar_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=G_kbstar_ALIEN[G_kbstar_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=G_kbstar_ALIEN[G_kbstar_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# SOL ###########


class fig_sol:
    
    def ant(st_dt,end_dt):
        G_sol_ant = pickle.load(open(root+'G_sol_ANT.pkl','rb'))  
        
        G_sol_ant=G_sol_ant[(G_sol_ant['TRD_DT']>=st_dt) & (G_sol_ant['TRD_DT']<=end_dt )] 
        #G_sol_ant=G_sol_ant.reset_index()
        G_sol_ant['SUM']=G_sol_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_sol_ant['순위'] = G_sol_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_sol_ant[G_sol_ant['TRD_DT']==max(G_sol_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=G_sol_ant[G_sol_ant['ETF_NM'].isin(ant1)]
        ant2=G_sol_ant[G_sol_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        G_sol_FINV = pickle.load(open(root+'G_sol_FINV.pkl','rb'))  
        
        G_sol_FINV=G_sol_FINV[(G_sol_FINV['TRD_DT']>=st_dt) & (G_sol_FINV['TRD_DT']<=end_dt )] 
        #G_sol_FINV=G_sol_FINV.reset_index()
        G_sol_FINV['SUM']=G_sol_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_sol_FINV['순위'] = G_sol_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_sol_FINV[G_sol_FINV['TRD_DT']==max(G_sol_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=G_sol_FINV[G_sol_FINV['ETF_NM'].isin(FINV1)]
        FINV2=G_sol_FINV[G_sol_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        G_sol_BK = pickle.load(open(root+'G_sol_BK.pkl','rb'))  
        
        G_sol_BK=G_sol_BK[(G_sol_BK['TRD_DT']>=st_dt) & (G_sol_BK['TRD_DT']<=end_dt )] 
        #G_sol_BK=G_sol_BK.reset_index()
        G_sol_BK['SUM']=G_sol_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_sol_BK['순위'] = G_sol_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_sol_BK[G_sol_BK['TRD_DT']==max(G_sol_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=G_sol_BK[G_sol_BK['ETF_NM'].isin(BK1)]
        BK2=G_sol_BK[G_sol_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        G_sol_INVT = pickle.load(open(root+'G_sol_INVT.pkl','rb'))  
        
        G_sol_INVT=G_sol_INVT[(G_sol_INVT['TRD_DT']>=st_dt) & (G_sol_INVT['TRD_DT']<=end_dt )] 
       # G_sol_INVT=G_sol_INVT.reset_index()
        G_sol_INVT['SUM']=G_sol_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_sol_INVT['순위'] = G_sol_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_sol_INVT[G_sol_INVT['TRD_DT']==max(G_sol_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=G_sol_INVT[G_sol_INVT['ETF_NM'].isin(INVT1)]
        INVT2=G_sol_INVT[G_sol_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        G_sol_ALIEN = pickle.load(open(root+'G_sol_ALIEN.pkl','rb'))  
        
        G_sol_ALIEN=G_sol_ALIEN[(G_sol_ALIEN['TRD_DT']>=st_dt) & (G_sol_ALIEN['TRD_DT']<=end_dt )] 
        #G_sol_ALIEN=G_sol_ALIEN.reset_index()
        G_sol_ALIEN['SUM']=G_sol_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        G_sol_ALIEN['순위'] = G_sol_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=G_sol_ALIEN[G_sol_ALIEN['TRD_DT']==max(G_sol_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=G_sol_ALIEN[G_sol_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=G_sol_ALIEN[G_sol_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )
