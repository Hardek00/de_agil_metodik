# FastAPI: Modern API-utveckling för Data Engineers

## Vad är FastAPI?
FastAPI är ett snabbt, modernt Python-ramverk för att bygga APIs med type hints, automatisk dokumentation och asynkron support.

## Varför FastAPI?
- Snabbt (uvicorn + Starlette), bra för I/O-intensiva workloads
- Type hints + Pydantic ger automatisk validering och färre buggar
- Swagger UI och ReDoc genereras automatiskt
- Enkelt att skriva rena, testbara endpoints

## Minimalt exempel
```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/items")
def create_item(item: Item):
    return {"message": "created", "item": item}
```

### Kör och testa
```bash
pip install fastapi uvicorn[standard]
uvicorn main:app --reload
# Docs: http://127.0.0.1:8000/docs
```

## Synkront vs Asynkront (enkelt förklarat)
- **Synkront**: Funktionen väntar på ett svar innan något annat kan fortsätta. Bra när du gör enstaka, korta anrop.
- **Asynkront**: Funktionen pausar medan den väntar på svar och låter andra requests fortsätta under tiden. Bra när du gör många externa anrop eller I/O-intensivt arbete.
- Tänk: Synkront = står i kö vid en kassa; Asynkront = tar en nummerlapp, gör annat, ropas upp när det är din tur.

## Hämta extern data i en FastAPI-endpoint
### Synkront (requests)
```python
import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/external/users")
def get_external_users():
    r = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
    r.raise_for_status()
    return r.json()
```

### Asynkront (httpx)
```python
import httpx
from fastapi import FastAPI

app = FastAPI()

@app.get("/external/users_async")
async def get_external_users_async():
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get("https://jsonplaceholder.typicode.com/users")
        r.raise_for_status()
        return r.json()
```

## Jämförelse (kort) – Flask vs FastAPI
- Flask: mycket enkelt att börja med; manuell validering/dokumentation
- FastAPI: snabbare I/O, automatisk validering/dokumentation, type hints

## När använda i pipelines?
- Bygg ett enkelt insamlings-API för att ta emot data (POST), styra batchjobb, eller visa status
- För ren ingestion i batch/event är ofta ett skript/Cloud Run-job enklare och billigare
- Tänk på “scale-to-zero” i Cloud Run: API kan få kallstarter

## Vidare läsning i detta repo
- API-koncept och best practices: [api.md](./api.md)
- Praktisk datahämtning (klient): [first_api.md](./first_api.md) 