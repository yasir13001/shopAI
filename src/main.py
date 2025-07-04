from pydantic import BaseModel
from src.parser import extract_order_items, update
from src.chroma_db import match_products, load_csv_to_chroma, store_order_interaction,get_chromadb_data,chat_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from uuid import uuid4
import os
from typing import List, Optional
import json
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Allow requests from any origin (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Mount the correct static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..",".")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
def get_home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

# Trigger this function on server startup
@app.on_event("startup")
def startup_event():
    try:
        load_csv_to_chroma("Store_id_00234.csv")
    except Exception as e:
        print(f"❌ Failed to load CSV data: {e}")

class OrderRequest(BaseModel):
    user_input: str
    session_id: Optional[str] = None  # Accept session_id from frontend

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    inv_qty: int 

class UpdateOrderRequest(BaseModel):
    user_input: str
    session_id: str

@app.post("/shopai/parse_order")
async def parse_order(request: OrderRequest):
    try:
        # 1. Get or create session ID
        session_id = request.session_id or str(uuid4())
        instruction = request.user_input

        # 2. Extract products and quantities
        extracted_items = extract_order_items(instruction)

        # 3. Match products
        matched_items = match_products(extracted_items)
        chat_history = get_chromadb_data(session_id)

        if chat_history:
            last_chat = chat_history[-1]['response']
            for item in matched_items:
                item = json.dumps(item, indent=4)
                parsed = json.loads(item)
                last_chat.append(parsed)
            store_order_interaction(session_id, instruction, last_chat, chat_collection)
        else: 
            # 4. Store interaction in ChromaDB
            store_order_interaction(session_id, instruction, matched_items, chat_collection)

        chat_history = get_chromadb_data(session_id)

        # 5. Return response with session_id (optional enhancement)
        return chat_history


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/shopai/update_order")
def update_order(request: UpdateOrderRequest):

    try:
        instruction = request.user_input
        session_id = request.session_id

        chat_history = get_chromadb_data(session_id)

        # 🧠 Analyse the instruction with the current items
        updated_items = update(chat_history[-1]["response"], instruction)

        # 4. Store interaction in ChromaDB
        store_order_interaction(session_id,instruction, updated_items, chat_collection)

        # Optional: store the update instruction + result in ChromaDB if needed
        chat_history = get_chromadb_data(session_id)

        return chat_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
