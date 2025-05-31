from pydantic import BaseModel
from src.parser import extract_order_items,analyse
from src.chroma_db import match_products, load_csv_to_chroma, store_order_interaction, collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from uuid import uuid4
import os
from typing import List, Optional
import json





app = FastAPI()

# Mount the correct static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..","docs")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/checkitout", response_class=HTMLResponse)
def get_home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    with open(index_path, "r") as f:
        return f.read()


# Trigger this function on server startup
@app.on_event("startup")
def startup_event():
    try:
        load_csv_to_chroma("Store_id_00234.csv")
    except Exception as e:
        print(f"❌ Failed to load CSV data: {e}")

@app.get("/checkitout")
def read_root():
    return {"message": "Checkitout is up and running!"}

class OrderRequest(BaseModel):
    user_input: str
    session_id: Optional[str] = None  # Accept session_id from frontend

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    inv_qty: int 

class UpdateOrderRequest(BaseModel):
    session_id: str
    items: List[OrderItem]
    instruction: str

class ParseOrderResponse(BaseModel):
    items: list[OrderItem]
    session_id: str

@app.post("/parse_order")
async def parse_order(request: OrderRequest ,  response_model=ParseOrderResponse):
    try:
        # 1. Get or create session ID
        session_id = request.session_id or str(uuid4())

        # 2. Extract products and quantities
        extracted_items = extract_order_items(request.user_input)

        # 3. Match products
        matched_items = match_products(extracted_items)

        # 4. Store interaction in ChromaDB
        store_order_interaction(session_id, request.user_input, matched_items, collection)

        # 5. Return response with session_id (optional enhancement)
        return {"session_id":session_id,"items": matched_items}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/update_order")
def update_order(request: UpdateOrderRequest):

    try:
        current_items = request.items
        instruction = request.instruction
        session_id = request.session_id

        # 🔍 Query ChromaDB using session_id
        results = collection.get(
            where={"session_id": session_id}
        )
        chat_history = []
        if results and "metadatas" in results:
            for metadata in results["metadatas"]:
                user_msg = metadata.get("user_message")
                items_response_str = metadata.get("items_response")
                items_response = json.loads(items_response_str) if items_response_str else []
                chat_history.append({
                    "user": user_msg,
                    "response": items_response
                })
        # 🧠 Analyse the instruction with the current items
        updated_items = analyse(items_response, instruction)

        # Optional: store the update instruction + result in ChromaDB if needed

        return {
            "updated_items": updated_items,
            "chat_history": chat_history  # Optional: useful for frontend to show
        }


        return 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))