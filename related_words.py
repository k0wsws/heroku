import requests
from bs4 import BeautifulSoup
from datetime import date
import streamlit as st
import pandas as pd



def naver_related_keyword(keyword):
    ## 모바일 환경에서
    url = 'https://m.search.naver.com/search.naver?query=' + keyword
    headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36')}

    rel_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(rel_response.text, 'html.parser')
    a_tags = soup.select('div#_related_keywords_aside > div > div > div > a')

    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=' + keyword
    rel_response = requests.get(url, headers=headers)
    soup = BeautifulSoup(rel_response.text, 'html.parser')
    lis = soup.select('#nx_footer_related_keywords > div > div.related_srch > ul > li')

    if len(lis):
        related_keywords = []
        for li in lis:
            related_keywords.append(li.text.strip())
    else:
        st.warning('네이버 연관검색어 없음!!')

    return related_keywords

def generate():
    # Streamlit 앱 구성
    st.title("네이버 연관검색어 출력")
    
    # 사용자로부터 단어 입력 받기
    keyword = st.text_input("연관검색어를 찾을 단어를 입력하세요:")
    
    # 버튼 클릭 이벤트 핸들링
    if st.button("연관검색어 조회"):
        related_keywords = naver_related_keyword(keyword)
    
        if related_keywords:
            new_keywords = pd.DataFrame()
    
            for i in range(5):
                new_keywords = new_keywords.append({'검색어': keyword, '연관검색어': related_keywords}, ignore_index=True)
                keyword = related_keywords[0]
                related_keywords = naver_related_keyword(keyword)
    
            st.dataframe(new_keywords)
        else:
            st.warning('네이버 연관검색어를 찾을 수 없습니다.')