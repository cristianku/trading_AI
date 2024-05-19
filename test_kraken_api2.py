import requests
import datetime
import time
from datetime import datetime, timezone, timedelta
from pykrakenapi import KrakenAPI
import krakenex

import time

# Calculate the timestamp for a date in the past
since_time = int(time.mktime(time.strptime('2023-01-01', '%Y-%m-%d')))


api = krakenex.API()
k = KrakenAPI(api)

# Initial OHLC dataframe
# df, last = k.get_ohlc_data("BCHUSD", ascending=True)
# df, last = k.get_ohlc_data("BCHUSD", interval=60, ascending=True)  # Fetch hourly data
df, last = k.get_ohlc_data("BCHUSD", interval=60, since=since_time, ascending=True)

df.to_csv('ohlc_data.csv', index=True)  # Set index=False if you do not want to save the index as a separate column

print(df)


