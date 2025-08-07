# Docker: Praktiska Övningar

## Mål
Dessa övningar är designade för att ge dig praktisk erfarenhet av de vanligaste Docker-koncepten, från att köra en befintlig container till att bygga och orkestrera dina egna applikationer.

## Förutsättningar
- Docker Desktop installerat och igång.
- WSL2 konfigurerat som backend för Docker Desktop.
- En terminal (som WSL/Ubuntu).

---

### Övning 1: "Hello, Docker!" - Kör din första container

**Mål:** Förstå `docker pull` och `docker run`.

1.  **Kör en test-container:**
    Docker kommer med en inbyggd test-image som heter `hello-world`. Kör den:
    ```bash
    docker run hello-world
    ```
    Du bör se ett meddelande som bekräftar att din installation fungerar. Docker laddade ner (pull) och körde (run) imagen automatiskt.

2.  **Kör en interaktiv shell:**
    Låt oss köra en fullständig Linux-distribution, som Ubuntu, interaktivt.
    ```bash
    docker run -it ubuntu bash
    ```
    - `-it` står för **i**nteractive & **t**ty, vilket ger dig en interaktiv shell inuti containern.
    - `ubuntu` är imagen vi vill köra.
    - `bash` är kommandot vi vill starta inuti containern.

    Din prompt kommer att ändras. Du är nu *inuti* en Ubuntu-container! Testa att köra några kommandon som `ls /` eller `echo "Jag är i en container"`. Skriv `exit` för att avsluta och återgå till din vanliga terminal.

3.  **Se vilka containers som körs:**
    Öppna en *ny* terminal (lämna den andra öppen om du vill) och kör:
    ```bash
    docker ps
    # Och för att se alla containers, även de som stoppats:
    docker ps -a
    ```
    Du kommer se `hello-world` och `ubuntu`-containrarna du just kört.

---

### Övning 2: Kör en webbserver

**Mål:** Förstå portmappning och att köra containers i bakgrunden (detached mode).

1.  **Starta en Nginx-webbserver:**
    Nginx är en populär webbserver. Låt oss starta en container från dess officiella image.
    ```bash
    docker run --name min-webbserver -d -p 8080:80 nginx
    ```
    - `--name min-webbserver`: Ger din container ett lättigenkännligt namn.
    - `-d`: **D**etached mode. Kör containern i bakgrunden så att du får tillbaka din terminalprompt.
    - `-p 8080:80`: **P**ublish port. Mappar port **8080** på din dator (host) till port **80** inuti containern (där Nginx lyssnar).
    - `nginx`: Imagen som ska köras.

2.  **Besök din webbserver:**
    Öppna en webbläsare och gå till `http://localhost:8080`. Du bör se Nginx välkomstsida!

3.  **Stoppa och ta bort containern:**
    ```bash
    # Stoppa containern
    docker stop min-webbserver

    # Ta bort containern (måste vara stoppad först)
    docker rm min-webbserver
    ```

---

### Övning 3: Bygg din egen image (Dockerfile)

**Mål:** Skapa en anpassad image för en enkel Python-applikation.

1.  **Skapa en projektkatalog:**
    ```bash
    mkdir min-python-app
    cd min-python-app
    ```

2.  **Skapa en Python-fil (`app.py`):**
    Skapa en fil med namnet `app.py` och klistra in följande kod. Detta är en minimal webbapp som använder Flask.
    ```python
    from flask import Flask
    import os

    app = Flask(__name__)

    @app.route('/')
    def hello():
        # Läs containerns hostname
        container_id = os.uname().nodename
        return f"<h1>Hello from Docker!</h1><p>Running inside container: {container_id}</p>"

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
    ```

3.  **Skapa en `requirements.txt`-fil:**
    ```
    Flask==2.1.2
    ```

4.  **Skapa en `Dockerfile`:**
    Detta är receptet för att bygga din image. Skapa en fil med namnet `Dockerfile` (utan filändelse) och klistra in:
    ```dockerfile
    # Använd en officiell Python-image som bas
    FROM python:3.9-slim

    # Sätt arbetskatalogen inuti containern
    WORKDIR /app

    # Kopiera filen med dependencies först (för att dra nytta av cache)
    COPY requirements.txt .

    # Installera dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Kopiera resten av applikationskoden
    COPY . .

    # Exponera porten som appen körs på
    EXPOSE 5000

    # Kommando för att köra appen när containern startar
    CMD ["python", "app.py"]
    ```

