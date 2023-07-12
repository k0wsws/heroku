# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:29:32 2023

@author: user
"""

#크롤링시 필요한 라이브러리 불러오기
from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import pandas as pd
from konlpy.tag import Okt
from collections import Counter
#크롤링시 필요한 라이브러리 불러오기
import pickle
from PIL import Image
import numpy as np
import key_wordcloud as wc
from konlpy.tag import Mecab
now = datetime.datetime.now()

def generate():
    #검색어 입력
    search = 'ETF'
    #검색 시작할 페이지 입력
    page = 1  
    #검색 종료할 페이지 입력
    page2 = 10
    
    
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
        if ("news.naver.com" in news_url_1[i]) and ("sports" not in news_url_1[i]):
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
            html_date = news_html.select_one("div#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
        # 날짜 가져오기
        news_dates.append(news_date)
    
    root='C:\\Users\\user\\Dashboard\\dataset\\'
    news_df = pd.DataFrame({'date':news_dates,'title':news_titles,'link':final_urls})
    news_contents=''.join(news_contents)
    okt = Okt()
    words = okt.nouns(news_contents)
    
    sw=pd.read_excel(root+'stopwords.xlsx',dtype=str,engine='openpyxl')
    sw=sw['stopword'].tolist()
    stop_words = ['산출','발생','강조','집중','정책','위해','회복','증시','뉴스','이익','기대','기관','심리','연금','가운데','개미','성장','미국','기준','투자신탁','주가','파산','안전','관련','활용','이자','업체','해외','비중','대표','테마','계좌','달러','설명','정보','확대','위기','라며','사태','삼성','미래에셋','인상','가장','규모','위험','가격','대한','상황','산업','예상','선물','때문','기간','전략','유입','종목','이상','기업','상승','수준','경우','최근','만기','대비','시작','자금','성과','포트폴리오','전망','지난해','거래','은행','개인','기록','결제','장기','포스','지난','금융투자','주식','채권','안정','예금','제공','연초','하락','상장','홈페이지','이후','매수','변동성','추종','지수','국내','증권사','수익','업무','올해','금융','공모','한국','운용','증권','통해','투자', '자산', '펀드', '상품', '수익률', '것', '자산운용', '투자자', '시장']
    stop_words=np.append(stop_words,sw)
    words = [word for word in words if word not in stop_words and len(word) > 1]
    # count the frequency of each word
    word_count = Counter(words)
    word_dict=dict(word_count)
    df_word = pd.DataFrame.from_dict({'key': list(word_dict.keys()), 'value': list(word_dict.values())})
    df_word=df_word.sort_values(by='value',ascending=False)
       
    pickle.dump(df_word, open(root+'df_word_count.pkl', 'wb')) 
    
    pickle.dump(word_count, open(root+'word_count.pkl', 'wb')) 
    pickle.dump(news_df, open(root+'news_df_etf.pkl', 'wb')) 
    #데이터 프레임 만들기

    #데이터 프레임 저장
    news_df.to_csv('{}.csv'.format(search),encoding='utf-8-sig',index=False)
    
    #검색어 입력
    search = 'ACE ETF'
    #검색 시작할 페이지 입력
    page = 1  
    #검색 종료할 페이지 입력
    page2 = 10
    
    
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
        if ("news.naver.com" in news_url_1[i]) and ("sports" not in news_url_1[i]):
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
            html_date = news_html.select_one("div#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
        # 날짜 가져오기
        news_dates.append(news_date)
    
    root='C:\\Users\\user\\Dashboard\\dataset\\'
    news_df = pd.DataFrame({'date':news_dates,'title':news_titles,'link':final_urls})
    news_contents=''.join(news_contents)
    #news_contents=news_contents.replace('인공 지능','인공지능')
    okt = Okt()
    words = okt.nouns(news_contents)
    
    sw=pd.read_excel(root+'stopwords.xlsx',dtype=str)
    sw=sw['stopword'].tolist()
    stop_words = ['산출','발생','강조','집중','정책','위해','회복','증시','뉴스','이익','기대','기관','심리','연금','가운데','개미','성장','미국','기준','투자신탁','주가','파산','안전','관련','활용','이자','업체','해외','비중','대표','테마','계좌','달러','설명','정보','확대','위기','라며','사태','삼성','미래에셋','인상','가장','규모','위험','가격','대한','상황','산업','예상','선물','때문','기간','전략','유입','종목','이상','기업','상승','수준','경우','최근','만기','대비','시작','자금','성과','포트폴리오','전망','지난해','거래','은행','개인','기록','결제','장기','포스','지난','금융투자','주식','채권','안정','예금','제공','연초','하락','상장','홈페이지','이후','매수','변동성','추종','지수','국내','증권사','수익','업무','올해','금융','공모','한국','운용','증권','통해','투자', '자산', '펀드', '상품', '수익률', '것', '자산운용', '투자자', '시장']
    stop_words=np.append(stop_words,sw)
    words = [word for word in words if word not in stop_words and len(word) > 1]
    # count the frequency of each word
    word_count = Counter(words)
    word_dict=dict(word_count)
    df_word = pd.DataFrame.from_dict({'key': list(word_dict.keys()), 'value': list(word_dict.values())})
    df_word=df_word.sort_values(by='value',ascending=False)
    
    pickle.dump(df_word, open(root+'df_word_ace.pkl', 'wb')) 
    pickle.dump(word_count, open(root+'word_count_ace.pkl', 'wb')) 
    pickle.dump(news_df, open(root+'news_df_ace.pkl', 'wb')) 
    

    #데이터 프레임 저장
    news_df.to_csv('{}.csv'.format(search),encoding='utf-8-sig',index=False)
    
    #검색어 입력
    search = '세계경제'
    #검색 시작할 페이지 입력
    page = 1  
    #검색 종료할 페이지 입력
    page2 = 10
    
    
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
        if ("news.naver.com" in news_url_1[i]) and ("sports" not in news_url_1[i]):
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
            html_date = news_html.select_one("div#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1,repl='',string=str(news_date))
        # 날짜 가져오기
        news_dates.append(news_date)
    
    root='C:\\Users\\user\\Dashboard\\dataset\\'
    news_df = pd.DataFrame({'date':news_dates,'title':news_titles,'link':final_urls})
    news_contents=''.join(news_contents)
    #news_contents=news_contents.replace('인공 지능','인공지능')
    okt = Okt()
    words = okt.nouns(news_contents)
    sw=pd.read_excel(root+'stopwords.xlsx',dtype=str)
    sw=sw['stopword'].tolist()
    stop_words = ['산출','발생','강조','집중','정책','위해','회복','증시','뉴스','이익','기대','기관','심리','연금','가운데','개미','성장','미국','기준','투자신탁','주가','파산','안전','관련','활용','이자','업체','해외','비중','대표','테마','계좌','달러','설명','정보','확대','위기','라며','사태','삼성','미래에셋','인상','가장','규모','위험','가격','대한','상황','산업','예상','선물','때문','기간','전략','유입','종목','이상','기업','상승','수준','경우','최근','만기','대비','시작','자금','성과','포트폴리오','전망','지난해','거래','은행','개인','기록','결제','장기','포스','지난','금융투자','주식','채권','안정','예금','제공','연초','하락','상장','홈페이지','이후','매수','변동성','추종','지수','국내','증권사','수익','업무','올해','금융','공모','한국','운용','증권','통해','투자', '자산', '펀드', '상품', '수익률', '것', '자산운용', '투자자', '시장']
    stop_words=np.append(stop_words,sw)
    words = [word for word in words if word not in stop_words and len(word) > 1]
    # count the frequency of each word
    word_count = Counter(words)
    word_dict=dict(word_count)
    df_word = pd.DataFrame.from_dict({'key': list(word_dict.keys()), 'value': list(word_dict.values())})
    df_word=df_word.sort_values(by='value',ascending=False)
    
    pickle.dump(df_word, open(root+'df_word_eco.pkl', 'wb')) 
    pickle.dump(word_count, open(root+'word_count_eco.pkl', 'wb')) 
    pickle.dump(news_df, open(root+'news_df_eco.pkl', 'wb')) 
    

    
    #데이터 프레임 만들기
    
    #데이터 프레임 저장
    news_df.to_csv('{}.csv'.format(search),encoding='utf-8-sig',index=False)
    
    wc.make_wordcloud()
    
    with open(root+"last_updated_wc.txt", "w") as file:
        file.write(now.strftime('%Y-%m-%d %H:%M:%S'))
    
