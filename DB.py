# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:30:12 2023

@author: user
"""
import pyodbc
import pandas as pd


server = 'tcp:192.168.194.229,1433'
database = 'quant1'
username = 'quant'
password = 'quant'
 

##DB 접속

def conn():
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return connection

## sql read
def read(data,connection):
    
    return pd.read_sql(data,conn())
    