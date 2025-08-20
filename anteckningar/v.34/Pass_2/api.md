# APIs: Grunderna för Data Engineers

> Denna sida förklarar API-koncept, REST/JSON och best practices.
> För praktisk datahämtning, se: [first_api.md](./first_api.md). För ramverk och exempel på att bygga egna APIs, se: [fastapi.md](./fastapi.md).

## Vad är ett API?

**API** står för **Application Programming Interface** - ett sätt för olika program att "prata" med varandra.

### Enkla analogier:
- **Restaurant:** Du (klienten) ger beställning till servitören (API:et) som tar det till köket (servern) och kommer tillbaka med maten (data)
- **Eluttag:** Du stoppar in sladden (request) och får elektricitet (data) utan att behöva veta hur kraftverket fungerar

### Varför är APIs viktiga för data engineers?
- **Hämta data** från externa tjänster (väder, aktiekurser, sociala medier)
- **Integrera system** - få olika applikationer att samarbeta
- **Mikroservices** - dela upp stora system i mindre, hanterbara delar
- **Automation** - låta program utföra uppgifter automatiskt

---

## JSON: Språket för APIs

**JSON** (JavaScript Object Notation) är det vanligaste formatet för att skicka data mellan system.

### JSON ser ut så här:
```json
{
  "name": "Anna Andersson",
  "age": 28,
  "city": "Stockholm",
  "skills": ["Python", "SQL", "Docker"],
  "is_employed": true,
  "salary": null
}
```

### JSON vs Python:
```python
# JSON data (som text/string)
json_string = '{"name": "Anna", "age": 28}'

# Python dictionary (objekt i minnet)
python_dict = {"name": "Anna", "age": 28}

# Konvertera mellan dem
import json

# JSON → Python
data = json.loads(json_string)
print(data["name"])  # "Anna"

# Python → JSON
json_output = json.dumps(python_dict)
print(json_output)  # '{"name": "Anna", "age": 28}'
```

### Varför JSON?
- **Läsbart** för människor
- **Lätt att parsa** för datorer
- **Språkoberoende** - fungerar med Python, JavaScript, Java, etc.
- **Kompakt** - mindre overhead än XML

---

## REST APIs: Regler för att bygga bra APIs

**REST** (Representational State Transfer) är en uppsättning designprinciper för APIs.

### REST-principer:

#### 1. **Resurser identifieras med URLs**
```
GET /users          # Alla användare
GET /users/123      # Användare med ID 123
GET /users/123/posts # Alla inlägg från användare 123
```

#### 2. **HTTP-metoder beskriver vad du vill göra**
| Metod | Syfte | Exempel |
|-------|-------|---------|
| `GET` | Hämta data | `GET /users` - Lista användare |
| `POST` | Skapa ny data | `POST /users` - Skapa ny användare |
| `PUT` | Uppdatera helt | `PUT /users/123` - Ersätt användare |
| `PATCH` | Uppdatera delvis | `PATCH /users/123` - Ändra bara namn |
| `DELETE` | Ta bort | `DELETE /users/123` - Ta bort användare |

#### 3. **HTTP-statuskoder förklarar vad som hände**
```python
200 OK          # Allt gick bra
201 Created     # Ny resurs skapades
400 Bad Request # Du skickade felaktig data
401 Unauthorized # Du är inte inloggad
404 Not Found   # Resursen finns inte
500 Server Error # Något gick fel på servern
```

---

## Använda APIs: Requests Library

### Installation:
```bash
pip install requests
```

### Grundläggande GET-request:
```python
import requests

# Hämta data från ett API
response = requests.get('https://jsonplaceholder.typicode.com/users')

# Kontrollera att det gick bra
if response.status_code == 200:
    users = response.json()  # Konverterar JSON till Python dict
    print(f"Hittade {len(users)} användare")
    print(f"Första användaren: {users[0]['name']}")
else:
    print(f"Fel: {response.status_code}")
```

