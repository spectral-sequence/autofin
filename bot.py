import os
import ccxt
import pandas as pd
import logging
import openai

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TradingBot')

# Load environment variables
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize CCXT Binance Exchange
def initialize_exchange():
    try:
        exchange = ccxt.binance({
            'apiKey': BINANCE_API_KEY,
            'secret': BINANCE_API_SECRET,
            'enableRateLimit': True
        })
        return exchange
    except Exception as e:
        logger.error("Error initializing exchange: %s", e)
        return None

# Fetch OHLCV Data
def fetch_ohlcv_data(symbol, timeframe='1m', limit=1000):
    exchange = initialize_exchange()
    if exchange is None:
        return pd.DataFrame()  # Return empty DataFrame if exchange initialization fails

    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        logger.error("Error fetching OHLCV data: %s", e)
        return pd.DataFrame()  # Return empty DataFrame on failure

# Analyze Market Data with GPT-4
def analyze_market(data):
    try:
        prompt = f"Analyze the following market data for BTC/USDT:\n{data.describe().to_string()}\nWhat should I do? (buy/sell/hold <amount>)"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            api_key=OPENAI_API_KEY
        )
        decision = response.choices[0].text.strip()
        return decision
    except Exception as e:
        logger.error("Error analyzing market data: %s", e)
        return "hold 0"

# Parse Decision
def parse_decision(decision):
    try:
        tokens = decision.split()
        action = tokens[0]
        amount = float(tokens[1]) if len(tokens) > 1 and tokens[1].isdigit() else 0
        return action, amount
    except Exception as e:
        logger.error("Error parsing decision: %s", e)
        return "hold", 0

# Execute Trade
def execute_trade(symbol, action, amount):
    exchange = initialize_exchange()
    if exchange is None:
        logger.error("Exchange initialization failed.")
        return

    try:
        if action in ['buy', 'sell']:
            order = exchange.create_order(symbol, type='market', side=action, amount=amount)
            logger.info("Order executed: %s", order)
        else:
            logger.info("Holding, no action required.")
    except Exception as e:
        logger.error("Error executing trade: %s", e)

# Main function
def main():
    symbol = 'BTC/USDT'
    data = fetch_ohlcv_data(symbol)
    if data.empty:
        logger.error("No data fetched for analysis.")
        return

    decision = analyze_market(data)
    action, amount = parse_decision(decision)
    logger.info("Action: %s, Amount: %s", action, amount)
    execute_trade(symbol, action, amount)

if __name__ == "__main__":
    main()
