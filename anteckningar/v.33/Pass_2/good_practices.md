# Best Practices för Data Engineering Studenter

## 🎯 Syfte

Detta är en praktisk guide med **viktiga regler** som du bör följa från dag ett. Dessa practices kommer rädda dig från huvudvärk och hålla dina projekt organiserade och säkra.

---

## 🗂️ Projektorganisation

### **📁 Alltid ny miljö för varje projekt**

```bash
# FEL - Jobba direkt i hem-katalogen
cd ~
python main.py  # Blandar paket mellan projekt!

# RÄTT - Skapa isolerad miljö
mkdir mitt_nya_projekt
cd mitt_nya_projekt
python -m venv venv
source venv/bin/activate  # Linux/Mac
# eller: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**Varför viktigt:**
- Olika projekt kräver olika versioner av paket
- Undviker konflikter mellan dependencies
- Lätt att dela exakta versioner med teamet

### **📦 Hantera dependencies med pip freeze**

```bash
# När du installerat paket i ditt projekt:
pip install pandas requests flask

# Frys alla versioner till requirements.txt
pip freeze > requirements.txt

# Nu innehåller requirements.txt exakt vilka versioner du använde:
# pandas==2.0.3
# requests==2.31.0
# flask==3.0.0
# (plus alla dependencies dessa paket behöver)
```

**Workflow för teamarbete:**
```bash
# Utvecklare A installerar och fryser
pip install new-package
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add new-package dependency"

# Utvecklare B syncar och installerar samma versioner
git pull
pip install -r requirements.txt  # Får exakt samma miljö!
```

### **📋 Standard projektstruktur**

```
mitt_projekt/
├── README.md           # Vad projektet gör + hur man kör det
├── requirements.txt    # Python dependencies
├── .env                # Secrets (ALDRIG i Git!)
├── .gitignore         # Vad Git ska ignorera
├── docker-compose.yml # Om du använder Docker
├── src/               # Din kod
│   ├── main.py
│   └── utils.py
├── data/              # Data files
│   ├── raw/
│   └── processed/
└── tests/             # Tester för din kod
```

---

## 🔒 Säkerhet och Secrets

### **🚫 ALDRIG commita hemligheter**

```bash
# Skapa .env för secrets
echo "DATABASE_URL=postgresql://user:secret@localhost:5432/db" > .env
echo "API_KEY=super_secret_key_123" >> .env
echo "AWS_ACCESS_KEY=AKIA..." >> .env

# Lägg .env i .gitignore OMEDELBART
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo "__pycache__/" >> .gitignore
echo ".DS_Store" >> .gitignore
```

### **📝 Använda .env i kod**

```python
# Installera python-dotenv först
# pip install python-dotenv

import os
from dotenv import load_dotenv

# Ladda .env-filen
load_dotenv()

# Använd secrets säkert
database_url = os.getenv("DATABASE_URL")
api_key = os.getenv("API_KEY")
```

### **🛡️ Komplett .gitignore mall**

```gitignore
# Secrets och miljödata
.env
*.env
service-account-key.json
*.pem
*.key

# Python
__pycache__/
*.py[cod]
*.so
venv/
env/
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs och temporära filer
*.log
*.tmp
*.pid

# Data (ofta för stora för Git)
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Docker
.dockerignore
```

---

## 🐙 Git Workflow - Rätt från början

### **🆕 Starta nytt projekt**

```bash
# Alternativ 1: Skapa lokalt först
mkdir mitt_projekt
cd mitt_projekt
git init
echo "# Mitt Projekt" > README.md
echo ".env" > .gitignore
git add .
git commit -m "Initial commit"

# Skapa repo på GitHub, sedan:
git remote add origin git@github.com:username/mitt_projekt.git
git push -u origin main
```

```bash
# Alternativ 2: Klona befintligt projekt
git clone git@github.com:username/befintligt_projekt.git
cd befintligt_projekt
```

### **📥 Alltid börja med att synca**

```bash
# FÖRSTA SAKEN du gör när du börjar jobba:
git pull origin main

# Sedan skapa ny branch för din feature
git checkout -b feature/ny-funktion
```

### **📤 Daily Git routine**

```bash
# 1. Kolla vad som ändrats
git status

# 2. Lägg till specifika filer (ALDRIG git add .)
git add src/main.py
git add README.md

# 3. Commit med beskrivande meddelande
git commit -m "Add data validation for user input"

# 4. Pusha din branch
git push origin feature/ny-funktion

# 5. Skapa Pull Request på GitHub för code review
```

### **🔄 Merge konflikter - steg för steg**

```bash
# När konflikter uppstår:
git pull origin main

# Git visar konflikter i filer med <<<<<<< ======= >>>>>>>
# Öppna filerna och fixa konflikterna manuellt

