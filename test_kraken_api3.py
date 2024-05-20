import requests
import pytz
import time
from datetime import datetime, timezone, timedelta
import pandas as pd

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

def safe_request(url):
    retry_delay = 5  # start with 1 second
    max_delay = 300  # maximum delay of 5 minutes
    while True:
        response = requests.get(url)
        data = response.json()
        if 'EGeneral:Too many requests' in data['error']:
            print(f"Rate limit exceeded, waiting {retry_delay} seconds to retry...")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_delay)  # increase delay, cap at max_delay
            continue
        time.sleep (.2)
        return response


def fetch_all_trades(pair,since=0):
    first_iteration = True  # To control header writing

    print("UNIX timestamp for X days ago:", since)
    readable_timestamp = datetime.utcfromtimestamp(since).strftime('%Y-%m-%d %H:%M:%S')
    print("Last returned timestamp:", readable_timestamp)

    all_trades = []

    while True:
        url = f'https://api.kraken.com/0/public/Trades?pair={pair}&since={since}'
        print ("")
        print ("***********************")
        print(url)
        print ("***********************")
        print ("")
        response = safe_request(url)
        data = response.json()

        if data['error']:
            print("Error:", data['error'])
            break

        new_trades = data['result'][pair]
        all_trades.extend(new_trades)

        if not new_trades:
            print("No new trades fetched. Exiting...")
            break

        # Convert timestamp from UNIX to readable datetime and keep original
        for trade in new_trades:
            readable_time = datetime.fromtimestamp(trade[2], tz=timezone.utc).isoformat()
            trade.append(readable_time)  # Append new readable time to the trade data

        # Define column names including timestamp
        columns = ['price', 'volume', 'time', 'buy_sell', 'market_limit', 'miscellaneous', 'id', 'readable_time']

        # print (new_trades)
        df = pd.DataFrame(new_trades, columns=columns)

        # Append to CSV file
        if first_iteration:
            df.to_csv('trades_data.csv', mode='w', index=False,
                      header=True)  # Write file with header in first iteration
            first_iteration = False
        else:
            df.to_csv('trades_data.csv', mode='a', index=False,
                      header=False)  # Append without header in subsequent iterations

        print(f"Fetched and saved {len(new_trades)} trades. Continuing...")

        since = data['result']['last']

        # break

    return all_trades


first_iteration = True  # To control header writing

# Define the timezone for Switzerland
swiss_tz = pytz.timezone('Europe/Zurich')

# Get the current time in Switzerland's timezone
local_time = datetime.now(swiss_tz)

# Convert to UTC
utc_time = local_time.astimezone(pytz.utc)

utc_time_since = utc_time - timedelta(days=1)

since = int(time.mktime(utc_time_since.timetuple()))  # Start from the beginning or a specific timestamp

trades = fetch_all_trades('XXBTZUSD', since)  # Replace 'XXBTZUSD' with the appropriate key for your pair
print(f"Total trades fetched: {len(trades)}")
