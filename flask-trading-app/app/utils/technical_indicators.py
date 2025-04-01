import yfinance as yf
import pandas as pd
import ta
from datetime import datetime, timedelta
import numpy as np
from pandas_datareader import data as pdr
import requests
from ta.volatility import BollingerBands, AverageTrueRange
from ta.trend import MACD
from ta.momentum import RSIIndicator

def fetch_stock_data(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    # Fetch stock data
    data = yf.download(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), auto_adjust=False)

    # Keep only the second level of MultiIndex (e.g., 'Close' instead of ('AAPL', 'Close'))
    data.columns = data.columns.get_level_values(0)

    # Reset index to make 'Date' a column
    data.reset_index(inplace=True)
    data.rename(columns={"Date": "date"}, inplace=True)
    # Debugging: Check column names
    return data



# Replace with your actual FMP API Key
FMP_API_KEY = "3hm0DNDCC5NhmWRn1TDxIoHlDZnmLCLd"


def fetch_fmp_indicator(symbol, indicator):
    """Fetches a specific technical indicator from the FMP API."""
    url = f"https://financialmodelingprep.com/api/v3/technical_indicator/daily/{symbol}?type={indicator}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(response.json())
        if data:
            df = pd.DataFrame(data)[['date', indicator]].set_index('date')
            df.index = pd.to_datetime(df.index)  # Ensure datetime index
            return df
    else:
        print(response.json())
    return pd.DataFrame()

import pandas as pd

def calculate_technical_indicators(data, symbol):
    data['date'] = pd.to_datetime(data['date'])
    result = data.copy()

    # RSI
    rsi = RSIIndicator(close=result['Close'], window=14)
    result['rsi'] = rsi.rsi()

    # MACD
    macd = MACD(close=result['Close'])
    result['macd'] = macd.macd()

    # ATR
    atr = AverageTrueRange(high=result['High'], low=result['Low'], close=result['Close'], window=14)
    result['atr'] = atr.average_true_range()

    # Bollinger Bands
    bb = BollingerBands(close=result['Close'], window=20, window_dev=2)
    result['bb_low'] = bb.bollinger_lband()
    result['bb_mid'] = bb.bollinger_mavg()
    result['bb_high'] = bb.bollinger_hband()

    # Dollar Volume
    result['dollar_volume'] = result['Close'].astype(float) * result['Volume'].astype(float)

    # Garman-Klass Volatility (optional)
    result['garman_klass_vol'] = (
        0.5 * ((result['High'] / result['Low']).apply(lambda x: x**2)) -
        (2 * (result['High'] / result['Low']).apply(lambda x: x)) + 
        ((result['Close'] / result['Open']).apply(lambda x: x**2))
    ) ** 0.5

    # Convert numeric columns to float
    numeric_cols = [col for col in result.columns if col not in ['date']]
    for col in numeric_cols:
        result[col] = result[col].astype(float)

    print("Result columns:", result.columns.tolist())
    print("Result head:\n", result.head())
    return result




def preprocess_data(data):
    data = data[[ 'Close', 'High', 'Low', 'Open', 'Volume', 'garman_klass_vol', 'rsi', 'bb_low', 'bb_mid', 'bb_high', 'atr', 'macd', 'dollar_volume']]

    return data.iloc[-1:]