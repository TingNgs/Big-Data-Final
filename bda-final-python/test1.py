from pytrends.request import TrendReq
import pandas as pd
from random import randint
import time

pytrend = TrendReq()
pList=[]
with open('dataLine.txt', 'r') as f:
    carNames = [line.strip() for line in f]
    for keywords in carNames:
        #print(keywords)
        keywords_list=[keywords]
        sleep_sec = randint(3,5)
        time.sleep(sleep_sec)
                         
        pytrend.build_payload(keywords_list, cat=0, timeframe='today 3-m', geo='', gprop='')
        interest_over_time_df = pytrend.interest_over_time()
        
        
with open('temp.json', 'w') as f:
    f.write(interest_over_time_df.to_json(orient='records', lines=True))

