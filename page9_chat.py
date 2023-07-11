# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 09:28:20 2023

@author: user
"""

import openai
import streamlit as st
from streamlit_chat import message
import os 
from dotenv import load_dotenv
load_dotenv('api_key.env')
openai.api_key = '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'
def generate_response(prompt):
    completion = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[{"role": "user", "content": prompt}]
)
    message=completion.choices[0].message.content
    return message

def generate():
    st.title("무엇이든물어보세요")
    #storing the chat

    user_input=st.text_input("You:",key='input')
    message(generate_response(user_input))
