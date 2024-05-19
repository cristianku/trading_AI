import requests
import datetime
import time
from datetime import datetime, timezone, timedelta
from pykrakenapi import KrakenAPI
import krakenex

import pytz

api = krakenex.API()
k = KrakenAPI(api)

# Initial OHLC dataframe
df, last = k.get_ohlc_data("BCHUSD", ascending=True)


import pandas as pd

def sort_csv_by_timestamp(filename):
    df = pd.read_csv(filename)
    df['time'] = pd.to_datetime(df['time'])
    df = df.sort_values('time')
    df.to_csv(filename, index=False)


def fetch_ohlc_data(api_key, pair, interval, since):
    """Fetch OHLC data from Kraken API."""
    url = "https://api.kraken.com/0/public/OHLC"
    headers = {'API-Key': api_key}
    params = {
        'pair': pair,
        'interval': interval,
        'since': since
    }
    print("")
    print("************************************")
    print("Making API call to:", url)
    print("With parameters:", params)
    print("first returned timestamp:", datetime.utcfromtimestamp(since).strftime('%Y-%m-%d %H:%M:%S'))
    print("************************************")
    print("")

    response = requests.get(url, headers=headers, params=params)
    response_data = response.json()
    # print("API response:", response_data)
    return response_data

def save_ohlc_data(data, pair, filename="bitcoin_ohlc.csv", first_run=False):
    """Save OHLC data to a CSV file."""
    mode = 'w' if first_run else 'a'
    header = "time,open,high,low,close,vwap,volume,count\n" if first_run else ''
    with open(filename, mode) as file:
        if first_run:
            file.write(header)
        if 'result' in data and pair in data['result']:
            for entry in data['result'][pair]:
                timestamp = datetime.fromtimestamp(int(entry[0]), tz=timezone.utc).isoformat()
                open_price, high, low, close, vwap, volume, count = entry[1:8]
                file.write(f"{timestamp},{open_price},{high},{low},{close},{vwap},{volume},{count}\n")

def main():
    current_time = datetime.now(timezone.utc)
    three_days_ago = int((current_time - timedelta(days=3)).timestamp())

    api_key = 'your_api_key'  # Your Kraken API key
    pair = "XXBTZUSD"  # Kraken API pair ID
    interval = 1  # Time frame interval in minutes

    # Define the timezone for Switzerland
    swiss_tz = pytz.timezone('Europe/Zurich')

    # Get the current time in Switzerland's timezone
    local_time = datetime.now(swiss_tz)

    # Convert to UTC
    utc_time = local_time.astimezone(pytz.utc)

    utc_time_one_hour_ago = utc_time - timedelta(hours=48)

    since = int(utc_time_one_hour_ago.timestamp())

    first_run = True
    while True:
        print (since)
        readable_timestamp = datetime.utcfromtimestamp(since).strftime('%Y-%m-%d %H:%M:%S')

        print("Last returned timestamp:", readable_timestamp)

        data = fetch_ohlc_data(api_key, pair, interval, since)
        if 'error' in data and data['error']:
            print("Error:", data['error'])
            # break

        save_ohlc_data(data, pair, first_run=first_run)
        first_run = False  # Set first_run to False after the first data save

        if 'result' in data and 'last' in data['result']:
            # since = data['result']['last']  # Update since to the last returned timestamp
            first = int(data['result'][pair][0][0])  # First element's timestamp
            print("first returned timestamp:", datetime.utcfromtimestamp(first).strftime('%Y-%m-%d %H:%M:%S'))

            last = int(data['result'][pair][0][0])  # First element's timestamp
            print("Last returned timestamp:", datetime.utcfromtimestamp(last).strftime('%Y-%m-%d %H:%M:%S'))

            since = last   # Subtract 6 hours in seconds
            if since < three_days_ago:
                print("Timestamp is older than three days. Stopping data fetch.")
                break

        else:
            print("Completed fetching data.")
            break

        time.sleep(5)  # Sleep to respect API rate limits
        print ("next round")
        break

    sort_csv_by_timestamp("bitcoin_ohlc.csv")

if __name__ == "__main__":
    main()
