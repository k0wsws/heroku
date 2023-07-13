#import page1_분류별현황 as ov
import page2_investor as invt
import page3_cluster as clust
import page4_RawData as rd
#import page5_MSgen as msg
#import page6_ace_overview as ace_ov
import page7_overview as ov_new
import page8_경쟁상품비교 as p8
import page9_chat as p9
import page10_회사별현황 as p10
#import page10_회사별overview as p11
import page11_fund as p12
#import page12_fund2 as p13
import page13_comment as p14
#import page14_news as p15
import page15_all as p16
from PIL import Image
import streamlit as st
st.set_page_config(layout="wide")
from streamlit_option_menu import option_menu
import news
import datetime
import pickle
#import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import trend as td
#5.14일 추가
import related_words as related
import youtube_keywords as youtube

## 화면옵션


#st.set_option('deprecation.showPyplotGlobalUse', False)

from st_aggrid import AgGrid, JsCode, GridOptionsBuilder,ColumnsAutoSizeMode
from bokeh.plotting import figure

from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn, HTMLTemplateFormatter
root=''




##이미지
logo = Image.open('ace.jpg') 
#dong = Image.open('thumb.png') 
ACEETF = Image.open(root+'ACEETF.jpg') 
ETF = Image.open(root+'ETF.jpg') 
ECO = Image.open(root+'ECO.jpg') 
#cookie = Image.open('cookie.jfif') 
#bed = Image.open('bed.jpg') 

df_ytm=pd.read_excel(root+"ytm.xlsx")


now = datetime.datetime.now()

df_word_ace=pickle.load(open(root+'df_word_ace.pkl','rb'))    
df_wordcount=pickle.load(open(root+'df_word_count.pkl','rb'))    
df_word_eco=pickle.load(open(root+'df_word_eco.pkl','rb'))   

df_etf=pickle.load(open(root+'news_df_etf.pkl','rb'))  
df_ace=pickle.load(open(root+'news_df_ace.pkl','rb'))  
df_eco=pickle.load(open(root+'news_df_eco.pkl','rb'))  

cds = ColumnDataSource(df_etf)
columns = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">✔</a>')),
]
p = DataTable(source=cds, columns=columns, fit_columns=False, css_classes=["my_table"])

cds2 = ColumnDataSource(df_ace)
columns2 = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">✔</a>')),
]
p2 = DataTable(source=cds2, columns=columns2, fit_columns=False, css_classes=["my_table"])

cds3 = ColumnDataSource(df_eco)
columns3 = [TableColumn(field="date",title="날짜",width=100),TableColumn(field="title",title="제목",width=200),
TableColumn(field="link", title="link",width=50, formatter=HTMLTemplateFormatter(template='<p style="text-align:center;"><a href="<%= value %>"target="_blank">✔</a>')),
]
p3 = DataTable(source=cds3, columns=columns3, fit_columns=False, css_classes=["my_table"])

df_word_ace['순위'] = df_word_ace['value'].rank(method='min',ascending=False)    
df_word_ace=df_word_ace.head(10) 
df_word_ace['순위']=df_word_ace['순위'].astype('int')
df_word_ace=df_word_ace.set_index('순위')
df_word_ace.rename(columns={'value':'개수'},inplace=True)

df_wordcount['순위'] = df_wordcount['value'].rank(method='min',ascending=False) 
df_wordcount=df_wordcount.head(10)   
df_wordcount['순위']=df_wordcount['순위'].astype('int')
df_wordcount=df_wordcount.set_index('순위')
df_wordcount.rename(columns={'value':'개수'},inplace=True)

df_word_eco['순위'] = df_word_eco['value'].rank(method='min',ascending=False)    
df_word_eco=df_word_eco.head(10) 
df_word_eco['순위']=df_word_eco['순위'].astype('int') 
df_word_eco=df_word_eco.set_index('순위')
df_word_eco.rename(columns={'value':'개수'},inplace=True)

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
            
