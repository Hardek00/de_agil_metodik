# Docker Compose Demo: Flask + PostgreSQL

## 📁 Filstruktur
```
docker_compose/
├── app.py                 # Enkel Flask-app (40 rader)
├── init.sql              # Databas-setup med exempeldata
├── templates/
│   └── index.html        # HTML-sida som visar användare
├── requirements.txt      # Flask + psycopg2
├── Dockerfile           # Container för web-appen
└── docker-compose.yml   # Två services: web + database
```

## 🚀 Snabbstart

### 1. Starta allt
```bash
docker-compose up --build
```

### 2. Öppna webbläsaren
Gå till: **http://localhost:5000**

Du ser en HTML-sida med:
- Lista över användare från databasen  
- Status om databasanslutning fungerar

### 3. Stoppa allt
```bash
docker-compose down
```

## 🔍 Vad som händer

### Två containers körs samtidigt:
1. **web-container** → Byggs från vår `Dockerfile` (Flask-app)
2. **database-container** → Använder färdig `postgres:15` image

### Services i docker-compose.yml:
- **web** → Bygger Flask-app från vår kod (`build: .`)
- **database** → Använder PostgreSQL från Docker Hub (`image: postgres:15`)

### Automatiskt:
1. PostgreSQL-container startar från färdig image
2. `init.sql` körs → skapar tabell + lägger in data  
3. Flask-container byggs från vår Dockerfile
4. Flask-app ansluter till databas via container-namn `database`
5. HTML-sida visar användare från databasen

### Varför två containers?
- **Separation of concerns:** Webb-app och databas är olika tjänster
- **Skalbarhet:** Kan köra flera web-containers mot samma databas
- **Utveckling:** Kan starta om web utan att förlora databas-data
- **Produktion:** Databas kan köras på separat server

## 🎯 Lärande-fokus

### Docker Compose-grunder:
- **Services:** Flera containers tillsammans
- **depends_on:** Web väntar på databas
- **Volumes:** `init.sql` mountas för databas-setup
- **Networks:** Containers pratar via namn (`database`)

### Enkelt men komplett exempel:
- Frontend (HTML)
- Backend (Flask)  
- Database (PostgreSQL)
- Allt i 40 rader Python-kod!

## 📋 Användbara kommandon

```bash
# Se vad som körs
docker-compose ps

# Se loggar
docker-compose logs web
docker-compose logs database

# Starta i bakgrunden
docker-compose up -d

# Gå in i databasen
docker-compose exec database psql -U postgres -d webapp
```

## 🤔 Vanliga frågor

### "Vi har ju en Dockerfile - varför kör vi flera containers?"

Ja, vi har en `Dockerfile` för vår Flask-app, men Docker Compose startar **två separata containers**:

```bash
# Detta sker när du kör docker-compose up:

# 1. Bygg web-container från vår Dockerfile
docker build -t docker_compose_web .

# 2. Starta PostgreSQL-container
docker run postgres:15

# 3. Koppla ihop dem i ett nätverk
# 4. Flask kan prata med PostgreSQL via namn "database"
```

### "Kan jag inte bara köra allt i en container?"

Jo, men det är **dåligt mönster**:

❌ **En stor container:**
```dockerfile
FROM python:3.10-slim
RUN apt-get install postgresql  # ❌ Blanda olika tjänster
COPY . .
CMD ["start_both_app_and_db.sh"]  # ❌ Flera processer
```

✅ **Flera små containers (microservices):**
```yaml
services:
  web:    # ✅ Bara Flask
  database:  # ✅ Bara PostgreSQL
```

### **Fördelar med flera containers:**
- **Specialisering:** Varje container gör EN sak bra
- **Återanvändning:** Samma databas för flera appar
- **Skalning:** Lägg till fler web-containers vid behov
- **Underhåll:** Uppdatera app utan att röra databasen

## 💡 Experimentera!

1. **Ändra init.sql** → Lägg till fler användare
2. **Ändra HTML** → Gör sidan snyggare  
3. **Lägg till fler tabeller** → Produkter, beställningar
4. **Lägg till en form** → Skapa nya användare via webb
5. **Testa skalning** → Kör flera web-containers:
   ```bash
   docker-compose up --scale web=3
   ```
