import requests
import time

def fetch_crypto_data(api_key, symbol="BTC", market="USD", interval="daily"):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "DIGITAL_CURRENCY_DAILY",
        "symbol": symbol,
        "market": market,
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def save_data(data, filename="bitcoin_minute_data.csv"):
    with open(filename, 'w') as file:
        file.write("timestamp,open,high,low,close,volume\n")
        for time_stamp, values in data['Time Series (Crypto Intraday)'].items():
            open_price = values['1. open']
            high = values['2. high']
            low = values['3. low']
            close = values['4. close']
            volume = values['5. volume']
            file.write(f"{time_stamp},{open_price},{high},{low},{close},{volume}\n")

def main():
    api_key = 'your_api_key_here'  # Replace with your actual Alpha Vantage API key
    data = fetch_crypto_data(api_key)
    if 'Time Series (Crypto Intraday)' in data:
        save_data(data)
        print("Data has been fetched and saved successfully.")
    else:
        print("Failed to fetch data:", data.get('Note', data.get('Information', 'Unknown error')))

if __name__ == "__main__":
    main()
