# Övningar: API och Ingestion

Nedan följer fyra övningar som bygger på varandra. Målet är att läsa API‑dokumentation, hämta data på ett robust sätt, och paketera detta i en liten tjänst.

---

dokumentation för requests biblioteket: https://requests.readthedocs.io/en/latest/

## Övning 1: Requests‑klient (grunder)
Bygg en enkel Python‑klient som hämtar data från ett publikt API.

- Steg:
  1. Skapa `client.py` som hämtar JSON (t.ex. `https://data.tomelilla.se/rowstore/dataset/3617552e-4c28-4a46-9b74-ac8bbbfee33f`).
  2. Lägg till `timeout`, `raise_for_status()` och enkel felhantering (skriv ut statuskod och feltext vid misslyckande).
  3. Spara svaret som rådata.
- Acceptanskriterier:
  - Körning skapar `raw/users.json` med giltig JSON.
  - Programmet bryter inte vid nätverksfel, utan loggar begripligt fel.
- Hints:
  - `requests.get(url, timeout=10)`

---

## Övning 2: WeatherAPI – nyckel i .env + rätt parametrar
Bygg en ingestion mot WeatherAPI där du själv läser dokumentationen och väljer rätt endpoint/parametrar.

- Steg:
  1. Skapa konto och hämta API‑nyckel på WeatherAPI: [weatherapi.com](https://www.weatherapi.com/).
  2. Läs dokumentationen och välj endpoint (t.ex. `current.json`, `forecast.json` eller `history.json` beroende på din plan). Identifiera vilka query‑parametrar som krävs (t.ex. `key`, `q`, ev. `dt` eller `days`).
  3. Lägg `API_KEY` i `.env` och läs in med `python-dotenv` (ingen hårdkodning i koden).
  4. Skriv `weather_client.py` som hämtar väder för en plats (`q`). Använd helst koordinater `lat,lon` (t.ex. `59.3293,18.0686`).
  5. Lägg till `timeout` och `raise_for_status()`. Vid 4xx/5xx – skriv ut statuskod och svarstext.
  6. Spara råsvaret som JSON till `raw/weather.json`.
- Acceptanskriterier:
  - Nyckeln läses från `.env` (inte hårdkodad).
  - Körning producerar `raw/weather.json` med giltig JSON via HTTPS.
  - Programmet hanterar fel (t.ex. 400/401/429/5xx) utan att krascha okontrollerat.
- Hints:
  - Parametrar skickas som `params={"key": API_KEY, "q": "59.3293,18.0686"}` (+ `dt` eller `days` om relevant).
  - Namnbaserad `q` ("Stockholm") kan ibland ge fel – koordinater är stabilt. Läs även `search.json` i dokumentationen om du vill lösa namn→koordinater.
  - Dokumentation och exempel finns på [weatherapi.com](https://www.weatherapi.com/).

---

## Övning 3: Arbetsförmedlingen JobSearch – jobb i Stockholm efter 2025‑08‑19 (utan nyckel)
Läs dokumentationen och hämta platsannonser publicerade efter angivet datum för Stockholm.

- Steg:
  1. Läs API‑introduktion och JobSearch‑dokumentation: [Arbetsförmedlingens Platsannonser](https://data.arbetsformedlingen.se/data/platsannonser/) och API‑basen [jobsearch.api.jobtechdev.se](https://jobsearch.api.jobtechdev.se/).
  2. Identifiera endpoint och query‑parametrar för:
     - publiceringsdatum (t.ex. "published‑after" i ISO8601)
     - plats/område (Stockholm – välj rätt fält enligt dokumentationen: fritext, kommun, region eller koordinater/geo)
     - paginering (limit/offset eller next‑länk) om det behövs
  3. Implementera `af_client.py` som:
     - gör en GET‑förfrågan med ovan parametrar
     - hanterar paginering om svaret indikerar fler sidor
     - sparar rå JSON till `raw/af_stockholm_after_2025‑08‑19.json`
- Acceptanskriterier:
  - Användning av korrekt datumformat (ISO: `2025-08-19`).
  - Resultatet innehåller endast annonser publicerade efter 2025‑08‑19 och avser Stockholm enligt valt filterfält.
  - Fel‑ och nätverkshantering: `timeout` + `raise_for_status()` och begriplig logg vid fel.
- Hints:
  - Läs parameternamn noga i docs (t.ex. "published‑after", "q", "municipality", "region", "offset", "limit").
  - Sortera på publiceringsdatum om API:et stödjer det för att förenkla paginering.
  - Spara hela råsvaret, inte bara delar – du kan filtrera i senare steg.

---

## Övning 4: FastAPI‑wrapper med /, /health, /fetch, /fetch_and_write
Gör en tunn FastAPI‑tjänst som kapslar din ingestion.

- Steg:
  1. Skapa `app.py` (FastAPI) med:
     - `GET /` – enkel preview (namn, version, länk till `/docs`).
     - `GET /health` – returnera `{status: ok}` + enklare metadata.
     - `GET /fetch` – anropa din klient och returnera JSON (t.ex. `location`/`date` som query‑params om väder‑exemplet används).
     - `POST /fetch_and_write` – hämta och skriv till fil (`filename` som query‑param eller body).
  2. Läs konfiguration (API‑nyckel, standardparametrar) från `.env`.
  3. Kör med `uvicorn` och testa via `/docs`.
- Acceptanskriterier:
  - Alla fyra endpoints fungerar och fel vid upstream visas som 4xx/5xx.
  - Inga hemligheter i URL:er eller loggar (nyckel via env eller header).
- Hints:
  - Exponera endast säkra fält i `/health`.
  - Återanvänd funktionerna från Övning 1–3.

---