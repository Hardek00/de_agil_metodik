# Docker Anteckningar

## Vad är Docker?

Docker är en **containeriseringsteknologi** som paketerar applikationer med alla dependencies i isolerade "containers".

> **Analogi:** Som shipping containers för kod - samma "låda" fungerar överallt

## Huvudproblemet Docker löser

### "Det fungerar på min maskin"-problemet

```
Utvecklare: "Min app fungerar perfekt!"
Production: *Kraschar*
DevOps: "Vad är skillnaden mellan din miljö och servern?"
```

**Lösning:** Samma miljö överallt genom containers

## Fördelar med Docker

### 1. Konsistenta miljöer
- **Problem:** Olika versioner av dependencies på olika maskiner
- **Lösning:** Allt paketerat i container
```dockerfile
FROM node:18
COPY package.json .
RUN npm install
COPY . .
CMD ["npm", "start"]
```

### 2. Snabb deployment
**Traditionellt:**
```bash
ssh server
sudo apt update
sudo apt install node python nginx mysql
# konfiguration, debugging, konflikter...
```

**Med Docker:**
```bash
docker run my-app
# Klart! 🚀
```

### 3. Isolation mellan projekt
```bash
docker run -p 3000:3000 project-a  # Node.js 16
docker run -p 3001:3001 project-b  # Node.js 18  
docker run -p 3002:3002 project-c  # Python 3.9
```
- Inga konflikter mellan olika projektversioner
- Olika tech stacks kan köras samtidigt

### 4. Enkel skalbarhet
```bash
# Starta 10 kopior av din app
docker run --replicas=10 my-web-app
```

## Praktiska användningsområden

### Microservices-arkitektur
```bash
docker run database
docker run api-service
docker run web-frontend  
docker run payment-service
```
- Varje tjänst isolerad och oberoende
- Kan utvecklas och deployas separat

### Utvecklingsmiljö
```bash
# Hela tech stack med ett kommando
docker-compose up
# Database + Redis + API + Frontend = igång på 30 sekunder
```

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

## Docker vs andra lösningar

| Lösning | Prestanda | Komplexitet | Isolation |
|---------|-----------|-------------|-----------|
| Native installation | Hög | Hög | Låg |
| Virtual Machines | Låg | Hög | Hög |
| **Docker containers** | **Hög** | **Låg** | **Hög** |

## Vanliga Docker-kommandon

```bash
# Grundläggande
docker run <image>              # Kör container
docker build -t <name> .        # Bygg image
docker ps                       # Lista containers
docker stop <container>         # Stoppa container

# Utveckling
docker-compose up              # Starta hela stack
docker-compose down            # Stoppa hela stack
docker logs <container>        # Visa loggar
docker exec -it <container> bash # Logga in i container
```

## Sammanfattning

**Docker = "Shipping container för kod"** 📦

Precis som shipping containers revolutionerade handel genom standardisering, har Docker revolutionerat mjukvarudeployment genom:

1. **Portabilitet** - Kör överallt
2. **Konsistens** - Samma miljö överallt  
3. **Isolation** - Inga konflikter
4. **Effektivitet** - Snabbare än VMs
5. **Skalbarhet** - Enkelt att skala upp/ner

**Med WSL2:** Du får Linux-prestanda på Windows, vilket gör Docker till den perfekta utvecklingsmiljön för moderna applikationer. 