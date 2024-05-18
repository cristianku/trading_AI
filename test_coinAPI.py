import requests
import datetime

def fetch_data(api_key, symbol="BITSTAMP_SPOT_BTC_USD", start_time, end_time):
    url = f"https://rest.coinapi.io/v1/ohlcv/{symbol}/history"
    headers = {'X-CoinAPI-Key': api_key}
    params = {
        'period_id': '1MIN',
        'time_start': start_time.isoformat(),
        'time_end': end_time.isoformat()
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def main():
    api_key = 'your_coinapi_key'
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    end_date = datetime.datetime.now()

    data = fetch_data(api_key, start_time=start_date, end_time=end_date)
    if 'error' not in data:
        for item in data:
            print(item['time_period_start'], item['price_close'])
    else:
        print("Error fetching data:", data['error'])

if __name__ == "__main__":
    main()
