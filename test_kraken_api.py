import requests
import datetime
import time

def fetch_ohlc_data(pair="XXBTZUSD", interval=1, since=None):
    url = "https://api.kraken.com/0/public/OHLC"
    params = {
        'pair': pair,
        'interval': interval,
        'since': since
    }
    response = requests.get(url, params=params)
    return response.json()

def save_ohlc_data(data, filename="bitcoin_ohlc_monthly.csv", mode='a'):
    with open(filename, mode) as file:
        if mode == 'w':  # write headers only once
            file.write("time,open,high,low,close,vwap,volume,count\n")
        for entry in data['result']['XXBTZUSD']:
            timestamp = datetime.datetime.fromtimestamp(int(entry[0])).isoformat()
            open_price = entry[1]
            high = entry[2]
            low = entry[3]
            close = entry[4]
            vwap = entry[5]
            volume = entry[6]
            count = entry[7]
            file.write(f"{timestamp},{open_price},{high},{low},{close},{vwap},{volume},{count}\n")

def main():
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    since = int(start_date.timestamp())
    last_since = None
    first_write = True
    end_time = datetime.datetime.now()

    while True:
        try:
            print(f"Fetching data since: {since}")  # Debug: print the 'since' timestamp
            data = fetch_ohlc_data(since=str(since))
            if data['error']:
                print("Error fetching data:", data['error'])
                break
            save_ohlc_data(data, mode='w' if first_write else 'a')
            first_write = False
            last_since = since
            since = int(data['result']['last'])  # Ensure 'since' is correctly updated
            print(f"New since value: {since}")  # Debug: print the new 'since' value
            print("Data fetched and saved for period starting at", datetime.datetime.fromtimestamp(last_since).isoformat())

            # Check if the last 'since' is recent enough
            if datetime.datetime.fromtimestamp(since) > end_time:
                print("Data fetching completed up to the current time.")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
        time.sleep(5)  # Sleep to avoid hitting the rate limit


if __name__ == "__main__":
    main()
