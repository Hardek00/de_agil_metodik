import os, json
import requests
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

API_KEY   = os.environ["API_KEY"]
LOCATION  = os.environ.get("LOCATION", "59.3293,18.0686")
DATE      = os.environ.get("DATE", "2025-08-19")

app = FastAPI(title="Weather Ingestion API", version="1.0.0")


def fetch_weather(location: str, date: str) -> dict:
    url = "http://api.weatherapi.com/v1/history.json"
    params = {"key": API_KEY, "q": location, "dt": date}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def write_weather(data: dict, filename: str = "weather.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


@app.get("/")
def welcome_page():
   
    return {
        "service": "Weather Ingestion API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "ok", "has_api_key": bool(API_KEY), "default_location": LOCATION, "default_date": DATE}


@app.get("/weather")
def get_weather(location: str, date: str):
    loc = location or LOCATION
    d = date or DATE
    return fetch_weather(loc, d)


# Accept both GET (for easy browser testing) and POST
@app.api_route("/weather/write", methods=["GET", "POST"])
def get_and_write_weather(
    location: str | None = None,
    date: str | None = None,
    filename: str = "weather.json",
):
    loc = location or LOCATION
    d = date or DATE
    data = fetch_weather(loc, d)
    write_weather(data, filename)
    return {"message": "written", "file": filename, "location": loc, "date": d}

# Run with: uvicorn app:app --reload
