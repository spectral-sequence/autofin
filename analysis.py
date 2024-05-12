# analysis.py

import openai
from config_manager import load_config

config = load_config()

def analyze_market(data):
    # Prepare a detailed prompt with market summary and indicators
    summary_stats = data.describe().to_string()
    latest_data = data.iloc[-1].to_dict()
    prompt = f"Analyze the following market data for BTC/USDT:\n{summary_stats}\nLatest data: {latest_data}\nWhat should I do? (buy/sell/hold <amount>)"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        api_key=config['openai_api_key']
    )
    decision = response.choices[0].text.strip()
    return decision

def parse_decision(decision):
    tokens = decision.split()
    action = tokens[0]
    amount = float(tokens[1]) if len(tokens) > 1 and tokens[1].isdigit() else 0
    return action, amount
