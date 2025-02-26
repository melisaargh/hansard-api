from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your deployed FastAPI API URL
FASTAPI_URL = "https://hansard-api.onrender.com/get_hansard"

@app.route("/fetch_hansard", methods=["GET"])
def fetch_hansard():
    query = request.args.get("query", "encryption")  # Default to 'encryption'
    
    # Fetch Hansard data from your FastAPI API
    response = requests.get(f"{FASTAPI_URL}?query={query}")

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch Hansard data"}), 500

    data = response.json()

    # Format the response for GPT
    formatted_text = "\n".join(
        [f"{item['title']}: {item['snippet']}" for item in data.get("results", [])]
    )

    return formatted_text, 200  # Returns plain text (GPT-friendly)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

