# app/parser.py

import requests

def extract_order_items(user_input):
    prompt = f"""
You are an order extraction bot. 
Extract products and quantities from the following text and return as a JSON list.

Input: "{user_input}"

Output Format Example:
[
  {{"product_name": "Oreo", "quantity": 2}},
  {{"product_name": "Coca Cola", "quantity": 1}}
]
Only output JSON. Nothing else.
"""

    # Talk to local Mistral running on Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    
    raw_output = response.json()['response']

    # Parse JSON safely
    import json
    return json.loads(raw_output)
