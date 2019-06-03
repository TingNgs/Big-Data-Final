from pytrends.request import TrendReq
import pandas as pd
import json

def GetKeywordsTrend(keywordsList,timeFrame,location,pytrend):
    pytrend.build_payload(keywordsList, cat=47, timeframe=timeFrame ,geo=location)
    interest_over_time_df = pytrend.interest_over_time()
    return interest_over_time_df

def GetTrendsRateData(carNames,timeFrame,location):
    pytrend = TrendReq()
    result = []
    for keyword in carNames:
        print(keyword)
        tempDF = GetKeywordsTrend([keyword],timeFrame,location,pytrend)
        temp = 0
        try:
            dataList = tempDF[keyword].tolist()
            print(dataList[len(dataList)-1],dataList[0])
            temp = ((dataList[len(dataList)-1] - dataList[0])/ dataList[0]) * 100
        except:
            temp = 0
        result.append(temp)
    return result
