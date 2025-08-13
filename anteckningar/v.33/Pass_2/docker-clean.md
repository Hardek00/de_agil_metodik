# Docker: Containerisering för Utvecklare

## Vad är Docker?

Docker är ett verktyg för **containerisering** - att packa din applikation med alla beroenden i en portabel "låda" som fungerar identiskt överallt.

**Kärnproblemet Docker löser:**
```
Utvecklare: "Det fungerar på min maskin!"
Produktion: *Kraschar*
Docker: "Samma container överallt = samma beteende"
```

## Grundkoncept

### 📦 De tre byggstenarna
1. **Dockerfile** → Blueprint/recept för att bygga en image
2. **Image** → Färdig mall/snapshot (oföränderlig)
3. **Container** → Körande process baserad på en image

### 🔄 Arbetsflödet
```
Dockerfile → build → Image → run → Container
    ↑              ↑           ↑         ↑
  Skriva kod   Skapa mall  Starta app  Körande app
```

---

## Dockerfile: Din första container

### Grundläggande struktur
```dockerfile
# 1. Välj basimage
FROM python:3.10-slim

# 2. Sätt arbetskatalog
WORKDIR /app

# 3. Kopiera requirements och installera
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Kopiera din kod
COPY . .

# 5. Dokumentera port
EXPOSE 5000

# 6. Säg hur appen startas
CMD ["python", "main.py"]
```

## 📁 WORKDIR 

### Vad är WORKDIR?
**WORKDIR** sätter vilken mapp alla kommanden körs från inuti containern - som `cd` i terminalen.

```dockerfile
WORKDIR /app
# Från nu körs alla kommandon från /app-mappen
# Som att göra: cd /app
```

### Kan den heta vad som helst? JA!
```dockerfile
# Alla dessa fungerar:
WORKDIR /app                    # Vanligast
WORKDIR /usr/src/app           # Mer "Unix-standard"
WORKDIR /home/appuser/myapp    # Med användare
WORKDIR /code                  # Kort och enkelt
WORKDIR /backend               # Beskrivande
WORKDIR /workspace             # IDE-liknande
WORKDIR /opt/mycompany/app     # Företagsstandard
```


### Projektstruktur-exempel

