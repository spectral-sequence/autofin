from data_fetcher import get_market_data
from analysis import analyze_market, parse_decision

def main():
    symbol = 'BTC/USDT'
    data = get_market_data(symbol)
    decision = analyze_market(data)
    action, amount = parse_decision(decision)
    
    if action == 'buy':
        print(f"Executing buy for {amount} units of {symbol}")
        # Add trading execution logic here
    elif action == 'sell':
        print(f"Executing sell for {amount} units of {symbol}")
        # Add trading execution logic here
    else:
        print("No action recommended.")

if __name__ == "__main__":
    main()

