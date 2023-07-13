# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 18:26:04 2023

@author: user
"""

import plotly.express as px
import pandas as pd
import pickle
root=''

class fig_ace:
    
    def ant(st_dt,end_dt):
        ace_ant = pickle.load(open(root+'ACE_ANT.pkl','rb'))  
        
        ace_ant=ace_ant[(ace_ant['TRD_DT']>=st_dt) & (ace_ant['TRD_DT']<=end_dt )] 
        #ace_ant=ace_ant.reset_index()
        ace_ant['SUM']=(ace_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        ace_ant['순위'] = ace_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=ace_ant[ace_ant['TRD_DT']==max(ace_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=ace_ant[ace_ant['ETF_NM'].isin(ant1)]
        ant2=ace_ant[ace_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )
    
    def finv(st_dt,end_dt):
        ace_FINV = pickle.load(open(root+'ACE_FINV.pkl','rb'))  
        
        ace_FINV=ace_FINV[(ace_FINV['TRD_DT']>=st_dt) & (ace_FINV['TRD_DT']<=end_dt )] 
        #ace_FINV=ace_FINV.reset_index()
        ace_FINV['SUM']=(ace_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        ace_FINV['순위'] = ace_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=ace_FINV[ace_FINV['TRD_DT']==max(ace_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=ace_FINV[ace_FINV['ETF_NM'].isin(FINV1)]
        FINV2=ace_FINV[ace_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )
    
    def bk(st_dt,end_dt):
        ace_BK = pickle.load(open(root+'ACE_BK.pkl','rb'))  
        
        ace_BK=ace_BK[(ace_BK['TRD_DT']>=st_dt) & (ace_BK['TRD_DT']<=end_dt )] 
        #ace_BK=ace_BK.reset_index()
        ace_BK['SUM']=(ace_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        ace_BK['순위'] = ace_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=ace_BK[ace_BK['TRD_DT']==max(ace_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=ace_BK[ace_BK['ETF_NM'].isin(BK1)]
        BK2=ace_BK[ace_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )
    
    def invt(st_dt,end_dt):
        ace_INVT = pickle.load(open(root+'ACE_INVT.pkl','rb'))  
        
        ace_INVT=ace_INVT[(ace_INVT['TRD_DT']>=st_dt) & (ace_INVT['TRD_DT']<=end_dt )] 
       # ace_INVT=ace_INVT.reset_index()
        ace_INVT['SUM']=(ace_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        ace_INVT['순위'] = ace_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=ace_INVT[ace_INVT['TRD_DT']==max(ace_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=ace_INVT[ace_INVT['ETF_NM'].isin(INVT1)]
        INVT2=ace_INVT[ace_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )
    
    def alien(st_dt,end_dt):
        ace_ALIEN = pickle.load(open(root+'ACE_ALIEN.pkl','rb'))  
        
        ace_ALIEN=ace_ALIEN[(ace_ALIEN['TRD_DT']>=st_dt) & (ace_ALIEN['TRD_DT']<=end_dt )] 
        #ace_ALIEN=ace_ALIEN.reset_index()
        ace_ALIEN['SUM']=(ace_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        ace_ALIEN['순위'] = ace_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=ace_ALIEN[ace_ALIEN['TRD_DT']==max(ace_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=ace_ALIEN[ace_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=ace_ALIEN[ace_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# KODEX ###########

class fig_kodex:
    
    def ant(st_dt,end_dt):
        KODEX_ant = pickle.load(open(root+'KODEX_ANT.pkl','rb'))  
        
        KODEX_ant=KODEX_ant[(KODEX_ant['TRD_DT']>=st_dt) & (KODEX_ant['TRD_DT']<=end_dt )] 
        #KODEX_ant=KODEX_ant.reset_index()
        KODEX_ant['SUM']=(KODEX_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        KODEX_ant['순위'] = KODEX_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=KODEX_ant[KODEX_ant['TRD_DT']==max(KODEX_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=KODEX_ant[KODEX_ant['ETF_NM'].isin(ant1)]
        ant2=KODEX_ant[KODEX_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        KODEX_FINV = pickle.load(open(root+'KODEX_FINV.pkl','rb'))  
        
        KODEX_FINV=KODEX_FINV[(KODEX_FINV['TRD_DT']>=st_dt) & (KODEX_FINV['TRD_DT']<=end_dt )] 
        #KODEX_FINV=KODEX_FINV.reset_index()
        KODEX_FINV['SUM']=(KODEX_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        KODEX_FINV['순위'] = KODEX_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=KODEX_FINV[KODEX_FINV['TRD_DT']==max(KODEX_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=KODEX_FINV[KODEX_FINV['ETF_NM'].isin(FINV1)]
        FINV2=KODEX_FINV[KODEX_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        KODEX_BK = pickle.load(open(root+'KODEX_BK.pkl','rb'))  
        
        KODEX_BK=KODEX_BK[(KODEX_BK['TRD_DT']>=st_dt) & (KODEX_BK['TRD_DT']<=end_dt )] 
        #KODEX_BK=KODEX_BK.reset_index()
        KODEX_BK['SUM']=(KODEX_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        KODEX_BK['순위'] = KODEX_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=KODEX_BK[KODEX_BK['TRD_DT']==max(KODEX_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=KODEX_BK[KODEX_BK['ETF_NM'].isin(BK1)]
        BK2=KODEX_BK[KODEX_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        KODEX_INVT = pickle.load(open(root+'KODEX_INVT.pkl','rb'))  
        
        KODEX_INVT=KODEX_INVT[(KODEX_INVT['TRD_DT']>=st_dt) & (KODEX_INVT['TRD_DT']<=end_dt )] 
       # KODEX_INVT=KODEX_INVT.reset_index()
        KODEX_INVT['SUM']=(KODEX_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        KODEX_INVT['순위'] = KODEX_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=KODEX_INVT[KODEX_INVT['TRD_DT']==max(KODEX_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=KODEX_INVT[KODEX_INVT['ETF_NM'].isin(INVT1)]
        INVT2=KODEX_INVT[KODEX_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        KODEX_ALIEN = pickle.load(open(root+'KODEX_ALIEN.pkl','rb'))  
        
        KODEX_ALIEN=KODEX_ALIEN[(KODEX_ALIEN['TRD_DT']>=st_dt) & (KODEX_ALIEN['TRD_DT']<=end_dt )] 
        #KODEX_ALIEN=KODEX_ALIEN.reset_index()
        KODEX_ALIEN['SUM']=(KODEX_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        KODEX_ALIEN['순위'] = KODEX_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=KODEX_ALIEN[KODEX_ALIEN['TRD_DT']==max(KODEX_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=KODEX_ALIEN[KODEX_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=KODEX_ALIEN[KODEX_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# TIGER ###########



class fig_tiger:
    
    
    def ant(st_dt,end_dt):
        TIGER_ant = pickle.load(open(root+'TIGER_ANT.pkl','rb'))  
        
        TIGER_ant=TIGER_ant[(TIGER_ant['TRD_DT']>=st_dt) & (TIGER_ant['TRD_DT']<=end_dt )] 
        #TIGER_ant=TIGER_ant.reset_index()
        TIGER_ant['SUM']=(TIGER_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        TIGER_ant['순위'] = TIGER_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=TIGER_ant[TIGER_ant['TRD_DT']==max(TIGER_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=TIGER_ant[TIGER_ant['ETF_NM'].isin(ant1)]
        ant2=TIGER_ant[TIGER_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )
    
    def finv(st_dt,end_dt):
        TIGER_FINV = pickle.load(open(root+'TIGER_FINV.pkl','rb'))  
        
        TIGER_FINV=TIGER_FINV[(TIGER_FINV['TRD_DT']>=st_dt) & (TIGER_FINV['TRD_DT']<=end_dt )] 
        #TIGER_FINV=TIGER_FINV.reset_index()
        TIGER_FINV['SUM']=TIGER_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        TIGER_FINV['순위'] = TIGER_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=TIGER_FINV[TIGER_FINV['TRD_DT']==max(TIGER_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=TIGER_FINV[TIGER_FINV['ETF_NM'].isin(FINV1)]
        FINV2=TIGER_FINV[TIGER_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )
    
    def bk(st_dt,end_dt):
        TIGER_BK = pickle.load(open(root+'TIGER_BK.pkl','rb'))  
        
        TIGER_BK=TIGER_BK[(TIGER_BK['TRD_DT']>=st_dt) & (TIGER_BK['TRD_DT']<=end_dt )] 
        #TIGER_BK=TIGER_BK.reset_index()
        TIGER_BK['SUM']=TIGER_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        TIGER_BK['순위'] = TIGER_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=TIGER_BK[TIGER_BK['TRD_DT']==max(TIGER_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=TIGER_BK[TIGER_BK['ETF_NM'].isin(BK1)]
        BK2=TIGER_BK[TIGER_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )
    
    def invt(st_dt,end_dt):
        TIGER_INVT = pickle.load(open(root+'TIGER_INVT.pkl','rb'))  
        
        TIGER_INVT=TIGER_INVT[(TIGER_INVT['TRD_DT']>=st_dt) & (TIGER_INVT['TRD_DT']<=end_dt )] 
       # TIGER_INVT=TIGER_INVT.reset_index()
        TIGER_INVT['SUM']=TIGER_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        TIGER_INVT['순위'] = TIGER_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=TIGER_INVT[TIGER_INVT['TRD_DT']==max(TIGER_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=TIGER_INVT[TIGER_INVT['ETF_NM'].isin(INVT1)]
        INVT2=TIGER_INVT[TIGER_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )
    
    def alien(st_dt,end_dt):
        TIGER_ALIEN = pickle.load(open(root+'TIGER_ALIEN.pkl','rb'))  
        
        TIGER_ALIEN=TIGER_ALIEN[(TIGER_ALIEN['TRD_DT']>=st_dt) & (TIGER_ALIEN['TRD_DT']<=end_dt )] 
        #TIGER_ALIEN=TIGER_ALIEN.reset_index()
        TIGER_ALIEN['SUM']=TIGER_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        TIGER_ALIEN['순위'] = TIGER_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=TIGER_ALIEN[TIGER_ALIEN['TRD_DT']==max(TIGER_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=TIGER_ALIEN[TIGER_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=TIGER_ALIEN[TIGER_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )


############# KBSTAR ###########


class fig_kbstar:
    
    def ant(st_dt,end_dt):
        kbstar_ant = pickle.load(open(root+'kbstar_ANT.pkl','rb'))  
        
        kbstar_ant=kbstar_ant[(kbstar_ant['TRD_DT']>=st_dt) & (kbstar_ant['TRD_DT']<=end_dt )] 
        #kbstar_ant=kbstar_ant.reset_index()
        kbstar_ant['SUM']=kbstar_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        kbstar_ant['순위'] = kbstar_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=kbstar_ant[kbstar_ant['TRD_DT']==max(kbstar_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=kbstar_ant[kbstar_ant['ETF_NM'].isin(ant1)]
        ant2=kbstar_ant[kbstar_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        kbstar_FINV = pickle.load(open(root+'kbstar_FINV.pkl','rb'))  
        
        kbstar_FINV=kbstar_FINV[(kbstar_FINV['TRD_DT']>=st_dt) & (kbstar_FINV['TRD_DT']<=end_dt )] 
        #kbstar_FINV=kbstar_FINV.reset_index()
        kbstar_FINV['SUM']=kbstar_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        kbstar_FINV['순위'] = kbstar_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=kbstar_FINV[kbstar_FINV['TRD_DT']==max(kbstar_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=kbstar_FINV[kbstar_FINV['ETF_NM'].isin(FINV1)]
        FINV2=kbstar_FINV[kbstar_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        kbstar_BK = pickle.load(open(root+'kbstar_BK.pkl','rb'))  
        
        kbstar_BK=kbstar_BK[(kbstar_BK['TRD_DT']>=st_dt) & (kbstar_BK['TRD_DT']<=end_dt )] 
        #kbstar_BK=kbstar_BK.reset_index()
        kbstar_BK['SUM']=kbstar_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        kbstar_BK['순위'] = kbstar_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=kbstar_BK[kbstar_BK['TRD_DT']==max(kbstar_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=kbstar_BK[kbstar_BK['ETF_NM'].isin(BK1)]
        BK2=kbstar_BK[kbstar_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        kbstar_INVT = pickle.load(open(root+'kbstar_INVT.pkl','rb'))  
        
        kbstar_INVT=kbstar_INVT[(kbstar_INVT['TRD_DT']>=st_dt) & (kbstar_INVT['TRD_DT']<=end_dt )] 
       # kbstar_INVT=kbstar_INVT.reset_index()
        kbstar_INVT['SUM']=kbstar_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        kbstar_INVT['순위'] = kbstar_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=kbstar_INVT[kbstar_INVT['TRD_DT']==max(kbstar_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=kbstar_INVT[kbstar_INVT['ETF_NM'].isin(INVT1)]
        INVT2=kbstar_INVT[kbstar_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        kbstar_ALIEN = pickle.load(open(root+'kbstar_ALIEN.pkl','rb'))  
        
        kbstar_ALIEN=kbstar_ALIEN[(kbstar_ALIEN['TRD_DT']>=st_dt) & (kbstar_ALIEN['TRD_DT']<=end_dt )] 
        #kbstar_ALIEN=kbstar_ALIEN.reset_index()
        kbstar_ALIEN['SUM']=kbstar_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0])/10000
        
        kbstar_ALIEN['순위'] = kbstar_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=kbstar_ALIEN[kbstar_ALIEN['TRD_DT']==max(kbstar_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=kbstar_ALIEN[kbstar_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=kbstar_ALIEN[kbstar_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )

    
############# SOL ###########


class fig_sol:
    
    def ant(st_dt,end_dt):
        sol_ant = pickle.load(open(root+'sol_ANT.pkl','rb'))  
        
        sol_ant=sol_ant[(sol_ant['TRD_DT']>=st_dt) & (sol_ant['TRD_DT']<=end_dt )] 
        #sol_ant=sol_ant.reset_index()
        sol_ant['SUM']=(sol_ant.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        sol_ant['순위'] = sol_ant.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=sol_ant[sol_ant['TRD_DT']==max(sol_ant['TRD_DT'])]
        ant1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ant2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ant1=sol_ant[sol_ant['ETF_NM'].isin(ant1)]
        ant2=sol_ant[sol_ant['ETF_NM'].isin(ant2)]
        
        return px.line(ant1,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(상위)" ),px.line(ant2,x="TRD_DT",y="SUM",color="ETF_NM",title="개인(하위)" )

    def finv(st_dt,end_dt):
        sol_FINV = pickle.load(open(root+'sol_FINV.pkl','rb'))  
        
        sol_FINV=sol_FINV[(sol_FINV['TRD_DT']>=st_dt) & (sol_FINV['TRD_DT']<=end_dt )] 
        #sol_FINV=sol_FINV.reset_index()
        sol_FINV['SUM']=(sol_FINV.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        sol_FINV['순위'] = sol_FINV.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=sol_FINV[sol_FINV['TRD_DT']==max(sol_FINV['TRD_DT'])]
        FINV1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        FINV2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        FINV1=sol_FINV[sol_FINV['ETF_NM'].isin(FINV1)]
        FINV2=sol_FINV[sol_FINV['ETF_NM'].isin(FINV2)]
        
        return px.line(FINV1,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(상위)" ),px.line(FINV2,x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(하위)" )

    def bk(st_dt,end_dt):
        sol_BK = pickle.load(open(root+'sol_BK.pkl','rb'))  
        
        sol_BK=sol_BK[(sol_BK['TRD_DT']>=st_dt) & (sol_BK['TRD_DT']<=end_dt )] 
        #sol_BK=sol_BK.reset_index()
        sol_BK['SUM']=(sol_BK.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        sol_BK['순위'] = sol_BK.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=sol_BK[sol_BK['TRD_DT']==max(sol_BK['TRD_DT'])]
        BK1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        BK2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        BK1=sol_BK[sol_BK['ETF_NM'].isin(BK1)]
        BK2=sol_BK[sol_BK['ETF_NM'].isin(BK2)]
        
        return px.line(BK1,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(상위)" ),px.line(BK2,x="TRD_DT",y="SUM",color="ETF_NM",title="은행(하위)" )

    def invt(st_dt,end_dt):
        sol_INVT = pickle.load(open(root+'sol_INVT.pkl','rb'))  
        
        sol_INVT=sol_INVT[(sol_INVT['TRD_DT']>=st_dt) & (sol_INVT['TRD_DT']<=end_dt )] 
       # sol_INVT=sol_INVT.reset_index()
        sol_INVT['SUM']=(sol_INVT.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        sol_INVT['순위'] = sol_INVT.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=sol_INVT[sol_INVT['TRD_DT']==max(sol_INVT['TRD_DT'])]
        INVT1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        INVT2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        INVT1=sol_INVT[sol_INVT['ETF_NM'].isin(INVT1)]
        INVT2=sol_INVT[sol_INVT['ETF_NM'].isin(INVT2)]
        
        return px.line(INVT1,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(상위)" ),px.line(INVT2,x="TRD_DT",y="SUM",color="ETF_NM",title="보험(하위)" )

    def alien(st_dt,end_dt):
        sol_ALIEN = pickle.load(open(root+'sol_ALIEN.pkl','rb'))  
        
        sol_ALIEN=sol_ALIEN[(sol_ALIEN['TRD_DT']>=st_dt) & (sol_ALIEN['TRD_DT']<=end_dt )] 
        #sol_ALIEN=sol_ALIEN.reset_index()
        sol_ALIEN['SUM']=(sol_ALIEN.groupby('ETF_NM')['SUM'].transform(lambda x: x - x.iloc[0]))/10000
        
        sol_ALIEN['순위'] = sol_ALIEN.groupby(['TRD_DT'])['SUM'].rank(method='min',ascending=False)     
        a=sol_ALIEN[sol_ALIEN['TRD_DT']==max(sol_ALIEN['TRD_DT'])]
        ALIEN1=a[a['순위']<=max(a['순위'])/2]['ETF_NM']
        ALIEN2=a[a['순위']>max(a['순위'])/2]['ETF_NM']
        
        ALIEN1=sol_ALIEN[sol_ALIEN['ETF_NM'].isin(ALIEN1)]
        ALIEN2=sol_ALIEN[sol_ALIEN['ETF_NM'].isin(ALIEN2)]
        
        return px.line(ALIEN1,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(상위)" ),px.line(ALIEN2,x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(하위)" )



#########ALL##########

class fig_all:
    
    def ant(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_ant = pickle.load(open(root+'ALL_ANT.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
                
            else:
                df=all_ant[all_ant['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)
            
        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="개인(억 원)" ,width=450)
               
        
    
    def bk(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_bk = pickle.load(open(root+'ALL_BK.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
                df=all_bk[all_bk['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df) 
              
        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="은행(억 원)",width=450 )
        
    
    def invt(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_invt = pickle.load(open(root+'ALL_INS.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_invt[all_invt['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="보험(억 원)" ,width=450)
        
    

    def alien(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_alien = pickle.load(open(root+'ALL_ALIEN.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_alien[all_alien['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="외국인(억 원)" ,width=450)
        
    
    def corp(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_corp = pickle.load(open(root+'ALL_CORP.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_corp[all_corp['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="기관(억 원)" ,width=450)
        
    def pens(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_pens = pickle.load(open(root+'ALL_PENS.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_pens[all_pens['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="연기금(억 원)" ,width=450)
        
    
    def pef(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_pef = pickle.load(open(root+'ALL_PEF.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_pef[all_pef['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="사모펀드(억 원)" ,width=450)
        
    

    def trust(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_trust = pickle.load(open(root+'ALL_TRUST.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_trust[all_trust['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="투신(억 원)" ,width=450)
        
    
    def finv(a1,a2,a3,a4,a5,st_dt,end_dt):
        all_finv = pickle.load(open(root+'ALL_FINV.pkl','rb'))   
        df=pd.DataFrame()
        df_f=pd.DataFrame()
        for i in  [a1,a2,a3,a4,a5]:
            
            if i=='없음':
                df_f=df_f
            else:
            
                df=all_finv[all_finv['ETF_NM']==i]
                df=df[(df['TRD_DT']>=st_dt) & (df['TRD_DT']<=end_dt )] 
                df=df.reset_index()
                df['SUM']=(df['SUM']-df['SUM'][0])/10000
                df_f=df_f.append(df)

        return px.line(df_f, x="TRD_DT",y="SUM",color="ETF_NM",title="금융투자(억 원)" ,width=450)
        
    

             
           

        
               