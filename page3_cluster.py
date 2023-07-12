# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 15:01:48 2023

@author: user
"""
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import kmean as km
import pickle
import math
import matplotlib as mpl

root=''

logo = Image.open('ace.jpg')
data_ace = pd.read_csv(root+"ACE.csv")
data_kodex = pd.read_csv(root+"KODEX.csv")
data_tiger = pd.read_csv(root+"TIGER.csv")
data_ex_ace = pd.read_csv(root+"ALL.csv")

data_ace = data_ace.drop(['Unnamed: 0'],axis =1)
data_kodex = data_kodex.drop(['Unnamed: 0'],axis =1)
data_tiger = data_tiger.drop(['Unnamed: 0'],axis =1)
data_ex_ace = data_ex_ace.drop(['Unnamed: 0'],axis =1) 

def generate():
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        title = '<p style="font-family:Cooper Black; color:#000000; font-size: 35px;">Cluster Chart</p>'
        st.markdown(title, unsafe_allow_html=True)    
    with col2:               # To display brand log
        st.image(logo, width=200 )
    option2 = st.selectbox("운용사", ("선택","ACE","KODEX","TIGER","전체"),key=2)
    
    if option2 =="ACE":
        
        plt.rc('font', family='Malgun Gothic')   
        fig=plt.figure(figsize=(15,10)) 
        correlations = data_ace.corr()
        sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, annot_kws={"size": 10}, vmin=-1, vmax=1);
        
        plt.rc('font', family='Malgun Gothic')             
        fig2=plt.figure(figsize=(12,5))
        dissimilarity = 1 - (correlations)
        Z = linkage((dissimilarity)**(1/2), 'complete')
        #Z = linkage(squareform(dissimilarity), 'complete')
            
        dendrogram(Z, labels=data_ace.columns, orientation='top', leaf_rotation=90);
        
        
        
        title1 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">1. Correlation Matrix</p>'
        st.markdown(title1, unsafe_allow_html=True)     
        st.pyplot(fig)
        
        title2 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">2. Clustering</p>'
        st.markdown(title2, unsafe_allow_html=True)        
        st.pyplot(fig2)
        
        title3 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">3. Risk-Return Profile</p>'
        st.markdown(title3, unsafe_allow_html=True)  
        
        fig3=plt.figure(figsize=(5,5))
        plt.rc('font', family='Malgun Gothic')
        mpl.rc('axes', unicode_minus=False)
        data=data_ace.pct_change(784)
        data_rt=data_ace.pct_change().dropna()
        data=data.dropna()
        x=data_rt.std()*math.sqrt(224)
        x=x.tolist()
        y=(data.mean()).tolist()

        symbols = data_ace.columns
        plt.scatter(x,y)
        for index, symbol in enumerate(symbols):
            plt.annotate(symbol, (x[index], y[index]))
            
        st.pyplot(fig3)
    
        
    elif option2 =="전체":
        
        plt.rc('font', family='Malgun Gothic')   
        fig=plt.figure(figsize=(15,10)) 
        correlations = data_ex_ace.corr()
        sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, annot_kws={"size": 10}, vmin=-1, vmax=1);
       
        plt.rc('font', family='Malgun Gothic')               
        fig2=plt.figure(figsize=(12,5))
        dissimilarity = 1 - (correlations)
        Z = linkage((dissimilarity), 'complete')
            
        dendrogram(Z, labels=data_ex_ace.columns, orientation='top', leaf_rotation=90);
            
        title1 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">1. Correlation Matrix</p>'
        st.markdown(title1, unsafe_allow_html=True)          
        st.pyplot(fig)
        
        title2 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">2. Clustering</p>'
        st.markdown(title2, unsafe_allow_html=True)         
        st.pyplot(fig2)
    
    elif option2 =="KODEX":
        
        plt.rc('font', family='Malgun Gothic')   
        fig=plt.figure(figsize=(15,10)) 
        correlations = data_kodex.corr()
        sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, annot_kws={"size": 10}, vmin=-1, vmax=1);
    
        plt.rc('font', family='Malgun Gothic')               
        fig2=plt.figure(figsize=(12,5))
        dissimilarity = 1 - (correlations)
        Z = linkage((dissimilarity)**(1/2), 'complete')
            
        dendrogram(Z, labels=data_kodex.columns, orientation='top', leaf_rotation=90);
            
        title1 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">1. Correlation Matrix</p>'
        st.markdown(title1, unsafe_allow_html=True)          
        st.pyplot(fig)
        
        title2 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">2. Clustering</p>'
        st.markdown(title2, unsafe_allow_html=True)          
        st.pyplot(fig2)
        
    
    elif option2 =="TIGER":
        
        plt.rc('font', family='Malgun Gothic')   
        fig=plt.figure(figsize=(15,10)) 
        correlations = data_tiger.corr()
        sns.heatmap(round(correlations,2), cmap='RdBu', annot=True, annot_kws={"size": 10}, vmin=-1, vmax=1);
        plt.rc('font', family='Malgun Gothic')   
            
        fig2=plt.figure(figsize=(12,5))
        dissimilarity = 1 - (correlations)
        Z = linkage((dissimilarity)**(1/2), 'complete')
            
        dendrogram(Z, labels=data_tiger.columns, orientation='top', leaf_rotation=90);
            
        title1 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">1. Correlation Matrix</p>'
        st.markdown(title1, unsafe_allow_html=True)  
         
        st.pyplot(fig)
        
        title2 = '<p style="font-family:Cooper Black; color:#000000; font-size: 20px;">2. Clustering</p>'
        st.markdown(title2, unsafe_allow_html=True)  
        
        st.pyplot(fig2)
