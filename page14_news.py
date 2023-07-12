# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:41:15 2023

@author: user
"""

import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import openai
import pandas as pd
import streamlit as st

root='C:\\Users\\user\\Dashboard\\dataset\\'
# OPENAI API키 설정
openai.api_key = "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"

# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# 뉴스 페이지 크롤링
def crawl_page(url):
    try:
        driver = set_chrome_driver(False)
        driver.get(url)
        # 요소 변경 가능
        article_page = driver.find_element(By.CLASS_NAME, 'articlePage')
        text = article_page.text
        driver.close()
    except NoSuchElementException:
        text = ""
    return text

# ChatGPT 요약
def summarize(text):
    # 모델 엔진 선택
    #model_engine = "gpt-3.5-turbo"

    # 맥스 토큰
    #max_tokens = 4000
    
    # 프롬프트 (요약해줘!)
    prompt = f'''Summarize the paragraph below and interpret whether it is a positive or negative sentiment.

    {text}
    '''

    # 요약 요청
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content

# 파파고 번역
def papago_translate(text):
    try:
        papago = set_chrome_driver(False)
        papago.get('https://papago.naver.com/')
        time.sleep(1)
        papago.find_element(By.ID, 'txtSource').send_keys(text)
        papago.find_element(By.ID, 'btnTranslate').click()
        time.sleep(2)
        papago_translated = papago.find_element(By.ID, 'targetEditArea')
        result = papago_translated.text
    except NoSuchElementException: # 예외처리 (요소를 찾지 못하는 경우)
        result = '번역 오류ㅠㅠ'
    finally:
        papago.close()
    return result

# 최종 wrapper
def summarize_news(url):
    page = crawl_page(url)
    summarized = summarize(page)
    print('[원문 요약]')
    print(summarized)
    korean_translated = papago_translate(summarized)
    print('\n[한글 요약]')
    print(korean_translated)
    return korean_translated

# most popular news 의 신문기사 요소를 크롤링 합니다
def generate(): 
    
    top5 = set_chrome_driver(False)
    # URL 요청
    top5.get('https://www.investing.com/news/most-popular-news')
    # 5개의 요소만 가져옵니다.
    top5.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:5]
    
    # 5개의 신문기사 URL 만 추출 합니다.
    top5_links = []
    
    for link in top5.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:5]:
        top5_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
        
    top5_links
    
    # 5개의 신문기사 링크에 대한 본문 크롤링+요약+번역 을 진행합니다.
    top5_summarize = []
    
    for link in top5_links:
        output = summarize_news(link)
        top5_summarize.append([link,output])
        
    top5_summarize=pd.DataFrame(top5_summarize,columns=['Link','Summary'])
    top5_summarize.to_csv(root+'top5news.csv')
