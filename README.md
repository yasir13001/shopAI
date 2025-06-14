# ShopAI

## Overview

**ShopAI** is a smart order extraction system powered by AI. It processes natural language input like:

> “Order 2 kg Sugar, 5 Black Coffee, 5 Carrots, and 1 litre Milk”

to extract product names and quantities, and matches them with items in your store’s inventory.

It uses cutting-edge models such as **Google's Gemini 1.5 Flash** and stores inventory data as vector embeddings in **ChromaDB** for accurate and scalable product matching.

This system is ideal for automating order processing from voice assistants, customer service chatbots, retail systems, or online ordering platforms.

---

### 📽 Demo Video

🎬 [Click here to watch the demo](assets/demo.mp4)


## ✨ Features

* **Natural Language Order Parsing** – Extracts products and quantities from user text.
* **Product Matching with Vector Search** – Finds the closest match in your store’s inventory using vector embeddings.
* **Inventory-aware Matching** – Includes stock quantity in the response.
* **FastAPI Backend** – RESTful API built for integration into any frontend.
* **ChromaDB Vector Store** – Persistent embedding storage for fast, similarity-based lookups.

---

## 🛠 Tech Stack

* **FastAPI** – High-performance Python web framework.
* **Google Gemini 1.5 Flash** – NLP model for text understanding and generation.
* **ChromaDB** – Vector database to store and query product embeddings.
* **Pydantic** – FastAPI schema validation.
* **python-dotenv** – For secure API key management.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ShopAI.git
cd ShopAI
```

### 2. Install Dependencies

Make sure Python 3.8+ is installed:

```bash
pip install -r requirements.txt
```

This installs:

* `google-generativeai`
* `fastapi`
* `uvicorn`
* `requests`
* `python-dotenv`
* `chromadb`
* Any other required packages

### 3. Set Up Your API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace with your actual Gemini API key.

---

### 4. Run the Application

```bash
uvicorn src.main:app --reload
```

Visit: [http://127.0.0.1:8000/shopai](http://127.0.0.1:8000/shopai)

---

## 📡 API Endpoints

### `GET /`

Simple health check.

**Response:**

```json
{ "message": "ShopAI is up and running!" }
```

---

### `POST /parse_order`

Sends an order string and receives matched product details from inventory.

**Request:**

```json
{
  "user_id": 1,
  "user_input": "order 2 kg Sugar and 5 Black coffee 5 carrots and 1 litre Milk"
}
```

**Response:**

```json
[
    {
        "product_id": "40-003-7322",
        "product_name": "White Sugar",
        "quantity": 2,
        "inv_qty": 13
    },
    {
        "product_id": "38-555-9147",
        "product_name": "Black Coffee",
        "quantity": 5,
        "inv_qty": 62
    },
    {
        "product_id": "05-720-8792",
        "product_name": "Carrot",
        "quantity": 5,
        "inv_qty": 80
    },
    {
        "product_id": "00-963-2193",
        "product_name": "Milk",
        "quantity": 1,
        "inv_qty": 43
    }
]
```

---

## 📁 Directory Structure

```
ShopAI/
├── LICENSE
├── README.md
├── Store_id_00234.csv             # Inventory CSV file
├── docs/
│   └── index.html                 # Frontend entry point (for GitHub Pages)
├── requirements.txt               # Python dependencies
├── src/
│   ├── __init__.py                # Makes src a Python package
│   ├── chroma_db.py               # ChromaDB-related logic
│   ├── main.py                    # FastAPI server
│   └── parser.py                  # Order parsing logic
└── start_server.sh                # Shell script to start the FastAPI server
```

---

## 🧠 Project Motivation

Manual order entry is slow, error-prone, and inefficient. **ShopAI** automates this process by understanding user input using AI and mapping it directly to your product inventory.

**Use cases include:**

* Retail stores automating sales desk input
* Voice assistant integration
* Inventory chatbots
* E-commerce platforms with smart order handling

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b my-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to your branch: `git push origin my-feature`
5. Open a Pull Request

---

## 🪪 License

MIT License – see the [LICENSE](LICENSE) file.
