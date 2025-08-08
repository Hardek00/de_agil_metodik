# Docker - Grundläggande Guide

## 🐳 Vad är Docker?

Docker låter dig **packa** din applikation med alla dess beroenden i en **container** som kan köras överallt på samma sätt.

```
Din App + Dependencies + OS = Container Image
Container Image → Kör → Running Container
```

## 📋 Dockerfile - Instruktioner för att Bygga Images

En **Dockerfile** är en textfil med instruktioner för hur Docker ska bygga din image.

### 📝 Grundläggande Syntax:

```dockerfile
# Kommentar börjar med #
INSTRUKTION argument
INSTRUKTION argument1 argument2
```

### 🏗️ Vanliga Instruktioner:

#### **FROM** - Basimage
```dockerfile
FROM python:3.10-slim
# Utgå från en existing image (här: Python 3.10 på Ubuntu slim)
```

#### **WORKDIR** - Sätt arbetskatalog
```dockerfile
WORKDIR /app
# Alla kommanden efter detta körs i /app-mappen
# Som att göra 'cd /app'
```

#### **COPY** - Kopiera filer
```dockerfile
COPY . .
# COPY <från host> <till container>
# COPY . . = kopiera allt från current directory (.) till current workdir (.)

COPY requirements.txt .
# Kopiera bara requirements.txt till current workdir

COPY src/ /app/src/
# Kopiera src-mappen till /app/src/ i containern
```

#### **RUN** - Kör kommando under bygget
```dockerfile
RUN pip install -r requirements.txt
# Installerar Python packages när imagen byggs
# Kör BARA under byggprocessen, inte när containern startar
```

#### **EXPOSE** - Dokumentera portar
```dockerfile
EXPOSE 5000
# Säger att appen lyssnar på port 5000
# Bara dokumentation - öppnar INTE porten automatiskt
```

#### **CMD** - Standard kommando
```dockerfile
CMD ["python", "main.py"]
# Vad som ska köras när containern startar
# Kan overridas när du kör 'docker run'
```

### 📂 Vad betyder "." och ".."?

```bash
.     # Current directory (där du står nu)
..    # Parent directory (en nivå upp)
./    # Samma som . men tydligare
../   # Samma som .. men tydligare

# Exempel:
COPY . .
# Från: current directory på host
# Till: current workdir i container

COPY ../data .
# Från: en nivå upp på host
# Till: current workdir i container
```

### 🔄 Komplett Exempel:

```dockerfile
# Steg 1: Välj basimage
FROM python:3.10-slim

# Steg 2: Sätt arbetskatalog
WORKDIR /app

# Steg 3: Kopiera requirements först (för caching)
COPY requirements.txt .

# Steg 4: Installera dependencies
RUN pip install -r requirements.txt

# Steg 5: Kopiera resten av koden
COPY . .

# Steg 6: Dokumentera vilken port appen använder
EXPOSE 5000

# Steg 7: Säg vad som ska köras när containern startar
CMD ["python", "main.py"]
```

## 🏃 Docker Kommandon

### **docker build** - Bygg Image

```bash
# Grundläggande syntax
docker build [OPTIONS] PATH

# Exempel:
docker build -t min-app:1.0 .
```

#### **Flaggor för build:**

```bash
-t name:tag     # Tagga imagen med namn och version
                # -t min-app:1.0 = namn "min-app", version "1.0"

.               # PATH = current directory
                # Här hittar Docker din Dockerfile

-f filename     # Använd annan Dockerfile
                # -f Dockerfile.prod

--no-cache      # Bygg utan att använda cache
```

**Vad händer under build:**
1. Docker läser Dockerfile
2. Kör varje instruktion i ordning
3. Skapar layers för varje steg
4. Skapar en final image

### **docker run** - Kör Container

```bash
# Grundläggande syntax
docker run [OPTIONS] IMAGE [COMMAND]

# Exempel:
docker run -p 5000:5000 min-app:1.0
```

#### **Flaggor för run:**

```bash
-p host:container   # Port mapping
                    # -p 5000:5000 = host port 5000 → container port 5000
                    # -p 8080:5000 = host port 8080 → container port 5000

-d                  # Detached mode (kör i bakgrunden)
                    # Utan -d = ser output i terminalen

-it                 # Interactive + TTY
                    # För att kunna interagera med containern

--name mycontainer  # Ge containern ett namn
                    # Annars får den ett random namn

-v host:container   # Volume mapping (dela filer)
                    # -v /local/path:/container/path

-e VAR=value        # Sätt environment variables
                    # -e DEBUG=true

--rm                # Ta bort containern när den stoppas
```

### **Skillnad: BUILD vs RUN**

```bash
# BUILD = Skapa image från Dockerfile
docker build -t min-app:1.0 .
# Resultat: En image sparad lokalt

# RUN = Starta container från image
docker run -p 5000:5000 min-app:1.0
# Resultat: En körande container
```

