# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 13:30:10 2023

@author: user
"""

class ACE():
    
    def ANT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
         WHERE INVEST_GB=8 and (ETF_NM LIKE 'ACE%' OR ETF_NM LIKE 'KINDEX%') ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


    def FINV():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=1 and (ETF_NM LIKE 'ACE%' OR ETF_NM LIKE 'KINDEX%')) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def BK():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=4 and (ETF_NM LIKE 'ACE%' OR ETF_NM LIKE 'KINDEX%')) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def INVT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=2 and (ETF_NM LIKE 'ACE%' OR ETF_NM LIKE 'KINDEX%') ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def ALIEN():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=9 and (ETF_NM LIKE 'ACE%' OR ETF_NM LIKE 'KINDEX%') ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

class KODEX():
    
    def ANT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=8 and ETF_NM LIKE 'KODEX%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


    def FINV():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
       WHERE INVEST_GB=1 and ETF_NM LIKE 'KODEX%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def BK():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=4 and ETF_NM LIKE 'KODEX%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def INVT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=2 and ETF_NM LIKE 'KODEX%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def ALIEN():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=9 and ETF_NM LIKE 'KODEX%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1
    
    
class tiger():
    
    def ANT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=8 and ETF_NM LIKE 'TIGER%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


    def FINV():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
       WHERE INVEST_GB=1 and ETF_NM LIKE 'TIGER%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def BK():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=4 and ETF_NM LIKE 'TIGER%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def INVT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=2 and ETF_NM LIKE 'TIGER%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def ALIEN():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=9 and ETF_NM LIKE 'TIGER%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

class kbstar():
    
    def ANT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=8 and ETF_NM LIKE 'KBSTAR%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


    def FINV():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
       WHERE INVEST_GB=1 and ETF_NM LIKE 'KBSTAR%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def BK():
        kor1 = """
        select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=4 and ETF_NM LIKE 'KBSTAR%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def INVT():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=2 and ETF_NM LIKE 'KBSTAR%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def ALIEN():
        kor1 = """
         select A.TRD_DT,replace(ETF_NM,'KINDEX','ACE') ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=9 and ETF_NM LIKE 'KBSTAR%' ) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


class sol():
    
    def ANT():
        kor1 = """
         select A.TRD_DT,ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=8 and ETF_CD IN (SELECT ETF_CD FROM FN_ETFINFO WHERE CO_NM='신한자산운용' AND TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()))) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1


    def FINV():
        kor1 = """
        select A.TRD_DT,ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=1 and ETF_CD IN (SELECT ETF_CD FROM FN_ETFINFO WHERE CO_NM='신한자산운용' AND TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()))) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND(B.CLASS_BIG LIKE '%국내%' ) AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def BK():
        kor1 = """
        select A.TRD_DT,ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=4 and ETF_CD IN (SELECT ETF_CD FROM FN_ETFINFO WHERE CO_NM='신한자산운용' AND TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()))) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' )AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def INVT():
        kor1 = """
        select A.TRD_DT,ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=2 and ETF_CD IN (SELECT ETF_CD FROM FN_ETFINFO WHERE CO_NM='신한자산운용' AND TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()))) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' ) AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1

    def ALIEN():
        kor1 = """
         select A.TRD_DT,ETF_NM,SUM,INVEST_GB  from (SELECT CONVERT(VARCHAR(20),CONVERT(datetime,TR_YMD,1),120) TRD_DT,ETF_CD,SUM(NET_AMT) OVER (PARTITION BY ETF_CD ORDER BY TR_YMD ASC) SUM,INVEST_GB FROM FN_ETFINV 
        WHERE INVEST_GB=9 and ETF_CD IN (SELECT ETF_CD FROM FN_ETFINFO WHERE CO_NM='신한자산운용' AND TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()))) A, FN_ETFINFO B WHERE A.ETF_CD=B.ETF_CD AND (B.CLASS_BIG LIKE '%국내%' ) AND B.TR_YMD=(SELECT MAX(TR_YMD) FROM FN_ETFINFO WHERE TR_YMD<=GETDATE()) ORDER BY A.ETF_CD ASC,A.TRD_DT ASC
         """
        return kor1        