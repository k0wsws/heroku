#크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import pickle
from PIL import Image
import numpy as np
from wordcloud import ImageColorGenerator

root='C:\\Users\\user\\Dashboard\\dataset\\'

def crawl(search='ETF',page=1,page2=10):
    
    # 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
    #입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
    
    def makePgNum(num):
        if num == 1:
            return num
        elif num == 0:
            return num+1
        else:
            return num+9*(num-1)
    
    # 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
    
    def makeUrl(search, start_pg, end_pg):
        if start_pg == end_pg:
            start_page = makePgNum(start_pg)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sm=tab_opt&sort=1&start=" + str(start_page)
            print("생성url: ", url)
            return url
        else:
            urls = []
            for i in range(start_pg, end_pg + 1):
                page = makePgNum(i)
                url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&sm=tab_opt&sort=1&start=" + str(page)
                urls.append(url)
            print("생성url: ", urls)
            return urls    
    
    # html에서 원하는 속성 추출하는 함수 만들기 (기사, 추출하려는 속성값)
    def news_attrs_crawler(articles,attrs):
        attrs_content=[]
        for i in articles:
            attrs_content.append(i.attrs[attrs])
        return attrs_content
    
    # ConnectionError방지
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    
    #html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
    def articles_crawler(url):
        #html 불러오기
        original_html = requests.get(i,headers=headers)
        html = BeautifulSoup(original_html.text, "html.parser")
    
        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        url = news_attrs_crawler(url_naver,'href')
        return url
    
    
    #####뉴스크롤링 시작#####
    
    
    # naver url 생성
    url = makeUrl(search,page,page2)
    
    #뉴스 크롤러 실행
    news_titles = []
    news_url =[]
    news_contents =[]
    news_dates = []
    for i in url:
        url = articles_crawler(url)
        news_url.append(url)
    
    
    #제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
    def makeList(newlist, content):
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist
    
        
    #제목, 링크, 내용 담을 리스트 생성
    news_url_1 = []
    
    #1차원 리스트로 만들기(내용 제외)
    makeList(news_url_1,news_url)
    
    #NAVER 뉴스만 남기기
    final_urls = []
    for i in tqdm(range(len(news_url_1))):
        if "news.naver.com" in news_url_1[i]:
            final_urls.append(news_url_1[i])
        else:
            pass
    
    # 뉴스 내용 크롤링
    
    for i in tqdm(final_urls):
        #각 기사 html get하기
        news = requests.get(i,headers=headers)
        news_html = BeautifulSoup(news.text,"html.parser")
    
        # 뉴스 제목 가져오기
        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")
        
        # 뉴스 본문 가져오기
        content = news_html.select("div#dic_area")
        if content == []:
            content = news_html.select("#articeBody")
    
        # 기사 텍스트만 가져오기
        # list합치기
        content = ''.join(str(content))
    
        # html태그제거 및 텍스트 다듬기
        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')
    
        news_titles.append(title)
        news_contents.append(content)
    
        try:
            html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
        # 날짜 가져오기
        news_dates.append(news_date)
        


def make_wordcloud():
    
    word_count_ace=pickle.load(open(root+'word_count_ace.pkl','rb'))  
    word_count=pickle.load(open(root+'word_count.pkl','rb'))  
    word_count_eco=pickle.load(open(root+'word_count_eco.pkl','rb'))  
    A = np.array(Image.open(root+"A.jpg"))
    C = np.array(Image.open(root+"C.jpg"))
    E = np.array(Image.open(root+"E.jpg"))
    wordcloud = WordCloud(min_font_size=1,font_path='C:/Windows/Fonts/malgun.ttf',width=800, height=800, background_color='white').generate_from_frequencies(word_count)
    wordcloud2 = WordCloud(min_font_size=1,font_path='C:/Windows/Fonts/malgun.ttf',width=800, height=800, background_color='white').generate_from_frequencies(word_count_ace)
    wordcloud3 = WordCloud(min_font_size=1,font_path='C:/Windows/Fonts/malgun.ttf',width=800, height=800, background_color='white').generate_from_frequencies(word_count_eco)
    
    
   # image_colors= ImageColorGenerator(mask)
   # image_colors2= ImageColorGenerator(mask2)
    # plot the word cloud
    fig=plt.figure(figsize=(15,15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('ETF', fontsize=50)
    
    plt.savefig(root+"ETF.jpg")
    
    fig2=plt.figure(figsize=(15,15))
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis('off')
    plt.title('ACE', fontsize=50)
    plt.savefig(root+"ACEETF.jpg")
    
    fig3=plt.figure(figsize=(15,15))
    plt.imshow(wordcloud3, interpolation='bilinear')
    plt.axis('off')
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False
    plt.title('경제', fontsize=50)
    plt.savefig(root+"ECO.jpg")
    
    
   