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
        logging.debug(f"Making request to: {FASTAPI_URL}?query={query}")
        response = requests.get(f"{FASTAPI_URL}?query={query}")
        response.raise_for_status()

        raw_data = response.text
        logging.debug(f"Raw API response: {raw_data}")

        data = response.json()
        logging.debug(f"Parsed API response: {data}")

        # Check if we have results
        results = data.get("results", [])
        if not results:
            logging.debug("No results found in API response")
            return "No results found for your query.", 200

        # Format the response for display
        formatted_lines = []
        for item in results:
            title = item.get('title', 'Untitled')
            snippet = item.get('snippet', 'No snippet available')
            if title and snippet:
                formatted_lines.append(f"{title}: {snippet}")

        if not formatted_lines:
            logging.debug("No valid results after formatting")
            return "No results found for your query.", 200

        formatted_text = "\n\n".join(formatted_lines)
        logging.debug(f"Formatted response: {formatted_text[:200]}...")  # Log first 200 chars

        return formatted_text, 200

    except requests.RequestException as e:
        logging.error(f"Error fetching Hansard data: {str(e)}")
        return jsonify({"error": "Failed to fetch Hansard data"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500