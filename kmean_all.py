# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:42:25 2023

@author: user
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode, AgGridTheme

root='C:\\Users\\user\\Dashboard\\dataset\\'

sc=StandardScaler()

df=pd.read_csv(root+'DATA_USA.csv',encoding ='cp949')
df = df.drop(['DATE'],axis =1)
#df = df.apply(lambda x: x.str.replace(",", "").astype(float))
df = df.dropna(axis =1)
#df = df.pct_change()
#df = df.dropna()
correlations = df.corr()
dis=1-correlations
dis_scaled=sc.fit_transform(dis)


def n_clust():
    ks = range(1,30)
    inertias = []
    
    for k in ks:
        model = KMeans(n_clusters=k)
        model.fit(dis_scaled)
        inertias.append(model.inertia_)
    
    # Plot ks vs inertias
    plt.figure(figsize=(4, 4))
    plt.rc('font',size=10)
    plt.plot(ks, inertias, '-o')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()



##############K-MEAN CLUSTER#######################
k=KMeans(n_clusters=19)
k.fit(dis_scaled)

result_by_sklearn = dis.copy()
result_by_sklearn["cluster"] = k.labels_
#result_by_sklearn.head()


#result_by_sklearn[result_by_sklearn['cluster']==0]
#result_by_sklearn[result_by_sklearn['cluster']==1]
#result_by_sklearn[result_by_sklearn['cluster']==2]
#result_by_sklearn[result_by_sklearn['cluster']==3]
#result_by_sklearn[result_by_sklearn['cluster']==4]
#result_by_sklearn[result_by_sklearn['cluster']==5]

result=result_by_sklearn['cluster']
result=result.reset_index()


custom_css = {
    #".ag-row-hover": {"background-color": "red !important"},
    #".ag-header-cell-label": {"background-color": "orange !important"},
    #".ag-header":{"background-color": "#d0cece !important"},
    ".ag-header-cell":{"font-size": "7px !important","color":"black !important"},
    ".all": {"background-color": "#d0cece !important","color":"black !important"},
    ".ace": {"background-color": "#bdd7ee !important","color":"black !important"},
    ".blank": {"background-color": "#ffffff !important","color":"black !important"}}


####################PCA + CLUSTER PLOT#############################

def fig():
    X=dis_scaled.copy()
    pca=PCA(n_components=3)
    pca.fit(X)
    x_pca=pca.transform(X)
    x_pca
    
    pca_df=pd.DataFrame(x_pca)
    pca_df.index=dis.index
    pca_df['cluster']=result_by_sklearn['cluster']
    
    plt.rc('font', family='Malgun Gothic')   
    fig=plt.figure(figsize=(12,12))
    sns.scatterplot(0,1,hue='cluster',data=pca_df,palette='coolwarm')
    
   # for idx, row in pca_df.iterrows():  
   #     plt.text(row[0], row[1], idx,size=8)
        
def agg():
    gridOptions = GridOptionsBuilder.from_dataframe(result,min_column_width=30)
    gb = gridOptions.build()
    AgGrid(result, gridOptions=gb,custom_css=custom_css ,allow_unsafe_jscode=True)
   

#Z = linkage(pca_df, 'complete')

#dendrogram(Z, labels=df.columns, orientation='top', leaf_rotation=50);