5.  **Bygg din image:**
    Se till att du är i `min-python-app`-katalogen och kör:
    ```bash
    docker build -t min-app:1.0 .
    ```
    - `-t min-app:1.0`: **T**ag (namnge) din image som `min-app` med version `1.0`.
    - `.`: Sökvägen till din `Dockerfile` (punkten betyder nuvarande katalog).

6.  **Kör din anpassade image:**
    ```bash
    docker run --name min-webb-app -d -p 5000:5000 min-app:1.0
    ```
    Gå till `http://localhost:5000` i din webbläsare. Du bör se meddelandet från din Python-app!

---

### Övning 4: Multi-container med Docker Compose

**Mål:** Använda `docker-compose` för att köra en applikation som är beroende av en annan tjänst (en Redis-databas).

1.  **Uppdatera `app.py`:**
    Vi ska lägga till en enkel besöksräknare som använder Redis. Ersätt innehållet i `app.py` med detta:
    ```python
    from flask import Flask
    from redis import Redis
    import os

    app = Flask(__name__)
    # Använd servicenamnet 'redis' från docker-compose.yml
    redis = Redis(host='redis', port=6379)

    @app.route('/')
    def hello():
        # Öka räknaren i Redis med 1 varje gång sidan besöks
        redis.incr('hits')
        # Hämta nuvarande värde (måste avkodas från bytes)
        counter = redis.get('hits').decode('utf-8')
        return f"<h1>Hello from Docker Compose!</h1><p>This page has been viewed {counter} time(s).</p>"

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=5000)
    ```

2.  **Uppdatera `requirements.txt`:**
    Lägg till `redis`:
    ```
    Flask==2.1.2
    redis==4.3.4
    ```

3.  **Skapa `docker-compose.yml`:**
    Detta är filen som definierar dina tjänster. Skapa `docker-compose.yml` i samma katalog.
    ```yaml
    version: '3.8'
    services:
      # Vår Python webbapp
      webapp:
        build: .
        ports:
          - "5000:5000"
        volumes: # Mappa koden så att ändringar slår igenom direkt
          - .:/app
        depends_on:
          - redis

      # Redis-databasen
      redis:
        image: "redis:alpine"
    ```

4.  **Kör med Docker Compose:**
    Stoppa och ta bort den tidigare containern om den fortfarande körs (`docker stop min-webb-app && docker rm min-webb-app`). Kör sedan:
    ```bash
    docker-compose up --build
    ```
    Docker Compose kommer att:
    - Bygga din `webapp`-image.
    - Ladda ner `redis`-imagen.
    - Starta båda containrarna och koppla ihop dem i ett nätverk.

    Gå till `http://localhost:5000`. Uppdatera sidan några gånger och se hur räknaren ökar! Tryck `Ctrl+C` i terminalen för att stoppa. Kör `docker-compose down` för att ta bort nätverket och containrarna.

---

### Övning 5: Persistera data med volymer

**Mål:** Spara data från en databas-container på din lokala dator så att den inte försvinner.

1.  **Starta en PostgreSQL-databas med en volym:**
    ```bash
    docker run --name min-postgres -d \
      -e POSTGRES_PASSWORD=mysecretpassword \
      -p 5432:5432 \
      -v postgres-data:/var/lib/postgresql/data \
      postgres
    ```
    - `-e`: Sätter en **e**nvironment variable, här för att sätta lösenordet.
    - `-v postgres-data:/var/lib/postgresql/data`: Detta är nyckeln! Det skapar en **v**olym med namnet `postgres-data` och mappar den till katalogen *inuti containern* där Postgres lagrar sin data.

2.  **Stoppa och ta bort containern:**
    ```bash
    docker stop min-postgres
    docker rm min-postgres
    ```
    Normalt sett skulle all data nu vara borta.

3.  **Starta en ny container med samma volym:**
    Kör exakt samma `docker run`-kommando igen:
    ```bash
    docker run --name min-postgres-2 -d \
      -e POSTGRES_PASSWORD=mysecretpassword \
      -p 5432:5432 \
      -v postgres-data:/var/lib/postgresql/data \
      postgres
    ```
    Även om detta är en helt ny container, återanvänder den `postgres-data`-volymen. Om du hade skapat tabeller och lagt in data i den första containern, skulle den finnas kvar i den andra.

4.  **Inspektera och rensa volymen:**
    ```bash
    # Lista alla volymer
    docker volume ls

    # Ta bort volymen (och all data i den)
    docker volume rm postgres-data
    ```

Grattis! Du har nu praktisk erfarenhet av de viktigaste Docker-koncepten! 