### POST-request (skicka data):
```python
import requests

# Data att skicka
new_user = {
    "name": "Anna Andersson",
    "email": "anna@example.com",
    "city": "Stockholm"
}

# Skicka POST-request
response = requests.post(
    'https://jsonplaceholder.typicode.com/users',
    json=new_user  # requests konverterar automatiskt till JSON
)

if response.status_code == 201:
    created_user = response.json()
    print(f"Användare skapad med ID: {created_user['id']}")
```

### Hantera headers och autentisering:
```python
import requests

# Headers för autentisering
headers = {
    'Authorization': 'Bearer YOUR_API_TOKEN',
    'Content-Type': 'application/json'
}

# GET med headers
response = requests.get(
    'https://api.example.com/data',
    headers=headers
)

# Query parameters
params = {
    'limit': 10,
    'sort': 'name',
    'filter': 'active'
}

response = requests.get(
    'https://api.example.com/users',
    params=params  # Blir: /users?limit=10&sort=name&filter=active
)
```

### Felhantering:
```python
import requests
from requests.exceptions import RequestException, Timeout

try:
    response = requests.get(
        'https://api.example.com/data',
        timeout=5  # Max 5 sekunder
    )
    response.raise_for_status()  # Kastar exception vid HTTP-fel
    data = response.json()
    print("Data hämtad framgångsrikt")
    
except Timeout:
    print("Request tog för lång tid")
except requests.exceptions.HTTPError as e:
    print(f"HTTP-fel: {e}")
except requests.exceptions.RequestException as e:
    print(f"Något gick fel: {e}")
```

---

## Bygga APIs: Flask Framework

**Flask** är ett Python-ramverk för att bygga webbapplikationer och APIs.

### Installation:
```bash
pip install flask
```

### Ditt första API:
```python
# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

# Exempel-data (i verkliga applikationer skulle detta vara en databas)
users = [
    {"id": 1, "name": "Anna", "email": "anna@example.com"},
    {"id": 2, "name": "Björn", "email": "bjorn@example.com"}
]

# GET /users - Hämta alla användare
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET /users/<id> - Hämta specifik användare
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Användare hittades inte"}), 404

# POST /users - Skapa ny användare
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Enkel validering
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name och email krävs"}), 400
    
    # Skapa ny användare
    new_user = {
        "id": len(users) + 1,
        "name": data['name'],
        "email": data['email']
    }
    users.append(new_user)
    
    return jsonify(new_user), 201

# PUT /users/<id> - Uppdatera användare
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "Användare hittades inte"}), 404
    
    data = request.get_json()
    user['name'] = data.get('name', user['name'])
    user['email'] = data.get('email', user['email'])
    
    return jsonify(user)

# DELETE /users/<id> - Ta bort användare
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u['id'] != user_id]
    return '', 204  # No Content

if __name__ == '__main__':
    app.run(debug=True)  # Kör på http://localhost:5000
```

### Kör API:et:
```bash
python app.py
```

### Testa API:et:
```bash
# Hämta alla användare
curl http://localhost:5000/users

# Skapa ny användare
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Clara", "email": "clara@example.com"}'

# Hämta specifik användare
curl http://localhost:5000/users/1
```

---

## API Design Best Practices

### 1. **Konsistent URL-struktur**
```python
# BRA
GET    /api/v1/users          # Lista användare
GET    /api/v1/users/123      # Hämta användare
POST   /api/v1/users          # Skapa användare
PUT    /api/v1/users/123      # Uppdatera användare
DELETE /api/v1/users/123      # Ta bort användare

# DÅLIGT
GET /getAllUsers
GET /getUserById?id=123
POST /createNewUser
```

### 2. **Korrekt HTTP-statuskoder**
```python
from flask import Flask, jsonify

@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Validering
        if not valid_data:
            return jsonify({"error": "Invalid data"}), 400
        
        # Skapa användare
        user = create_user(data)
        return jsonify(user), 201  # Created
        
    except Exception as e:
        return jsonify({"error": "Server error"}), 500
```

### 3. **API-versioning**
```python
# Genom URL
@app.route('/api/v1/users')
@app.route('/api/v2/users')

# Genom headers
@app.route('/users')
def get_users():
    version = request.headers.get('API-Version', 'v1')
    if version == 'v2':
        return new_format()
    else:
        return old_format()
```