# =============================================================================
# with st.sidebar:
#     choose = option_menu("ACE DashBoard", ["ACE","OVERVIEW","분류별 현황","회사별 현황","펀드별 보유현황","펀드내 타사 보유현황","만기채권현황","경쟁상품비교","ACE 펀드별 댓글","INVESTOR","회사별 Overview","NEWS","검색어트렌드", "Cluster","시장점유율","DATA","chat"],
#                          icons=['info-circle','view-stacked','display','briefcase','basket','binoculars','cash-coin','shop','chat-left','bank','bar-chart','newspaper','columns-gap', 'collection', 'pie-chart','download','chat-dots'],
#                          menu_icon="app-indicator", default_index=0,
#                          styles={
#         "container": {"padding": "5!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"}, 
#         "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
#         "nav-link-selected": {"background-color": "#02ab21"},
#     }
#     )
#     
# =============================================================================
    
    
with st.sidebar:
    choose = option_menu("ACE DashBoard", ["ACE","NEWS", "ETF Market Overview", "ETF Analysis","FUND-ETF ANALYSIS", "BUZZ", "Cluster Map","DATA","chat"],
                         icons=['suit-heart-fill','newspaper','wifi','vector-pen','shuffle','ear','globe','battery-half','wrench'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
 
################################################ACE 소개#######################################################


if choose == "ACE":

        st.image(logo )
        st.write("“키워드로 검색한 뉴스내용에서 많이 언급되고 있는 단어”")
        with open(root+"last_updated_wc.txt", "r") as file:
                file_contents = file.read()
                st.write("Last updated: "+file_contents)                    
        col1, col2, col3, col4 = st.columns( [0.3, 0.3,0.3,0.1])
        with col1:  
            st.image(ACEETF)
            st.table(df_word_ace)
            st.bokeh_chart(p2)
            
            #p15.generate()
        with col2:
            st.image(ETF)
            st.table(df_wordcount)
            st.bokeh_chart(p)

        with col3:
            st.image(ECO)
            st.table(df_word_eco)
            st.bokeh_chart(p3)
        df=pd.read_csv(root+'top5news.csv')
        df=df.loc[:,['Link','Summary']]
        #df.rename(columns={'0':'Link'},inplace=True)
        #df.rename(columns={'1':'Summary'},inplace=True)
        st.write("“INVESTING.COM 실시간 TOP5 뉴스 요약”")
        st.table(df)  
        #btn_clicked = st.button("Click")
        #st.write(btn_clicked)
        #if btn_clicked:
        #    col1, col2 = st.columns( [0.5, 0.5])
        #    with col1:  
        #        st.image(cookie)
        #    with col2:  
        #        st.image(bed)

if choose == "ETF Market Overview":
    sub_menu = option_menu("ETF Market Overview", ["Market Overview", "시장점유율","Asset 분류별 현황", "회사별 현황","회사별 ETF 상세분석","전체ETF 현황"],
                               icons=['display', 'display-fill', 'display','display-fill','display','display-fill'],
                               menu_icon="app-indicator", default_index=0, orientation ='horizontal',
                               styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "orange", "font-size": "22px"},
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#02ab21"},
                               }
                               )
    
    if sub_menu == "Market Overview":
        #st.write("준비중") 
        ov_new.aum_load()
    
   # elif sub_menu == "Asset 분류별 현황":
   #     ov.generate()

    elif sub_menu == "회사별 현황":
        #st.write("준비중") 
        p10.generate()
       
    elif sub_menu == "회사별 ETF 상세분석":
        st.write("준비중") 
        #p11.generate()

    elif sub_menu == "시장점유율":
          st.write("준비중") 
          #msg.generate()
          
    elif sub_menu == "전체ETF 현황":
          #st.write("준비중") 
          p16.generate()   
######################################################################################################
if choose == "ETF Analysis":
    sub_menu = option_menu("ETF Analysis", [ "만기채권ETF분석","ACE경쟁상품비교", "투자자별 매매추이"],
                                 icons=['display', 'display-fill', 'display'],
                                 menu_icon="app-indicator", default_index=0,orientation ='horizontal',
                                 styles={
                                     "container": {"padding": "5!important", "background-color": "#fafafa"},
                                     "icon": {"color": "orange", "font-size": "25px"},
                                     "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                     "nav-link-selected": {"background-color": "#02ab21"},
                                 }
                                 )    

    if sub_menu == "만기채권ETF분석":
        df_ytm['AUM']=df_ytm['AUM']/1000000000
        fig3=px.scatter(df_ytm,'DURATION','YTM',text="ETF_NM",size="AUM",color="ETF_NM",title="만기채권ETF YTM-듀레이션" ,width=1500,height=800)     
        fig3.update_layout(
        font=dict(
            size=16  # Set the font size here
            )
        )
        st.plotly_chart(fig3)
    
    elif sub_menu == "ACE경쟁상품비교":
        p8.generate()

    elif sub_menu == "투자자별 매매추이":
        #st.write("준비중") 
        invt.generate()
       
