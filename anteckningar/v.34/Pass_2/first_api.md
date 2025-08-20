# Ditt första API-anrop (praktisk guide)

Se också: API-koncept [api.md](./api.md) och FastAPI-intro [fastapi.md](./fastapi.md).

## Vad vi ska göra
Hämta data från internet med Python så enkelt som möjligt.

---

## Installera requests
```bash
pip install requests
```

## Exempel 1: Hämta en resurs
```python
import requests

resp = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
resp.raise_for_status()
print(resp.json())
```

## Exempel 2: Hämta flera och iterera
```python
import requests

resp = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
users = resp.json()
for u in users:
    print(f"Namn: {u['name']}, Email: {u['email']}")
```

## Exempel 3: Kontrollera statuskod
```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
if r.status_code == 200:
    print("OK", r.json()["name"])
else:
    print("Fel:", r.status_code)
```

## Felsökning och best practices
- Sätt `timeout` och använd `resp.raise_for_status()`
- Hantera undantag (nätverkstidout, HTTPError)
- Respektera paginering och rate limits
- Logga URL, statuskod och fel

```python
import requests
from requests.exceptions import RequestException, Timeout, HTTPError

try:
    r = requests.get("https://api.example.com/data", timeout=10)
    r.raise_for_status()
    data = r.json()
except (Timeout, HTTPError, RequestException) as e:
    print("API-fel:", e)
```

---

## Sammanfattning
- Du kan nu hämta data med `requests`
- Du vet hur du kontrollerar statuskoder och hanterar fel
- Nästa steg: använd data i din pipeline eller bygg ett eget API med FastAPI