**Analogi:**
- **BUILD** = Baka en kaka från recept
- **RUN** = Äta kakan

## 🐙 Docker Compose - Flera Containers

Docker Compose låter dig definiera och köra **flera containers** tillsammans.

### 📝 docker-compose.yml Syntax:

```yaml
version: '3.8'

services:              # Lista av containers
  web:                 # Service namn
    build: .           # Bygg från Dockerfile i current dir
    ports:
      - "5000:5000"    # Port mapping
    environment:
      - DEBUG=true     # Environment variables
    volumes:
      - .:/app         # Volume mapping
    depends_on:
      - database       # Vänta på database service

  database:
    image: postgres:13 # Använd existing image
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:               # Definiera volumes
  db_data:
```

### 🔧 Docker Compose Kommandon:

```bash
# Bygg och starta alla services
docker-compose up

# Starta i bakgrunden
docker-compose up -d

# Bygg om innan start
docker-compose up --build

# Stoppa alla services
docker-compose down

# Visa status
docker-compose ps

# Visa logs
docker-compose logs web
```

## 🎯 Praktiska Exempel

### 1. Enkel Python App

**Dockerfile:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

**Kommandon:**
```bash
# Bygg
docker build -t my-python-app .

# Kör
docker run -p 5000:5000 my-python-app
```

### 2. Med Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
```

**Kommandon:**
```bash
# Allt i ett kommando
docker-compose up --build
```

## 🔍 Felsökning

### Vanliga Kommandon:

```bash
# Lista alla images
docker images

# Lista körande containers
docker ps

# Lista alla containers (även stoppade)
docker ps -a

# Gå in i en körande container
docker exec -it <container_name> bash

# Se logs från container
docker logs <container_name>

# Stoppa container
docker stop <container_name>

# Ta bort container
docker rm <container_name>

# Ta bort image
docker rmi <image_name>
```

## 🤔 Djupare Förklaringar

### **🗃️ Vad är Cache?**

Docker **cachear** (sparar) varje steg i Dockerfile för att bygga snabbare nästa gång.

```dockerfile
FROM python:3.10-slim        # Layer 1 - cachas
WORKDIR /app                 # Layer 2 - cachas  
COPY requirements.txt .      # Layer 3 - cachas om requirements.txt inte ändrats
RUN pip install -r requirements.txt  # Layer 4 - hoppar över om Layer 3 cachad
COPY . .                     # Layer 5 - byggs om om någon fil ändrats
```

**Varför cache är bra:**
```bash
# Första bygget: 3 minuter
docker build -t min-app .

# Andra bygget (ingen kod ändrad): 5 sekunder
docker build -t min-app .

# Tredje bygget (bara main.py ändrad): 30 sekunder
# Bara Layer 5 byggs om, pip install hoppas över
```

**Varför --no-cache:**
```bash
# Problem: Cache kan bli korrupt eller föråldrad
docker build --no-cache -t min-app .
# Bygger ALLT från scratch, ignorerar all cache
```

### **📁 Working Directory (WORKDIR)**

WORKDIR är som att göra `cd` i containern:

```dockerfile
# Utan WORKDIR
COPY requirements.txt /usr/app/requirements.txt
RUN cd /usr/app && pip install -r requirements.txt
COPY . /usr/app/
CMD ["python", "/usr/app/main.py"]

# Med WORKDIR (mycket cleanare!)
WORKDIR /usr/app
COPY requirements.txt .          # Hamnar i /usr/app/
RUN pip install -r requirements.txt  # Kör från /usr/app/
COPY . .                         # Hamnar i /usr/app/
CMD ["python", "main.py"]       # Kör från /usr/app/
```

**Vad händer:**
```bash
WORKDIR /app     # Sätter current directory till /app
                 # Alla kommanden efter detta körs "från /app"
```

### **📋 COPY utan "." - Vart hamnar filerna?**

```dockerfile
# MED punkt (rekommenderat)
WORKDIR /app
COPY requirements.txt .     # → /app/requirements.txt

# UTAN punkt (absolut path)
COPY requirements.txt /tmp/requirements.txt  # → /tmp/requirements.txt
COPY requirements.txt requirements.txt       # → /requirements.txt (root!)

# Vad händer utan WORKDIR och utan punkt?
COPY requirements.txt requirements.txt  # → /requirements.txt (i root!)
```

**Dåligt exempel:**
```dockerfile
FROM python:3.10-slim
# Ingen WORKDIR satt
COPY requirements.txt requirements.txt  # Hamnar i / (root directory)
RUN pip install -r requirements.txt     # Kör från /
COPY . .                                # Dumpar ALLT i / (root directory)
```

**Bättre:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app                            # Sätt working directory
COPY requirements.txt .                 # → /app/requirements.txt
RUN pip install -r requirements.txt    # Kör från /app/
COPY . .                               # → /app/
```

