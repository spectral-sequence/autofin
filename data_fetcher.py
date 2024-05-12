import ccxt
import pandas as pd
from technical_indicators import calculate_indicators

def initialize_exchange():
    # Initialize and return CCXT Binance exchange connection
    exchange = ccxt.binance({
        'apiKey': 'your-api-key',
        'secret': 'your-api-secret',
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    return exchange

def fetch_ohlcv_data(symbol, timeframe='1m', since=None, limit=1440):
    exchange = initialize_exchange()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def get_market_data(symbol):
    data = fetch_ohlcv_data(symbol)
    indicators = calculate_indicators(data)
    return data.join(indicators)

