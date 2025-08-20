import os
import requests
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import psycopg2
import pendulum

app = FastAPI()
load_dotenv()

# This function fetches the weather data

def fetch_weather_data(api_url, api_key, location, date):
	# WeatherAPI history expects 'dt' and works best over HTTPS
	if api_url.startswith("http://"):
		api_url = api_url.replace("http://", "https://", 1)

	params = {
		"key": api_key,
		"q": location,  # prefer coordinates like "59.3293,18.0686"
		"dt": date,
	}

	response = requests.get(api_url, params=params, timeout=15)
	response.raise_for_status()
	print("Fetched data from API")
	return response.json()


# This function inserts one row per hour (verbatim hour JSON)

def json_to_psql(json_data):
	conn = psycopg2.connect(
		user=os.getenv("POSTGRES_USER"),
		password=os.getenv("POSTGRES_PASSWORD"),
		host="db",
		port="5432",
		database=os.getenv("POSTGRES_DB"),
	)
	cur = conn.cursor()

	for hour in json_data["hour"]:
		ingestion_timestamp = pendulum.now().format("YYYY-MM-DD:HH:mm:ss")
		modified_timestamp = pendulum.from_format(
			json_data["location"]["localtime"], "YYYY-MM-DD HH:mm"
		).format("YYYY-MM-DD:HH:mm:ss")
		id_time_epoch = hour["time_epoch"]
		data = json.dumps(hour, ensure_ascii=False)
		cur.execute(
			"""
			INSERT INTO RAW__WEATHERAPP (ingestion_timestamp, modified_timestamp, id, data)
			VALUES (%s, %s, %s, %s)
			""",
			(ingestion_timestamp, modified_timestamp, id_time_epoch, data),
		)
	conn.commit()
	cur.close()
	conn.close()
	print(f'Inserted {len(json_data["hour"])} rows')


# This function stores the full raw payload (one call -> one row)

def json_to_psql_full(full_payload: dict, request_params: dict):
	conn = psycopg2.connect(
		user=os.getenv("POSTGRES_USER"),
		password=os.getenv("POSTGRES_PASSWORD"),
		host="db",
		port="5432",
		database=os.getenv("POSTGRES_DB"),
	)
	cur = conn.cursor()
	cur.execute(
		"""
		INSERT INTO RAW__WEATHERAPP_FULL (ingestion_timestamp, params, data)
		VALUES (%s, %s, %s)
		""",
		(
			pendulum.now().to_iso8601_string(),
			json.dumps(request_params, ensure_ascii=False),
			json.dumps(full_payload, ensure_ascii=False),
		),
	)
	conn.commit()
	cur.close()
	conn.close()
	
	print("Inserted 1 full raw payload row")


@app.get("/")
def read_root():
	return "Welcome to our ingestion API"


@app.get("/ingestion")
def ingestion(location, date):
	API_URL = os.getenv("API_URL")
	API_KEY = os.getenv("API_KEY")

	if not API_URL or not API_KEY:
		raise HTTPException(status_code=500, detail="Missing API_URL or API_KEY")

	try:
		weather_data = fetch_weather_data(
			api_url=API_URL,
			api_key=API_KEY,
			location=location,
			date=date,
		)
	except requests.exceptions.RequestException as e:
		print(f"Error fetching data from API: {e}")
		raise HTTPException(status_code=502, detail="Upstream API error")

	# Store the full payload as true raw
	try:
		json_to_psql_full(
			full_payload=weather_data,
			request_params={"location": location, "date": date},
		)
	except Exception as e:
		print("Insert RAW_FULL failed:", e)

	# Also store exploded hourly rows (pragmatic raw)
	try:
		formatted_data = {
			"location": weather_data["location"],
			"hour": weather_data["forecast"]["forecastday"][0]["hour"],
		}
		json_to_psql(formatted_data)
	except Exception:
		print("Insert RAW hourly failed")

	return {"status": "ok", "stored": ["full", "hourly"]}