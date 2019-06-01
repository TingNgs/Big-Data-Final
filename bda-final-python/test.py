from pytrends.request import TrendReq
import pandas as pd
import statistics
import time
import json

pList = []
pytrend = TrendReq()
timeFrame = "today 1-m"
with open('./data/CarNameData.txt') as json_file:  
    carNames = json.load(json_file)
    for keywords in carNames:
        print(keywords)

        keywordsList = [keywords]
        pytrend.build_payload(keywordsList, cat=47, timeframe=timeFrame, geo='', gprop='')
        interest_over_time_df = pytrend.interest_over_time()

        print(interest_over_time_df)

        




