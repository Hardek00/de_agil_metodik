# Docker 101 – Sammanfattning

En kort introduktion till containerisering och Docker

---

## Varför Containerisering?
- **Lokalt utvecklande:** Löser problemet *"It works on my machine"*.
- **Molnproduktion:** Löser problemet *"This architecture doesn't scale"*.

---

## Big picture:
- **Bare metal**: Fysisk hårdvara (CPU, RAM, disk).
- **Operativsystem & Kernel**: Mellanlager mellan hårdvara och applikationer.
- **Klient och server**: Kommunikation via nätverk.
- **Skalning**:
  - **Vertikal:** Mer CPU/RAM till samma server.
  - **Horisontell:** Flera mindre servrar/mikrotjänster.

---

## Från Bare Metal → Virtuella maskiner → Docker
- **VMs**: Flera OS på samma maskin via hypervisor. Resursallokering är fast.
- **Docker**: Delar samma OS-kernel, resurser dynamiskt.

---

## Hur Docker fungerar
1. **Dockerfile** – Instruktioner för att bygga miljön.
2. **Image** – OS + beroenden + kod. Oföränderlig snapshot.
3. **Container** – Körbar instans av en image.

Flöde: Dockerfile → build → Image → run → Container.

**Containers är:**
- Isolerade
- Portabla
- Statelösa

Isolerade
Varje container kör sin applikation och dess beroenden i en separat miljö, utan att störa andra containers eller värdsystemet.
Detta gör att olika projekt kan ha olika biblioteksversioner eller konfigurationer utan konflikter.

Portabla
En container innehåller all kod, alla beroenden och konfigurationer som krävs för att köra applikationen.
Detta innebär att du kan köra den på din laptop, i en testmiljö eller i molnet  och den fungerar på samma sätt överallt.
Portabiliteten bygger på att containern inte är beroende av den underliggande maskinens specifika miljö.

Statelösa
En container lagrar inte beständig data internt — när den stängs av försvinner all intern lagring.
Detta gör dem enkla att starta om, klona och skala upp/ner.
Behöver du spara data använder du volymer eller externa databaser, vilket håller applikationen flexibel och lätt att distribuera.

---
## Installation och verktyg

- **Windows**: Installera Docker Desktop och aktivera WSL2. Kör projekten i WSL-filsystemet (`/home/...`) för bättre prestanda.
- **macOS/Linux**: Docker Desktop eller `docker` via paketmanager.
- **Editor**: VS Code + Docker‑extension (syntax för Dockerfile/Compose, GUI för containers/images).

---

## Viktiga kommandon

```bash
docker ps            # Lista körande containers
docker images        # Lista images
docker build -t <name:tag> .
docker run -p 5000:8080 --name <ctr> <image>
docker stop <ctr> && docker rm <ctr>
docker logs -f <ctr>
```

## Vanliga Dockerfile-instruktioner
```dockerfile
FROM ubuntu:20.04       # Basimage
WORKDIR /app            # Arbetskatalog
RUN apt-get update && apt-get install -y python3
COPY . .                # Kopiera lokala filer
ENV API_KEY=12345       # Miljövariabel
EXPOSE 8080             # Öppna port
CMD ["python3", "app.py"] # Startkommando
```

Andra användbara instruktioner:
- `USER` – Byt till icke-root användare
- `LABEL` – Metadata
- `HEALTHCHECK` – Kontrollera containerstatus
- **Volymer** – För persistent lagring

---

## Viktiga CLI-kommandon
- **Bygga image:**
  ```bash
  docker build -t myapp .
  ```
- **Köra container:**
  ```bash
  docker run -p 8080:8080 myapp

  - Vänster sida (8080) = port på din dator. Höger sida (8080) = port i containern.
- `EXPOSE` är dokumentation; riktig exponering sker med `-p`.
  ```
- **Stoppa container:**
  ```bash
  docker stop <id>
  docker kill <id> # tvångsstopp
  ```
- **Ladda upp/ned image:**
  ```bash
  docker push myapp
  docker pull myapp
  ```

---

## Säkerhet
- **`.dockerignore`** – Uteslut filer från image.
- **Docker Scout** – Identifiera sårbarheter i varje lager.

---

## Multi-container appar & orkestrering
- **Docker Compose**:
  - Definiera flera tjänster i en `docker-compose.yml`.
  - `docker compose up` – Starta alla.
  - `docker compose down` – Stoppa alla.
- **Kubernetes**:
  - För massiv skala och komplexa system.
  - Bygger på pods, noder och en kontrollplan.
  - Automatisk skalning och återställning.

---

### CI/CD Pipeline
```
git push → Docker build → Test i container → Deploy till produktion
```
- Samma container från utveckling till produktion
- Eliminerar miljöskillnader

## Docker + WSL2 = Perfekt kombination

### Före WSL2 på Windows:
- ❌ Docker Desktop med Hyper-V = långsamt
- ❌ Dålig filsystem-prestanda  
- ❌ Memory-hungrigt
- ❌ Extra virtualiseringslager

### Med WSL2:
- ✅ Linux-prestanda på Windows
- ✅ Snabba builds
- ✅ Mindre resursanvändning
- ✅ "Native" Docker (direkt mot Linux-kärnan)

### Arkitektur-jämförelse:

**WSL2 (Native):**
```
Windows → WSL2 (Linux-kärna) → Docker → Container
```

**Hyper-V (Non-native):**
```
Windows → Hyper-V → Linux VM → Docker → Container
```

## Real-world exempel

### Stora företag:
- **Netflix:** 1000+ microservices i containers
- **Google:** 2+ miljarder containers per vecka
- **Spotify:** Alla nya tjänster containeriserade

### För utvecklare:
- ✅ **Snabbare onboarding:** Ny kollega kör `docker-compose up`
- ✅ **Inga miljökonflikter:** Isolerade containers
- ✅ **Production parity:** Samma miljö som produktion
- ✅ **Enklare deployment:** Container fungerar överallt
- ✅ **Bättre testning:** Konsistenta testmiljöer

