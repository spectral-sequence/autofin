import openai

def analyze_market(data):
    # Convert DataFrame to a string or a structured format that GPT-4 can understand
    data_summary = data.describe().to_string()
    prompt = f"Analyze the following market data and recommend actions:\n{data_summary}\nShould I buy, sell, or hold? How much?"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

def parse_decision(decision):
    # Expected format: "buy 10", "sell 5", "hold 0"
    tokens = decision.lower().split()
    action = tokens[0]
    amount = float(tokens[1]) if len(tokens) > 1 else 0
    return action, amount

