# chroma_db.py
import csv
import chromadb
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from datetime import datetime
import json


# Initialize
client = chromadb.PersistentClient(path="./chroma_data")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Separate collections
inventory_collection = client.get_or_create_collection(name="store_001")
chat_collection = client.get_or_create_collection(name="store_001_chat_history")


def load_csv_to_chroma(csv_path):
    # Only load if the collection is empty
    if inventory_collection.count() > 0:
        print(f"🟡 ChromaDB already contains {inventory_collection.count()} documents. Skipping load.")
        return

    documents = []
    ids = []
    metadatas = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_name = row["Product_Name"]
            product_id = row["Product_ID"]

            documents.append(product_name)
            ids.append(str(product_id))
            metadatas.append({
                "Category": row["Catagory"],
                "Supplier_Name": row["Supplier_Name"],
                "Stock_Quantity": row["Stock_Quantity"]
            })

    # Generate embeddings
    embeddings = embedding_model.encode(documents)

    # Add to Chroma
    inventory_collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )

    print("✅ CSV data loaded into ChromaDB.")


def match_products(extracted_items, collection = inventory_collection, top_k=1):
    results = []
    for item in extracted_items:
        query_vector = embedding_model.encode([item['product_name']])

        matches = collection.query(
            query_embeddings=query_vector.tolist(),
            n_results=top_k
        )

        if matches['documents'] and matches['ids']:
            matched_product = matches['documents'][0][0]  # Top match
            matched_id = matches['ids'][0][0]
            match_metadata = matches["metadatas"][0][0]


            results.append({
                "product_id": matched_id,
                "product_name": matched_product,
                "quantity": item['quantity'],
                "inv_qty": match_metadata["Stock_Quantity"]
                # Optional: include match distance
                # "score": matches['distances'][0][0]
            })
        else:
            # Optional: include unmatched items
            results.append({
                "product_id": None,
                "product_name": item['product_name'],
                "quantity": item['quantity'],
                "note": "No match found"
            })

    return results

def store_order_interaction(session_id, user_input, matched_items, collection=chat_collection):
    document = f"User said: {user_input}"

    metadata = {
        "session_id": session_id,
        "user_message": user_input,
        "items_response": json.dumps(matched_items),  # ✅ Serialize to JSON string
        "timestamp": datetime.utcnow().isoformat()
    }

    collection.add(
        documents=[document],
        metadatas=[metadata],
        ids=[str(uuid4())]
    )
def get_chromadb_data(session_id):
 # 🔍 Query ChromaDB using session_id
        results = chat_collection.get(
            where={"session_id": session_id}
        )
        chat_history = []
        if results and "metadatas" in results:
            for metadata in results["metadatas"]:
                user_msg = metadata.get("user_message")
                items_response_str = metadata.get("items_response")
                items_response = json.loads(items_response_str) if items_response_str else []
                chat_history.append({
                    "session_id": session_id,
                    "user_message": user_msg,
                    "response": items_response
                })
        return chat_history


