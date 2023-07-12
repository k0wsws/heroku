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

root=''

sc=StandardScaler()

df=pd.read_csv(root+'ACE.csv')
df = df.drop(['Unnamed: 0'],axis =1)
correlations = df.corr()
dis=1-correlations
dis_scaled=sc.fit_transform(dis)


def n_clust():
    ks = range(1,15)
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
k=KMeans(n_clusters=4)
k.fit(dis_scaled)

result_by_sklearn = dis.copy()
result_by_sklearn["cluster"] = k.labels_
result_by_sklearn.head()


result_by_sklearn[result_by_sklearn['cluster']==0]
result_by_sklearn[result_by_sklearn['cluster']==1]
result_by_sklearn[result_by_sklearn['cluster']==2]
result_by_sklearn[result_by_sklearn['cluster']==3]
result_by_sklearn[result_by_sklearn['cluster']==4]
result_by_sklearn[result_by_sklearn['cluster']==5]





####################PCA + CLUSTER PLOT#############################

def fig():
    X=dis_scaled.copy()
    pca=PCA(n_components=2)
    pca.fit(X)
    x_pca=pca.transform(X)
    x_pca
    
    pca_df=pd.DataFrame(x_pca)
    pca_df.index=dis.index
    pca_df['cluster']=result_by_sklearn['cluster']
    
    plt.rc('font', family='Malgun Gothic')   
    fig=plt.figure(figsize=(12,12))
    sns.scatterplot(0,1,hue='cluster',data=pca_df,palette='coolwarm')
    
    for idx, row in pca_df.iterrows():  
        plt.text(row[0], row[1], idx,size=8)
   

#Z = linkage(pca_df, 'complete')

#dendrogram(Z, labels=df.columns, orientation='top', leaf_rotation=50);
