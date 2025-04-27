# app/chroma_db.py

import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.create_collection(name="products")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Fake products for demo
fake_products = [
    {"product_id": "1", "name": "Oreo Cookies"},
    {"product_id": "2", "name": "Coca Cola 500ml"},
    {"product_id": "3", "name": "Almonds Pack 200g"},
    {"product_id": "4", "name": "Oat Milk 1L"},
    {"product_id": "5", "name": "Basmati Rice 1kg"}
]

# Insert fake data into Chroma
def populate_fake_data():
    embeddings = embedding_model.encode([p['name'] for p in fake_products])
    collection.add(
        documents=[p['name'] for p in fake_products],
        embeddings=embeddings.tolist(),
        ids=[p['product_id'] for p in fake_products]
    )

populate_fake_data()

# Match user-extracted products
def match_products(extracted_items):
    results = []
    for item in extracted_items:
        query_vector = embedding_model.encode([item['product_name']])
        matches = collection.query(query_embeddings=query_vector.tolist(), n_results=1)

        if matches['documents']:
            matched_product = matches['documents'][0][0]  # top match
            results.append({
                "product_name": matched_product,
                "quantity": item['quantity']
            })
    return results
