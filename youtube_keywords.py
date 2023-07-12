# -*- coding: utf-8 -*-
"""
Created on Sun May 14 16:48:33 2023

@author: user
"""


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st
from datetime import datetime
import pandas as pd


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
API_KEY = "AIzaSyCE8-AKQ7qQ71nwAWWujwrssdU0UeCaAiI"

def generate():

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

    keywords = st.text_input("검색할 키워드를 입력하세요 (쉼표로 구분):").split(",")
    
    total_counts = dict()
    data = []
    
    for query in keywords:
        search_response = youtube.search().list(
            q=query,
            order="viewCount",
            part="snippet",
            maxResults=50
        ).execute()
    
        total_counts[query] = search_response['pageInfo']['totalResults']
    
        for i in range(len(search_response['items'])):
            videoid = search_response['items'][i]['id']['videoId']
    
            stats = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=videoid
            ).execute()
            
            temp = stats['items'][0]['statistics']
            temp['key'] = query
            temp['title'] = search_response['items'][i]['snippet']['title']
            temp['channel'] = search_response['items'][i]['snippet']['channelTitle']
            temp['url'] = 'https://www.youtube.com/watch?v=' + videoid
            temp['publishedAt'] = search_response['items'][i]['snippet']['publishedAt']
            
            # 동영상 스크립트 가져오기
            video_response = youtube.videos().list(
                part="snippet",
                id=videoid
            ).execute()
            
            script = video_response['items'][0]['snippet']['description']
            temp['script'] = script
            
            data.append(temp)
    
    df = pd.DataFrame(data)
    total = pd.DataFrame.from_dict(total_counts, orient='index')
    total.columns = ['videos']
    
    st.title("YouTube 검색 결과")
    
    st.header("검색 결과 개수")
    st.dataframe(total)
    
    st.header("동영상 통계")
    st.dataframe(df)