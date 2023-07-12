# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:55:03 2023

@author: user
"""
import streamlit as st
import pickle

root=''



@st.cache_data
def load_data(TTL=60*60):
  """Loads the data from the pickle file."""
  with open(root+'investor.pkl', 'rb') as f:
    investor = pickle.load(f)
  with open(root+'aum_raw.pkl', 'rb') as f:
    aum_raw = pickle.load(f)
  with open(root+'aum_ace.pkl', 'rb') as f:
    aum_ace_raw = pickle.load(f)
  with open(root+'investor_ace.pkl', 'rb') as f:
    investor_ace = pickle.load(f)
  with open(root+'aum_ace_all.pkl', 'rb') as f:
    aum_ace_all = pickle.load(f)
  with open(root+'aum_rev.pkl', 'rb') as f:
    aum_rev = pickle.load(f)
  aum_rev = aum_rev.sort_values(by='TR_YMD', axis=0)
  return investor, aum_raw, aum_ace_raw, investor_ace, aum_ace_all, aum_rev

@st.cache_data
def load_data_p8(TTL=60*10):
  """Loads the data from the pickle file."""
  with open(root+'master_comp.pkl', 'rb') as f:
    master_comp = pickle.load(f)
  with open(root+'investor.pkl', 'rb') as f:
    investor = pickle.load(f)
  with open(root+'ace_overview.pkl', 'rb') as f:
    ace_overview = pickle.load(f)
    
  return master_comp,investor, ace_overview


@st.cache_data
def load_data_p10(TTL=60*10):
  """Loads the data from the pickle file."""
  with open(root+'aum1.pkl', 'rb') as f:
    aum1 = pickle.load(f)
  with open(root+'overview.pkl', 'rb') as f:
    overview = pickle.load(f)
  with open(root+'investor.pkl', 'rb') as f:
    investor = pickle.load(f)
  with open(root+'etf_map.pkl', 'rb') as f:
    etf_map = pickle.load(f)
  with open(root+'trd_amt.pkl', 'rb') as f:
    trd_amt = pickle.load(f)
  with open(root+'ant_ret.pkl', 'rb') as f:
    ant_ret = pickle.load(f)
  with open(root+'comp_overview.pkl', 'rb') as f:
    comp_overview = pickle.load(f)
  return aum1,investor, overview, etf_map, trd_amt, ant_ret, comp_overview

@st.cache_data
def load_data_p11(TTL=60*10):
  """Loads the data from the pickle file."""
  with open(root+'comp_map.pkl', 'rb') as f:
    comp_map = pickle.load(f)
  with open(root+'comp_overview.pkl', 'rb') as f:
    comp_overview = pickle.load(f)
  with open(root+'comp_investor.pkl', 'rb') as f:
    comp_investor = pickle.load(f)
  with open(root+'ant_ret.pkl', 'rb') as f:
    ant_ret = pickle.load(f)
  return comp_map,comp_overview, comp_investor, ant_ret

@st.cache_data
def load_data_p15(TTL=60*10):
  """Loads the data from the pickle file."""
  with open(root+'aum1.pkl', 'rb') as f:
    aum1 = pickle.load(f)
  with open(root+'overview.pkl', 'rb') as f:
    overview = pickle.load(f)
  with open(root+'investor.pkl', 'rb') as f:
    investor = pickle.load(f)
  with open(root+'etf_map.pkl', 'rb') as f:
    etf_map = pickle.load(f)
  with open(root+'trd_amt.pkl', 'rb') as f:
    trd_amt = pickle.load(f)
  with open(root+'ant_ret.pkl', 'rb') as f:
    ant_ret = pickle.load(f)
  return aum1,investor, overview, etf_map, trd_amt, ant_ret
