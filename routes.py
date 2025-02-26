from flask import request, jsonify, render_template
from app import app
import requests
import logging

# Your deployed FastAPI API URL
FASTAPI_URL = "https://hansard-api.onrender.com/get_hansard"

@app.route("/")
def index():
    """Render the main page with a search interface"""
    return render_template("index.html")

@app.route("/fetch_hansard", methods=["GET"])
def fetch_hansard():
    """Endpoint to fetch Hansard data"""
    query = request.args.get("query", "encryption")  # Default to 'encryption'

    logging.debug(f"Fetching Hansard data for query: {query}")

    try:
        # Fetch Hansard data from your FastAPI API
        response = requests.get(f"{FASTAPI_URL}?query={query}")
        response.raise_for_status()

        data = response.json()
        logging.debug(f"Received API response: {data}")

        if not data.get("results"):
            return "No results found for your query.", 200

        # Format the response for GPT
        formatted_text = "\n".join(
            [f"{item.get('title', 'Untitled')}: {item.get('snippet', 'No snippet available')}" 
             for item in data.get("results", [])]
        )

        if not formatted_text.strip():
            return "No results found for your query.", 200

        return formatted_text, 200

    except requests.RequestException as e:
        logging.error(f"Error fetching Hansard data: {str(e)}")
        return jsonify({"error": "Failed to fetch Hansard data"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500