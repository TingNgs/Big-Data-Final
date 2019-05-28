from pytrends.request import TrendReq
import pandas as pd

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
pytrend.build_payload(kw_list=['iphone se', 'iphone 4', 'iphone 5', 'iphone 6', 'iphone 7'], cat=0, timeframe='today 3-m', geo='', gprop='')
# Interest Over Time
interest_over_time_df = pytrend.interest_over_time()

interest_over_time_df.index= interest_over_time_df.index.strftime(r'%d%m%Y')
print(interest_over_time_df.index)

with open('temp.json', 'w') as f:
    f.write(interest_over_time_df.to_json(orient='records', lines=True))
