# CheckoutGPT

## Overview

**CheckoutGPT** is a smart order extraction system built using AI technologies. It processes user input to extract product names and quantities from natural language text, such as order descriptions or receipts, and matches them with actual products stored in a store's inventory. This project uses cutting-edge natural language processing (NLP) models, such as Google's **Gemini 1.5 Flash**, to generate accurate and contextually relevant product matches.

The system is designed to help businesses automate the order processing from various input formats (e.g., invoices, online orders) and integrate them with their inventory management systems.

## Features

* **Order Parsing**: Extracts product names and quantities from a given text input using a generative AI model.
* **Product Matching**: Matches extracted products with a store’s inventory stored in **ChromaDB** for accurate product recommendations.
* **FastAPI Integration**: Exposes APIs for order parsing and product matching, making it easy to integrate with other systems.

## Tech Stack

* **FastAPI**: Web framework for building APIs.
* **Google Gemini 1.5 Flash**: AI model for natural language understanding and generation.
* **ChromaDB**: Vector database for storing product embeddings and matching them with extracted products.
* **Pydantic**: Data validation library for request and response models.

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CheckoutGPT.git
cd CheckoutGPT
```

### 2. Install Dependencies

Make sure you have Python 3.8+ installed, and then install the required dependencies:

```bash
pip install -r requirements.txt
```

* `google-generativeai` for connecting with Google's Gemini AI model.
* `FastAPI` for creating the API.
* `uvicorn` for running the FastAPI server.
* `requests` for handling HTTP requests.
* `python-dotenv` for managing environment variables.

### 3. Set Up API Key

Create a `.env` file in the root of the project and add the following:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Replace `your_gemini_api_key_here` with your actual Gemini API key.

### 4. Running the Application

To run the FastAPI server:

```bash
uvicorn src.main:app --reload
```

This will start the application at `http://127.0.0.1:8000`.

### 5. API Endpoints

* **GET /**: Test endpoint to check if the server is running.

  Response:

  ```json
  {
    "message": "CheckoutGPT is up and running!"
  }
  ```

* **POST /parse\_order**: Receives a text input containing an order description and returns a list of extracted items and quantities.

  Example Request:

  ```json
  {
    "user_input": "I want to order 2 Oreo Cookies and 1 Coca Cola 500ml"
  }
  ```

  Example Response:

  ```json
  [
    {"product_name": "Oreo Cookies", "quantity": 2},
    {"product_name": "Coca Cola 500ml", "quantity": 1}
  ]
  ```

## Contributing

If you'd like to contribute to the project:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Explanation of the Project's Motive:

The primary purpose of **CheckoutGPT** is to provide a seamless and efficient solution for order extraction and product matching in real-time. It can be integrated into e-commerce platforms, retail businesses, or any system that processes orders manually. By automating the order parsing and matching process, it helps save time, reduce errors, and improve the overall customer experience. 
