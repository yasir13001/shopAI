# app/main.py

from pydantic import BaseModel
from parser import extract_order_items
from chroma_db import match_products
from fastapi import FastAPI
from fastapi import HTTPException


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "CheckoutGPT is up and running!"}

class OrderRequest(BaseModel):
    user_input: str

class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int

@app.post("/parse_order", response_model=list[OrderItem])
async def parse_order(request: OrderRequest):
    try:
        # 1. Extract products and quantities from user input
        extracted_items = extract_order_items(request.user_input)

        # 2. Match extracted items to real products
        matched_items = match_products(extracted_items)

        return matched_items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