**Scenario: Dockerfile i kod/backend/**
```
mitt-projekt/
├── frontend/
│   └── src/...
└── kod/
    └── backend/          ← Du står här
        ├── Dockerfile    ← Dockerfile finns här
        ├── main.py
        └── requirements.txt
```

**Din Dockerfile (i kod/backend/):**
```dockerfile
FROM python:3.10-slim
WORKDIR /app              # ← Kan fortfarande heta /app!
COPY requirements.txt .   # Kopiera från kod/backend/ till /app/
COPY . .                  # Kopiera allt från kod/backend/ till /app/
CMD ["python", "main.py"] # Kör /app/main.py
```

**Bygga från kod/backend/:**
```bash
cd kod/backend
docker build -t backend-app .  # Dockerfile i current dir
```

**Eller från projektrot:**
```bash
# Från mitt-projekt/
docker build -t backend-app -f kod/backend/Dockerfile kod/backend/
#                             ↑ Dockerfile path    ↑ Build context
```

### De viktigaste instruktionerna

| Instruktion | Syfte | Exempel |
|-------------|-------|---------|
| `FROM` | Basimage att utgå från | `FROM python:3.10-slim` |
| `WORKDIR` | Sätt arbetskatalog | `WORKDIR /app` |
| `COPY` | Kopiera filer från host till container | `COPY . .` |
| `RUN` | Kör kommando under byggfasen | `RUN pip install -r requirements.txt` |
| `EXPOSE` | Dokumentera vilken port appen lyssnar på | `EXPOSE 5000` |
| `CMD` | Kommando som körs när containern startar | `CMD ["python", "main.py"]` |

## 🔌 Portar i CMD vs app-kod vs docker run

### Varför finns portar på tre ställen?

**1. I din app-kod (Python/Flask):**
```python
app.run(host='0.0.0.0', port=5000)  # Appen lyssnar på port 5000
```

**2. I CMD (ibland):**
```dockerfile
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
```

**3. I docker run:**
```bash
docker run -p 8080:5000 my-app  # Map host:8080 → container:5000
```

### När används portar i CMD?

#### **Scenario 1: Framework utan konfiguration**
```dockerfile
# Vissa frameworks läser port från argument
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["node", "server.js", "--port=3000"]
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
```

#### **Scenario 2: Environment variables**
```dockerfile
# Appen läser från miljövariabel
ENV PORT=5000
CMD ["python", "main.py"]  # main.py läser os.environ['PORT']
```

#### **Scenario 3: Docker-compose miljöer**
```yaml
# docker-compose.yml
services:
  web:
    build: .
    environment:
      - PORT=5000
    ports:
      - "8080:5000"
```

### Tre sätt att hantera portar

#### **Metod 1: Hårdkodad i app (enklast)**
```python
# main.py
app.run(host='0.0.0.0', port=5000)  # Alltid port 5000
```

```dockerfile
# Dockerfile  
EXPOSE 5000
CMD ["python", "main.py"]  # Ingen port-config
```

```bash
# Docker run
docker run -p 8080:5000 my-app  # Map till host:8080
```

#### **Metod 2: Environment variable (flexibel)**
```python
# main.py
import os
port = int(os.environ.get('PORT', 5000))  # Default 5000
app.run(host='0.0.0.0', port=port)
```

```dockerfile
# Dockerfile
ENV PORT=5000
EXPOSE 5000  
CMD ["python", "main.py"]
```

```bash
# Docker run - ändra port runtime
docker run -p 8080:3000 -e PORT=3000 my-app
```

#### **Metod 3: CMD argument (framework-specific)**
```dockerfile
# För vissa verktyg (uvicorn, gunicorn, etc.)
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=5000"]
```

### Vanliga framework-exempel

#### **Flask med flask run:**
```dockerfile
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
# Varför? Flask run kommandot behöver explicit port
```

#### **FastAPI med uvicorn:**
```dockerfile  
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
# Varför? Uvicorn är separat server som behöver konfiguration
```

#### **Express.js:**
```dockerfile
CMD ["node", "server.js"]  # Inget port-argument
# Varför? server.js hanterar port internt
```

### Best Practice-rekommendation

**För enkla appar (Flask, Express):**
```python
# Hårdkoda i app-kod
app.run(host='0.0.0.0', port=5000)
```

```dockerfile
# Minimal Dockerfile
EXPOSE 5000
CMD ["python", "main.py"]
```

**För produktions-appar:**
```python
# Använd environment variables
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

```dockerfile
# Flexibel konfiguration
ENV PORT=5000
EXPOSE $PORT
CMD ["python", "main.py"]
```

---

## Bygga och köra containers

### Bygga en image
```bash
# Bygg image från Dockerfile
docker build -t min-app:1.0 .

# Förklaring:
# -t min-app:1.0  = ge imagen namn "min-app" och tag "1.0" 
# .               = använd Dockerfile i nuvarande mapp
```

### Köra en container
```bash
# Grundläggande körning
docker run min-app:1.0

# Med port-mapping (vanligast)
docker run -p 5000:5000 min-app:1.0

# I bakgrunden med namn
docker run -d --name my-container -p 5000:5000 min-app:1.0
```

### Viktiga flaggor för `docker run`

| Flagga | Syfte | Exempel |
|--------|-------|---------|
| `-p host:container` | Koppla portar | `-p 5000:5000` |
| `-d` | Kör i bakgrunden | `-d` |
| `--name` | Ge containern ett namn | `--name my-app` |
| `-it` | Interaktiv terminal | `-it` |
| `--rm` | Ta bort container vid stopp | `--rm` |

---

## Praktiskt exempel: Flask-app

### 1. Skapa filstruktur
```
my-flask-app/
├── main.py
├── requirements.txt
└── Dockerfile
```

### 2. main.py
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 3. requirements.txt
```
Flask==2.3.2
```

### 4. Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
```

### 5. Bygga och köra
```bash
# Bygg
docker build -t flask-app .

# Kör
docker run -p 5000:5000 flask-app

# Testa: öppna http://localhost:5000
```

---

## Docker Compose: Flera containers tillsammans

När din app behöver flera tjänster (databas, cache, etc.) använder du Docker Compose.

### docker-compose.yml exempel
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    depends_on:
      - database

  database:
    image: postgres:13
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

### Compose-kommandon
```bash
# Starta alla tjänster
docker-compose up

# I bakgrunden
docker-compose up -d

# Bygga om och starta
docker-compose up --build

# Stoppa allt
docker-compose down

# Se status
docker-compose ps
```

---

## Användbara Docker-kommandon

### Information och debugging
```bash
# Lista images
docker images

# Lista körande containers
docker ps

# Lista alla containers (även stoppade)
docker ps -a

# Se loggar från container
docker logs <container-name>

# Gå in i körande container
docker exec -it <container-name> bash
```

### Rensning
```bash
# Stoppa container
docker stop <container-name>

# Ta bort container
docker rm <container-name>

# Ta bort image
docker rmi <image-name>

# Rensa allt (stoppade containers, oanvända images, etc.)
docker system prune
```

---

## Best Practices

### 1. Cache-optimerad Dockerfile
```dockerfile
# BRA: Kopiera requirements först
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# DÅLIGT: Kopiera allt först
COPY . .
RUN pip install -r requirements.txt
```

**Varför?** Docker cachear varje steg. Om du bara ändrar kod (inte requirements) behöver pip inte köras igen.

### 2. Använd .dockerignore
```
node_modules
.git
.env
*.pyc
__pycache__
.vscode
```

### 3. Säkra images
```dockerfile
# Använd specifika versioner
FROM python:3.10-slim

# Inte bara "latest"
# FROM python:latest  ← Undvik detta
```

### 4. Små images
```dockerfile
# Föredra slim/alpine-versioner
FROM python:3.10-slim     # ✅ Mindre
FROM python:3.10-alpine   # ✅ Ännu mindre

# Istället för full versions
FROM python:3.10          # ❌ Större
```

---

## Vanliga misstag och lösningar

### Problem: "Port already in use"
```bash
# Hitta vad som använder porten
sudo lsof -i :5000

# Eller använd annan port
docker run -p 5001:5000 min-app
```

### Problem: "No such file or directory"
```dockerfile
# Se till att filer finns och COPY är korrekt
COPY requirements.txt .  # ✅ Fil måste finnas
COPY . .                 # ✅ Kopierar allt
```

### Problem: Slow builds
```dockerfile
# Optimera för cache
COPY requirements.txt .     # ✅ Ändras sällan först
RUN pip install -r requirements.txt
COPY . .                    # ✅ Ändras ofta sist
```

---

## Sammanfattning

### Grundflöde
1. **Skriv Dockerfile** med FROM, WORKDIR, COPY, RUN, CMD
2. **Bygg image**: `docker build -t app-name .`
3. **Kör container**: `docker run -p 5000:5000 app-name`
4. **Använd Compose** för flera tjänster

### Nyckelkoncept
- **Dockerfile** = Recept för att skapa image
- **Image** = Oföränderlig mall/snapshot
- **Container** = Körande process från image
- **Port mapping** = Koppla host-port till container-port
- **Volume** = Dela data mellan host och container

### Varför Docker?
- ✅ **Konsistens**: Samma miljö överallt
- ✅ **Portabilitet**: Fungerar på alla system
- ✅ **Isolation**: Inga konflikter mellan projekt
- ✅ **Skalbarhet**: Enkelt att duplicera och skala

Nu kan du containerisera dina applikationer! 🐳

---

## Djupare fördjupning

### 🏔️ Alpine vs andra basimages: Varför inte alltid Alpine?

**Kort svar:** Alpine är liten men kan orsaka problem. Använd `-slim` för learning/development.

#### Storleksjämförelse
| Image | Storlek | Vad som ingår |
|-------|---------|---------------|
| `python:3.10` | ~900MB | Debian + Python + många verktyg |
| `python:3.10-slim` | ~120MB | Debian minimal + Python |
| `python:3.10-alpine` | ~45MB | Alpine Linux + Python |

#### ❌ Problem med Alpine
1. **C library-konflikt:** numpy, pandas måste byggas från source (långsamt)
2. **Saknar verktyg:** Ingen curl, bash, gcc som standard
3. **Säkerhet:** Mindre team, långsammare uppdateringar

#### ✅ När Alpine är bra
- Enkla appar utan C-dependencies
- Microservices där storlek spelar roll
- Embedded/IoT-system

#### 🎯 Rekommendation
| Use Case | Använd |
|----------|--------|
| **Learning/Development** | `python:3.10-slim` |
| **Data Science** | `python:3.10-slim` |
| **Produktion (vanligt)** | `python:3.10-slim` |
| **Microservices (storlek kritiskt)** | `python:3.10-alpine` |

**Bottom line:** Börja med `-slim`, byt till Alpine endast om du har specifika skäl!