######################################################################################################

if choose == "BUZZ":
    sub_menu = option_menu("BUZZ", [ "ACE ETF 토론방 모니터", "검색어트렌드","연관검색어","유튜브"],
                                 icons=['display', 'display-fill', 'display', 'display-fill'],
                                 menu_icon="app-indicator", default_index=0,orientation ='horizontal',
                                 styles={
                                     "container": {"padding": "5!important", "background-color": "#fafafa"},
                                     "icon": {"color": "orange", "font-size": "25px"},
                                     "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                     "nav-link-selected": {"background-color": "#02ab21"},
                                 }
                                 )    

    if sub_menu == "ACE ETF 토론방 모니터":
        p14.generate() 
    
    elif sub_menu == "검색어트렌드":
        td.generate()
    elif sub_menu == "연관검색어":
        related.generate()
    elif sub_menu == "유튜브":
        youtube.generate()
        
# ###############################################시장주체별#######################################################        

# if choose == "INVESTOR":
#     st.write("준비중") 
#     #invt.generate()
 
        
# ###############################################Clustering########################################################### 
        
elif choose == "Cluster Map":
#     st.write("준비중") 
      clust.generate()


# ##########################################시장점유율#############################################################


# elif choose == "시장점유율":

#     st.write("준비중") 
    
#     #msg.generate()
        
        
# ##########################################로우데이터#############################################################


elif choose == "DATA":
    #st.write("준비중") 
    
    rd.generate()
            
# ##########################################오버뷰#############################################################    
    
# elif choose == "분류별 현황" :
#     st.write("준비중") 
#     #ov.generate()

# elif choose == "회사별 Overview" :
    
#     p11.generate()
    
elif choose == "NEWS" :
    #st.write("준비중") 
    news=news.news()
    
    col3,edge2, col4 = st.columns( [0.35,0.05, 0.6])
    
    with col3:              
        st.write(news[3].astype(int))
    
    with col4:               
        st.plotly_chart(news[4], theme="streamlit", use_conatiner_width=True)

    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.write(news[1])              
    down=news[1].to_csv().encode('utf-8')

    
    st.download_button(
      label='📥 CSV로 저장',
      data=down,
      file_name="data.csv"
      )
    
    col1,edge1, col2 = st.columns( [0.45,0.1, 0.45])
    
    with col1:              
        st.plotly_chart(news[2], theme="streamlit", use_conatiner_width=True)
    
    with col2:               
        st.plotly_chart(news[0], theme="streamlit", use_conatiner_width=True)

# elif choose == "OVERVIEW" :

#     ov_new.aum_load()
    
# elif choose == "경쟁상품비교" :
    
#     try:
#         p8.generate()
#     except IndexError:
#         st.write('경쟁상품 맵핑전')
elif choose == "chat" :
    #st.write("준비중")
    p9.generate()
    
# elif choose == "회사별 현황" :
    
#     p10.generate()
    
elif choose == "FUND-ETF ANALYSIS" :
    
     p12.generate()    #st_disqus("streamlit-disqus-demo")
    
# elif choose == "만기채권현황" :
    
    
#     df_ytm['AUM']=df_ytm['AUM']/1000000000
#     fig3=px.scatter(df_ytm,'DURATION','YTM',text="ETF_NM",size="AUM",color="ETF_NM",title="만기채권ETF YTM-듀레이션" ,width=1500,height=800)     
#     fig3.update_layout(
#     font=dict(
#         size=16  # Set the font size here
#     )
# )
#     st.plotly_chart(fig3)
    
# elif choose == "펀드내 타사 보유현황" :
    
#     p13.generate() 

# elif choose == "ACE 펀드별 댓글" :
    
#     p14.generate() 
    
# elif choose == "검색어트렌드" :
    
#     td.generate() 
    
# elif choose == "전체 ETF현황" :
#     st.write("준비중") 
#     #p16.generate() 
