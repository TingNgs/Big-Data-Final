from pytrends.request import TrendReq
import pandas as pd

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()
carNames=[]
kw_list=[]
i=0
# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
with open('dataLine.txt', 'r') as f:
    carNames = [line.strip() for line in f]
    #print(len(carNames))
    for i in range(int(len(carNames)/5)):
        pytrend.build_payload(carNames[i*5:i*5+5], cat=3, timeframe='today 3-m', geo='', gprop='')
        print(carNames[i*5:i*5+5])
        interest_over_time_df = pytrend.interest_over_time()

        interest_over_time_df.index= interest_over_time_df.index.strftime(r'%d%m%Y')
    #print(interest_over_time_df.index)

    with open('temp.json', 'w') as f:
        f.write(interest_over_time_df.to_json(orient='records', lines=True))

