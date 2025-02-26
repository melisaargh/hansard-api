from fastapi import FastAPI
import requests

app = FastAPI()

# TheyWorkForYou API details
TWFY_API_KEY = "AFwZvbBhrawsAryA6uArH2Kw"  # Replace with your own API key
TWFY_BASE_URL = "https://www.theyworkforyou.com/api/getHansard"

@app.get("/get_hansard")
def get_hansard(query: str = "climate change", output: str = "js"):
    """Fetch Hansard records from TheyWorkForYou API."""
    params = {
        "key": TWFY_API_KEY,
        "search": query,
        "output": output
    }
    response = requests.get(TWFY_BASE_URL, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
