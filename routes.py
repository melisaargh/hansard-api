from flask import request, jsonify, render_template
from app import app
import requests
import logging
import urllib.parse

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

    # URL encode the query parameter
    encoded_query = urllib.parse.quote(query)
    request_url = f"{FASTAPI_URL}?query={encoded_query}"

    logging.debug(f"Making request to: {request_url}")

    try:
        # Fetch Hansard data from your FastAPI API
        response = requests.get(request_url)
        logging.debug(f"Response status code: {response.status_code}")

        # Log raw response for debugging
        raw_response = response.text
        logging.debug(f"Raw response: {raw_response[:500]}...")  # First 500 chars

        if response.status_code != 200:
            logging.error(f"API returned status code {response.status_code}")
            return jsonify({"error": "Failed to fetch Hansard data"}), 500

        try:
            data = response.json()
            logging.debug(f"Parsed JSON data: {str(data)[:500]}...")  # First 500 chars
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {str(e)}")
            return jsonify({"error": "Invalid response format from API"}), 500

        # Check for rows instead of results
        rows = data.get("rows", [])
        if not rows:
            logging.debug("No rows found in API response")
            return "No results found for your query.", 200

        formatted_lines = []
        for item in rows:
            body = item.get('body', '')
            if body:
                # Remove HTML tags and format the text
                body = body.replace('<p>', '').replace('</p>', '\n')
                formatted_lines.append(body)

        if not formatted_lines:
            return "No results found for your query.", 200

        formatted_text = "\n\n".join(formatted_lines)
        return formatted_text, 200

    except requests.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return jsonify({"error": "Failed to fetch Hansard data"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500