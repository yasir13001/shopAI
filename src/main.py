from pydantic import BaseModel
from src.parser import extract_order_items
from src.chroma_db import match_products, load_csv_to_chroma
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
import os



app = FastAPI()

# Mount the correct static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..","docs")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/checkoutgpt", response_class=HTMLResponse)
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

@app.get("/checkoutgpt")
def read_root():
    return {"message": "CheckoutGPT is up and running!"}

class OrderRequest(BaseModel):
    user_input: str

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    inv_qty: int 

@app.post("/parse_order", response_model=list[OrderItem])
async def parse_order(request: OrderRequest):
    try:
        # 1. Extract products and quantities from user input
        extracted_items = extract_order_items(request.user_input)

        matched_items = match_products(extracted_items)

        # 2. Match extracted items to real products
        # matched_items = match_products(extracted_items)

        return matched_items

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
