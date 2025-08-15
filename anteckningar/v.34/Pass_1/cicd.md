# CI/CD med GitHub Actions

## Vad är CI/CD?

**CI/CD** står för **Continuous Integration** (Kontinuerlig Integration) och **Continuous Deployment** (Kontinuerlig Deployment).

### Varför behöver vi CI/CD?

**Problemet utan CI/CD:**
```
Utvecklare pushes kod → Någon annan testar manuellt → Deployment till server manuellt
```
- Manuella steg = risk för fel
- Långsam feedback 
- Ingen standardisering
- "Det fungerar på min maskin"-problem

**Lösningen med CI/CD:**
```
git push → Automatisk test → Automatisk deployment → Notifiering
```

### Fördelar med CI/CD
- ✅ **Snabbare feedback** - Problem upptäcks inom minuter
- ✅ **Mindre risk** - Automatiserade tester fångar fel tidigt
- ✅ **Reproducerbarhet** - Samma process varje gång
- ✅ **Snabbare releases** - Från dagar till minuter

> **📖 Läs mer:** För en översikt av andra CI/CD-verktyg i industrin, se [CI/CD Alternativ](./cicd_alternativ.md)

---

## GitHub Actions: Grunder

GitHub Actions är GitHubs inbyggda CI/CD-plattform. Den kör **workflows** (arbetsflöden) baserat på **events** (händelser) i ditt repository.

### Kärnkoncept

| Koncept | Beskrivning |
|---------|-------------|
| **Workflow** | En automatiserad process (t.ex. "testa och deploya") |
| **Job** | En uppsättning steg som körs på samma runner |
| **Step** | En enskild uppgift (t.ex. "kör tester") |
| **Runner** | En virtuell maskin som kör dina jobs (Ubuntu, Windows, macOS) |
| **Action** | En färdig komponent (t.ex. "checkout kod") |

### Workflow-struktur
```yaml
name: Min Workflow
on: [push]                    # Trigger: När någon pushar kod
jobs:
  test:                       # Job namn
    runs-on: ubuntu-latest    # Runner typ
    steps:                    # Lista av steg
      - name: Checka ut kod
        uses: actions/checkout@v3
      - name: Kör tester
        run: npm test
```

---

## Din första GitHub Actions Workflow

### Steg 1: Skapa workflow-mappen
I ditt lokala Git repository, skapa denna struktur:
```
ditt-projekt/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── app.py
├── tests/
│   └── test_app.py
├── Dockerfile
└── requirements.txt
```

### Steg 2: En enkel Python-app
Skapa `src/app.py`:
```python
def hello_world():
    return "Hello, World!"

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    print(hello_world())
```

Skapa `tests/test_app.py`:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import hello_world, add_numbers

def test_hello_world():
    assert hello_world() == "Hello, World!"

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
```

Skapa `requirements.txt`:
```
pytest==7.1.2
```

### Steg 3: Din första workflow
Skapa `.github/workflows/ci.yml`:
```yaml
name: Continuous Integration

# När ska denna workflow köras?
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Kör tester
    runs-on: ubuntu-latest
    
    steps:
    # Steg 1: Hämta koden från repository
    - name: Checkout kod
      uses: actions/checkout@v3
    
    # Steg 2: Sätt upp Python
    - name: Sätt upp Python 3.9
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    # Steg 3: Installera dependencies
    - name: Installera dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    # Steg 4: Kör tester
    - name: Kör tester med pytest
      run: |
        pytest tests/ -v
```

### Steg 4: Testa din workflow
```bash
# Lägg till alla filer
git add .

# Committa
git commit -m "Add CI workflow with tests"

# Pusha till GitHub
git push origin main
```

Gå till ditt repository på GitHub och klicka på fliken "Actions". Du ska se din workflow köra!

---

## Docker i CI/CD

Nu ska vi bygga och testa Docker-images i vår pipeline.

### Steg 1: Skapa en Dockerfile
Skapa `Dockerfile` i projektets root:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Kopiera requirements först (för bättre caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera applikationskod
COPY src/ .

# Exponera port
EXPOSE 5000

# Kör applikationen
CMD ["python", "app.py"]
```

### Steg 2: Uppdatera workflow för Docker
Skapa `.github/workflows/docker-ci.yml`:
```yaml
name: Docker CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Kör tester
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout kod
      uses: actions/checkout@v3
    
    - name: Sätt upp Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Installera dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Kör tester
      run: pytest tests/ -v

  build:
    name: Bygg Docker image
    runs-on: ubuntu-latest
    needs: test  # Kör bara om testerna passerar
    
    steps:
    - name: Checkout kod
      uses: actions/checkout@v3
    
    - name: Sätt upp Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Bygg Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: false  # Publicera inte än
        tags: my-app:latest
    
    - name: Testa Docker image
      run: |
        docker build -t my-app:test .
        docker run --rm my-app:test python -c "from app import hello_world; print(hello_world())"
```

---

## Spara Docker Images som Artifacts

Istället för att deploya till Docker Hub kan vi spara våra byggda images som **artifacts** i GitHub. Det här är perfekt för testing och intern distribution.

### Uppdaterad workflow med artifacts
Uppdatera `.github/workflows/docker-ci.yml`:
```yaml
name: Docker CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Kör tester
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout kod
      uses: actions/checkout@v3
    
    - name: Sätt upp Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9
    
    - name: Installera dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Kör tester
      run: pytest tests/ -v

  build-and-save:
    name: Bygg och spara Docker image
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'  # Bara på main branch
    
    steps:
    - name: Checkout kod
      uses: actions/checkout@v3
    
    - name: Sätt upp Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Bygg Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        tags: my-app:latest
        outputs: type=docker,dest=/tmp/my-app.tar
    
    - name: Testa Docker image
      run: |
        docker load -i /tmp/my-app.tar
        docker run --rm my-app:latest python -c "from app import hello_world; print(hello_world())"
    
    - name: Upload Docker image som artifact
      uses: actions/upload-artifact@v3
      with:
        name: docker-image
        path: /tmp/my-app.tar
        retention-days: 30
```

### Fördelar med artifacts:
- ✅ **Ingen extern service** behövs
- ✅ **Gratis** (ingår i GitHub)
- ✅ **Enkelt att komma åt** från GitHub UI
- ✅ **Automatisk cleanup** efter 30 dagar

---

## Avancerade GitHub Actions-koncept

### Environment Variables och Secrets
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production
      API_URL: ${{ secrets.API_URL }}
    
    steps:
    - name: Deploy till staging
      run: |
        echo "Deploying to $NODE_ENV"
        echo "API URL: $API_URL"
```

### Matrix builds (Testa flera versioner)
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    
    steps:
    - uses: actions/checkout@v3
    - name: Sätt upp Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Kör tester
      run: pytest
```

