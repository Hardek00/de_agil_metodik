# Docker Compose Demonstration - Två Kommunicerande Containers

Detta är en pedagogisk demonstration som visar hur två Docker containers kan kommunicera med varandra via Docker Compose.

## 🏗️ Arkitektur

```
┌─────────────────┐    HTTP requests    ┌─────────────────┐
│   Container 2   │ ─────────────────► │   Container 1   │
│ Word Processor  │                    │   Word API      │
│   (Client)      │ ◄───────────────── │   (Server)      │
└─────────────────┘    JSON responses   └─────────────────┘
```

### Container 1: Word Storage API (Flask)
- **Port**: 5000
- **Funktion**: Tar emot ord via POST, lagrar dem och returnerar statistik
- **Endpoints**:
  - `POST /words` - Lägg till ord
  - `GET /words` - Hämta alla ord
  - `GET /stats` - Få statistik om orden
  - `GET /health` - Hälsokontroll

### Container 2: Word Processor (Python Client)
- **Funktion**: Skickar en lista med ord till API:et och visar statistik i realtid
- **Beteende**: Väntar på att API:et startar, skickar ord ett i taget, visar statistik

## 🚀 Hur man kör demonstrationen

### 1. Bygg och starta containers
```bash
docker-compose up --build
```

### 2. Vad händer?
1. **Container 1** (API) startar först
2. **Container 2** (Client) väntar tills API:et är redo
3. Klienten skickar ord ett i taget till API:et
4. Efter varje ord visas uppdaterad statistik
5. Till slut visas en sammanfattning

### 3. Manuell testning (valfritt)
Medan containers kör kan du också testa API:et manuellt:

```bash
# Lägg till ett ord
curl -X POST http://localhost:5000/words \
  -H "Content-Type: application/json" \
  -d '{"word": "test"}'

# Hämta statistik
curl http://localhost:5000/stats
```

### 4. Stoppa containers
```bash
docker-compose down
```

## 📁 Filstruktur

```
docker_compose_2/
├── docker-compose.yml          # Orkestrering av containers
├── README.md                   # Denna fil
├── container_1/                # Flask API
│   ├── app_1.py               # API-kod
│   └── dockerfile             # Dockerfile för API
└── container_2/                # Python client
    ├── app_2.py               # Klient-kod
    └── dockerfile             # Dockerfile för klient
```

## 🎯 Pedagogiska poänger

1. **Två separata Dockerfiles**: Varje container har sin egen Dockerfile
2. **Container-kommunikation**: Containers pratar via HTTP över Docker-nätverk
3. **Service dependencies**: Container 2 väntar på att Container 1 ska bli redo
4. **Nätverkshantering**: Docker Compose skapar automatiskt ett nätverk
5. **Health checks**: API:et kontrolleras innan klienten startar
6. **Realtidsdata**: Data skickas och bearbetas live mellan containers

## 🔧 Tekniska detaljer

- **Nätverk**: Containers kommunicerar via Docker-nätverket `word-network`
- **Service discovery**: Container 2 hittar Container 1 via service-namnet `word-api`
- **Port mapping**: API:et är tillgängligt på `localhost:5000` utanför Docker
- **Dependencies**: `depends_on` säkerställer rätt startordning
- **Health checks**: Förhindrar att klienten startar innan API:et är redo

---

*Detta är en minimal demonstration för att visa grundläggande Docker Compose-koncept!*
