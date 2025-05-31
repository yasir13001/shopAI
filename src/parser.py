# app/parser.py

from pathlib import Path
import os
from dotenv import load_dotenv
import requests
import json
import google.generativeai as genai

# Load the environment variables from .env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

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

    # Get response from Gemini
    response = model.generate_content(prompt)
    raw_output = response.text.strip()

    # Clean up: remove code fences if present
    if raw_output.startswith("```json"):
        raw_output = raw_output.strip("```json").strip("```").strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nRaw Output: {raw_output}")

def update(query, instruction):
    prompt = f"""
You are an intelligent bot. 
instruction: "{instruction}"
input: "{query}"
output format example: 
[
        {{"product_id": "38-555-9147","product_name": "Black Coffee","quantity": 5,"inv_qty": 62}}
]
Act on instruction and return only the list of items in the given format
  
Only output JSON. Nothing else.
"""
    # Get response from Gemini
    response = model.generate_content(prompt)
    raw_output = response.text.strip()

    # Clean up: remove code fences if present
    if raw_output.startswith("```json"):
        raw_output = raw_output.strip("```json").strip("```").strip()
        
    return json.loads(raw_output)