### **🖼️ Basimage - Vad är det?**

En **basimage** är en färdig image som du bygger vidare på:

```dockerfile
FROM python:3.10-slim
# Du får:
# - Ubuntu Linux
# - Python 3.10 installerat
# - pip installerat
# - Grundläggande system-verktyg
```

**Vanliga baseimages:**
```dockerfile
FROM python:3.10-slim          # Python + minimal Linux
FROM node:18-alpine            # Node.js + Alpine Linux (mycket liten)
FROM ubuntu:22.04              # Bara Ubuntu (du installerar själv)
FROM nginx:alpine              # Nginx webserver + Alpine
FROM postgres:15               # PostgreSQL databas
FROM scratch                   # TOM image (bara din app)
```

**Varför inte bara scratch?**
```dockerfile
FROM scratch
COPY main.py .
CMD ["python", "main.py"]      # FEJL! Ingen Python installerad!
```

### **🚪 EXPOSE - Vilka portar som helst?**

**JA, du kan exponera vilka portar som helst:**

```dockerfile
EXPOSE 80          # Web traffic
EXPOSE 443         # HTTPS
EXPOSE 3000        # Node.js default
EXPOSE 5432        # PostgreSQL
EXPOSE 8080        # Tomcat/alternativ web
EXPOSE 22          # SSH
EXPOSE 9999        # Din egen port
```

**MEN: EXPOSE gör INGENTING!**
```dockerfile
EXPOSE 5000        # Bara dokumentation
                   # Öppnar INTE porten automatiskt
```

För att faktiskt komma åt porten:
```bash
docker run -p 5000:5000 min-app    # Nu kan du nå localhost:5000
docker run -p 8080:5000 min-app    # Nu kan du nå localhost:8080
```

**Flera portar:**
```dockerfile
EXPOSE 5000        # API
EXPOSE 8080        # Admin interface
EXPOSE 9090        # Metrics
```

```bash
docker run -p 5000:5000 -p 8080:8080 -p 9090:9090 min-app
```

### **⚙️ CMD - Vad kan stå där?**

CMD kan vara **vilken körbar kommando som helst:**

```dockerfile
# Python apps
CMD ["python", "main.py"]
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

# Node.js apps
CMD ["node", "server.js"]
CMD ["npm", "start"]

# Bash script
CMD ["bash", "start.sh"]
CMD ["./run.sh"]

# Direkt binärer
CMD ["nginx", "-g", "daemon off;"]

# Med portar (som du såg)
CMD ["python", "-m", "http.server", "8000"]
        # Startar Python's inbyggda webserver på port 8000

# Flera kommandon
CMD ["sh", "-c", "python migrate.py && python main.py"]
```

**Array vs String format:**
```dockerfile
# FÖREDRA: Array format (exec form)
CMD ["python", "main.py"]

# UNDVIK: String format (shell form)
CMD python main.py
```

**Varför array är bättre:**
- **Exec form** → Direktstart, inga extra processer
- **Shell form** → Startar via shell, extra process

### **🔌 Portar i CMD - Varför?**

```dockerfile
# Flask example
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
#                                                        ↑ Säger åt Flask vilken port

# Python HTTP server
CMD ["python", "-m", "http.server", "8000"]
#                                    ↑ Säger åt servern vilken port

# Node.js med port från environment
CMD ["node", "server.js"]  # server.js läser process.env.PORT
```

**Skillnad mellan EXPOSE och CMD port:**
```dockerfile
EXPOSE 5000                    # Dokumentation: "appen lyssnar på 5000"
CMD ["python", "main.py"]      # main.py startar Flask på port 5000
```

**Om de inte matchar:**
```dockerfile
EXPOSE 3000                                    # Säger port 3000
CMD ["python", "-m", "flask", "run", "--port=8000"]  # Startar på port 8000

# Förvirrande! EXPOSE ljuger om vilken port som används
```

### **🎯 Best Practices:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app

# Cache-optimerat: requirements först
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kod sist (ändras oftast)
COPY . .

# Dokumentera korrekt port
EXPOSE 5000

# Kör appen
CMD ["python", "main.py"]
```

## 🎉 Sammanfattning

### **Dockerfile:**
- **Recept** för att bygga en image
- **FROM** = basimage
- **COPY** = kopiera filer
- **RUN** = kör kommando under bygget
- **CMD** = vad som körs när containern startar

### **Docker Commands:**
- **build** = skapa image från Dockerfile
- **run** = starta container från image
- **-t** = tagga image
- **-p** = port mapping
- **-d** = detached mode

### **Docker Compose:**
- **Flera containers** tillsammans
- **YAML-format** för konfiguration
- **docker-compose up** = starta allt

### **Katalog-syntax:**
- **.** = current directory
- **..** = parent directory
- **COPY . .** = kopiera allt till workdir

Nu har du grunden för Docker! 🚀