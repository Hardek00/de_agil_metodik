# Tomelilla Skol- och Förskoledata Pipeline

Enkel pipeline som hämtar skol- och förskolaData från Tomelilla kommun och laddar upp RAW data till BigQuery.

## Data Source
- **URL**: https://data.tomelilla.se/rowstore/dataset/3617552e-4c28-4a46-9b74-ac8bbbfee33f
- **Typ**: JSON med alla skolor och förskolor i Tomelilla kommun
- **Uppdateras**: Regelbundet av Tomelilla kommun

## Setup

### 1. Förutsättningar
- GCP-projekt med BigQuery API aktiverat
- Service account med BigQuery-behörigheter
- Docker installerat

### 2. Konfiguration
1. Lägg din `service-account-key.json` i denna mapp
2. Ändra `GCP_PROJECT_ID` i `docker-compose.yml`

### 3. Kör Pipeline

#### Lokalt:
```bash
# Installera dependencies
pip install -r requirements.txt

# Sätt miljövariabel
export GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json
export GCP_PROJECT_ID=ditt-projekt-id

# Kör
python main.py
```

#### Med Docker:
```bash
# Bara RAW data (Extract + Load)
docker-compose up --build

# Eller kör bara transformation
docker-compose -f docker-compose-full.yml up transform

# Eller hela pipeline (E + L + T)
docker-compose -f docker-compose-full.yml up full-pipeline
```

## Vad Händer

1. **Fetch**: Hämtar aktuell skol/förskoledata från Tomelilla kommun  
2. **Raw Upload**: Laddar upp helt obehandlad data till BigQuery
3. **Metadata**: Lägger till timestamp och käll-URL

## BigQuery Schema

**ÄKTA RAW DATA** - bara 3 kolumner:
```
{
  "fetched_at": "2024-01-15T10:30:00.000000",
  "source_url": "https://data.tomelilla.se/...",
  "raw_json": "{\"resultCount\":21,\"offset\":0,\"limit\":100,\"queryTime\":4,\"results\":[{\"source\":\"1270\",\"street\":\"Rosencrantzgatan 15\",\"postalcode\":\"273 31\",\"name\":\"Allegro montessoriförskola\",\"locality\":\"Tomelilla\",\"students\":\"28\",\"id\":\"200\",\"type\":\"FS\",\"operation\":\"F\",\"lat\":\"55.54253094\",\"url\":\"http://forskolanallegro.se/\",\"long\":\"13.94951848\"}...]}"
}
```

## Riktigt RAW Approach

- **En rad per fetch** (inte per skola)
- **Hela API-responsen** lagras som JSON-sträng
- **Ingen strukturering** - 100% obehandlad data
- **Metadata** endast för spårning

För att använda data senare:
```sql
SELECT 
  JSON_EXTRACT_SCALAR(raw_json, '$.resultCount') as antal_skolor,
  JSON_EXTRACT_ARRAY(raw_json, '$.results') as skolor
FROM `din-project.raw_data.sample_data`
```

Perfect för vidare analys och transformation!