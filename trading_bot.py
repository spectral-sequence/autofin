# trader.py

from data_fetcher import initialize_exchange

def execute_trade(symbol, action, amount):
    exchange = initialize_exchange()
    if action == 'buy' or action == 'sell':
        order = exchange.create_order(symbol, type='market', side=action, amount=amount)
        return order
    else:
        print("Holding, no action required.")
        return None

