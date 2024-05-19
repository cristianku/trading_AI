import time
import krakenex
import pandas as pd
import numpy as np
from pykrakenapi import KrakenAPI
from datetime import timedelta


def convert_to_ohlc(df, granularity):
    # Determine time frame of data
    since = df['time'].iloc[0] * 1000000000
    to =  df['time'].iloc[-1] * 1000000000

    # Create an initial data table with entries from start till end time, with steps of 5 seconds
    timestamps = pd.date_range(since, to, freq=str(granularity) + 's')

    # Initialise output dataframe
    output = pd.DataFrame(index=timestamps, columns=['open', 'high', 'low', 'close'])

    # Step through data in steps of 5 seconds
    df['dtime'] = df.index
    df = df.set_index('time')
    for i in range(0, len(output.index)):
        # Select the relevant datapoints for this step
        relevant_rows = df[
            (df['dtime'] >= output.index[i]) &
            (df['dtime'] < (output.index[i] +
                              timedelta(seconds=granularity)))
            ]

        # Convert data in time frame to OHLC data
        if len(relevant_rows) > 0 and not relevant_rows.empty:
            # open
            output.loc[output.index[i], 'open'] = relevant_rows['price'].iloc[0]
            # high
            output.loc[output.index[i], 'high'] = np.max(relevant_rows['price'])
            # low
            output.loc[output.index[i], 'low'] = np.min(relevant_rows['price'])
            # close
            output.loc[output.index[i], 'close'] = relevant_rows['price'].iloc[-1]
        else:
            for col in output.keys():
                output.loc[output.index[i], str(col)] = np.nan

    return output

api = krakenex.API()
k = KrakenAPI(api)

# Get trades data
df, last = k.get_recent_trades("BCHUSD", ascending=True)

# Convert data to OHLC data, steps of 5 seconds
df = convert_to_ohlc(df, 5)

# Infinite loop for additional OHLC data
while True:
    # Wait 60 seconds for new trades to happen
    time.sleep(60)

    # Get new trades data
    data, last = k.get_recent_trades("XBTUSD", since=last, ascending=True)

    # Convert data to OHLC data, steps of 5 seconds
    if not data.empty:
        data = convert_to_ohlc(data, 5)
        df = pd.concat([df, data])

        print(f'{len(data.index)} new data point{"s" if len(data.index) > 1 else ""} downloaded. Total: {len(df.index)} data points.')
    else:
        print("Could not find new trades. Retrying...")