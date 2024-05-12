# data_fetcher.py

import ccxt
import pandas as pd
from config_manager import load_config
from technical_indicators import calculate_indicators  # Assuming you've a module for technical calculations

config = load_config()

def initialize_exchange():
    exchange = ccxt.binance({
        'apiKey': config['binance_api_key'],
        'secret': config['binance_api_secret'],
        'enableRateLimit': True
    })
    return exchange

def fetch_ohlcv_data(symbol, timeframe='1m', limit=1000):
    exchange = initialize_exchange()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = calculate_indicators(df)  # Calculate technical indicators
    return df