### 4. **Paginering för stora dataset**
```python
@app.route('/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    users_page = users[start:end]
    
    return jsonify({
        "users": users_page,
        "page": page,
        "per_page": per_page,
        "total": len(users),
        "pages": (len(users) + per_page - 1) // per_page
    })
```

---

## Testa APIs

### Enhetstest med pytest:
```python
# test_api.py
import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_user(client):
    new_user = {"name": "Test User", "email": "test@example.com"}
    response = client.post('/users', 
                          data=json.dumps(new_user),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == "Test User"

def test_get_nonexistent_user(client):
    response = client.get('/users/999')
    assert response.status_code == 404
```

### Integration testing med requests:
```python
import requests
import pytest

BASE_URL = "http://localhost:5000"

def test_full_user_lifecycle():
    # Skapa användare
    new_user = {"name": "Integration Test", "email": "test@test.com"}
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201
    user = response.json()
    user_id = user['id']
    
    # Hämta användaren
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()['name'] == "Integration Test"
    
    # Ta bort användaren
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 204
```

---


### 2. **Data Collection API:**
```python
from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Enkel databas setup
def init_db():
    conn = sqlite3.connect('data.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            sensor_id TEXT NOT NULL,
            value REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.close()

@app.route('/sensors/<sensor_id>/data', methods=['POST'])
def collect_sensor_data(sensor_id):
    """Samla in data från sensorer"""
    data = request.get_json()
    
    if 'value' not in data:
        return jsonify({"error": "Value required"}), 400
    
    # Spara till databas
    conn = sqlite3.connect('data.db')
    conn.execute(
        'INSERT INTO sensor_data (sensor_id, value, timestamp) VALUES (?, ?, ?)',
        (sensor_id, data['value'], datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "Data saved"}), 201

@app.route('/sensors/<sensor_id>/data', methods=['GET'])
def get_sensor_data(sensor_id):
    """Hämta sensor-data för analys"""
    limit = request.args.get('limit', 100, type=int)
    
    conn = sqlite3.connect('data.db')
    cursor = conn.execute(
        'SELECT value, timestamp FROM sensor_data WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT ?',
        (sensor_id, limit)
    )
    
    data = [{"value": row[0], "timestamp": row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

---

## REST vs Flask: Vad är skillnaden?

### **REST:**
- **Designprinciper** för hur APIs ska byggas
- **Arkitekturstil** - regler för URL:er, HTTP-metoder, statuskoder
- **Språkoberoende** - kan implementeras i Python, Java, JavaScript, etc.

### **Flask:**
- **Python-ramverk** för att bygga webbapplikationer och APIs
- **Verktyg** för att implementera REST-principer
- **Ett sätt** att skapa REST APIs (andra alternativ: Django REST, FastAPI)

**Analogi:**
- **REST** = Regler för hur man bygger hus (arkitektoniska principer)
- **Flask** = Hammare och såg (verktyg för att bygga huset)

### Andra Python API-ramverk:
```python
# Flask - Enkelt och flexibelt
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# FastAPI - Modern, snabb, automatisk dokumentation
@app.get("/users")
def get_users():
    return users

# Django REST Framework - Kraftfullt, många funktioner
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

---

## Sammanfattning

**APIs är fundamentala för modern datahantering:**

### **Vad du lärt dig:**
- ✅ **JSON** - dataformat för API-kommunikation
- ✅ **REST** - designprinciper för bra APIs
- ✅ **Requests** - hur man använder andra APIs
- ✅ **Flask** - hur man bygger egna APIs
- ✅ **Testing** - kvalitetssäkra dina APIs

### **Nästa steg:**
- Experimentera med publika APIs (väder, nyheter, social media)
- Bygg dina egna APIs för datainsamling
- Integrera APIs med dina CI/CD-pipelines
- Lär dig om API-säkerhet och autentisering

**Remember:** APIs är byggblocken för moderna datasystem. Behärska dem så kan du integrera vilka system som helst! 🚀