# Efter fix:
git add fil_med_konflikt.py
git commit -m "Resolve merge conflict in data processing"
git push origin feature/ny-funktion
```

---

## 🐳 Docker Best Practices

### **📦 Alltid starta med rätt Dockerfile**

```dockerfile
# Använd specifik version, inte "latest"
FROM python:3.11-slim

# Sätt working directory
WORKDIR /app

# Kopiera requirements först (för cache-optimering)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera kod sist (ändras oftast)
COPY src/ ./src/
COPY .env .

# Exponera port tydligt
EXPOSE 5000

# Kör applikationen
CMD ["python", "src/main.py"]
```

### **🚀 Docker-compose för utveckling**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app          # Live reload under utveckling
      - ./data:/app/data
    environment:
      - FLASK_ENV=development
      - DEBUG=true
    env_file:
      - .env            # Ladda secrets säkert

  database:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### **🧹 Docker underhåll**

```bash
# Städa upp regelbundet
docker system prune -f

# Ta bort oanvända images
docker image prune -f

# Lista stora containers/images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## 💻 Bash/Terminal Effektivitet

### **⚡ Användbara aliases**

```bash
# Lägg i ~/.bashrc eller ~/.zshrc
alias ll='ls -la'
alias la='ls -la'
alias ..='cd ..'
alias ...='cd ../..'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git pull'
alias python='python3'
alias pip='pip3'

# Ladda om config
source ~/.bashrc
```

### **📁 Navigering och sökande**

```bash
# Hitta filer snabbt
find . -name "*.py" -type f

# Sök i filinnehåll
grep -r "TODO" src/

# Visa stora filer
du -sh * | sort -h

# Snabb backup
cp important_file.py important_file.py.backup

# Rensa terminal men behåll history
clear
```

---

## 🔄 Utvecklingsworkflow

### **📋 Daglig checklista**

1. ✅ **Start av dagen:**
   ```bash
   git pull origin main
   source venv/bin/activate
   docker-compose up -d  # Om du använder docker
   ```

2. ✅ **Under utveckling:**
   ```bash
   # Testa ofta
   python -m pytest tests/
   
   # Om du installerat nya paket - uppdatera requirements
   pip freeze > requirements.txt
   
   # Commit små, logiska ändringar
   git add specific_file.py requirements.txt
   git commit -m "Fix validation bug in user input"
   ```

3. ✅ **Slutet av dagen:**
   ```bash
   git push origin feature/my-branch
   docker-compose down  # Spara resurser
   deactivate  # Lämna venv
   ```

### **🚨 Innan du lämnar projektet**

```bash
# Kolla att allt är committat
git status

# Pusha allt till GitHub
git push

# Skapa/uppdatera README.md med:
# - Vad projektet gör
# - Hur man installerar dependencies
# - Hur man kör applikationen
# - Exempel på användning
```

---

## ⚠️ Vanliga Fallgropar att Undvika

### **🚫 GÖR ALDRIG:**

```bash
# ALDRIG commit .env eller secrets
git add .env  # STOPP!

# ALDRIG git add . utan att kolla först
git add .  # Farligt! Använd specifika filer

# ALDRIG jobba direkt på main branch
git commit -m "Quick fix" # Skapa branch först!

# ALDRIG stora filer i Git
git add data/massive_dataset.csv  # Använd Git LFS eller .gitignore

# ALDRIG hårdkodade secrets
api_key = "abc123"  # Använd .env istället!
```

### **✅ GÖR ISTÄLLET:**

```bash
# Kolla alltid vad du committar
git status
git diff

# Använd specifika git add
git add src/main.py README.md

# Skapa branch för varje feature
git checkout -b feature/user-authentication

# Använd .env för secrets
load_dotenv()
api_key = os.getenv("API_KEY")

# Stora filer: Git LFS eller cloud storage
git lfs track "*.csv"
```

---

## 🎯 Sammanfattning: Gyllene Regler

1. **🏗️ Nytt projekt = ny virtual environment**
2. **🔒 Secrets i .env, ALDRIG i Git**
3. **📝 .gitignore från dag ett**
4. **🔄 Git pull innan du börjar jobba**
5. **🌿 Alltid arbeta i brancher, aldrig direkt på main**
6. **💬 Tydliga commit-meddelanden**
7. **🐳 Docker: specifika versioner, optimera cache**
8. **📋 README.md som förklarar hur man kör projektet**
9. **🧪 Testa före commit**
10. **🧹 Städa Docker-images regelbundet**

**Kom ihåg:** Det tar 2 minuter att sätta upp rätt från början, men timmar att fixa senare! 

---

*"En timme av planering sparar tio timmar av debugging"* - Varje erfaren utvecklare 🧠⚡