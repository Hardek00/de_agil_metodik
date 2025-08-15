# Guide: Skapa enkel CI med Ruff-lintning i GitHub Actions

## Vad är linting och varför är det viktigt?

**Linting** är processen att analysera kod för att hitta potentiella fel, stilproblem och kodkvalitetsproblem innan koden körs. En linter är ett verktyg som automatiskt granskar din kod och rapporterar:

- **Syntaxfel**: Kod som inte följer språkets syntax
- **Stilproblem**: Kod som inte följer etablerade stilriktlinjer (t.ex. indentation, radlängd, namngivning)
- **Potentiella buggar**: Oanvänd variabel, importerade moduler som inte används, etc.
- **Kodkvalitet**: Komplex kod som kan förenklas, dålig struktur, etc.

### Fördelar med linting:
- **Förebygger fel**: Hittar problem innan koden når produktion
- **Konsistent kodstil**: Alla utvecklare följer samma regler
- **Lättare underhåll**: Ren, strukturerad kod är enklare att förstå och uppdatera
- **Automatisk kvalitetskontroll**: Ingen manuell granskning behövs för grundläggande stilfrågor

---

Den här guiden förklarar hur du sätter upp en minimal Continuous Integration (CI)-pipeline för ett Python-projekt med GitHub Actions, med fokus på kodgranskning (lintning) med Ruff.

## 1. Filstruktur

Ditt projekt bör se ut så här:

```
my_awesome_flask_app/
├── app.py
├── requirements.txt
├── Dockerfile
├── ruff.toml (eller pyproject.toml)
└── .github/
    └── workflows/
        └── ci.yml
```

- `.github/workflows/ci.yml`: Workflow-filen som definierar din CI-pipeline.
- `requirements.txt`: Lista över dina Python-beroenden.
- `app.py`: Din huvudapplikationskod.
- `Dockerfile`: (Valfritt) För containerisering.
- `ruff.toml` eller `pyproject.toml`: (Valfritt) Konfigurationsfil för Ruff (linter).

## 2. Vad är Ruff och vad gör ruff.toml?

- **Ruff** är en modern, extremt snabb linter för Python, skriven i Rust. Den kan ersätta flake8, isort och flera andra verktyg. Ruff hittar både stil- och kodfel och kan även sortera importsatser.
- **ruff.toml** (eller konfiguration i pyproject.toml) är en valfri konfigurationsfil som styr vilka regler Ruff ska använda, vilka mappar som ska ignoreras, radlängd, Python-version m.m. **Ruff fungerar utmärkt med standardinställningar**, men konfigurationsfilen är användbar när du vill anpassa reglerna för ditt projekt. Om du har en konfigurationsfil ska den alltid versionshanteras så att alla utvecklare och CI använder samma regler.

### Exempel på ruff.toml

```toml
# ruff.toml
# Vilken Python-version koden ska tolkas som
# (t.ex. "py311" för Python 3.11)
target-version = "py311"

# Maxlängd på kodrader (t.ex. 88 för att matcha Black-formattern)
line-length = 88

# Vilka regel-familjer som ska användas (E=pycodestyle, F=pyflakes)
select = ["E", "F"]

# Regler att ignorera (E501 = för långa rader)
ignore = ["E501"]

# Mappar som Ruff ska ignorera vid lintning
exclude = [".venv", "build", "__pycache__"]
```

#### Förklaring av de viktigaste inställningarna:
- `target-version`: Vilken Python-version Ruff ska tolka koden som.
- `line-length`: Maxlängd på kodrader.
- `select`: Vilka regel-familjer som ska användas.
- `ignore`: Vilka regler som ska ignoreras.
- `exclude`: Mappar som Ruff ska ignorera vid lintning.

## 3. Exempel på workflow-fil (ci.yml) med Ruff

```yaml
name: Lint CI

on:
  push:
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Installera beroenden
        run: |
          python -m pip install --upgrade pip
          pip install ruff
      - name: Kör Ruff linter
        run: ruff check .
```

## 4. Saker att tänka på

- **Välj en linter**: Ruff är snabb och modern, men det finns även andra alternativ (flake8, pylint, black, etc).
- **Misslyckade byggen**: Workflowen misslyckas om lintningsfel hittas. Åtgärda dem lokalt innan du pushar.
- **Konfigurationsfil**: Ha alltid ruff.toml eller pyproject.toml i versionshanteringen.
- **Branch-skydd**: Du kan kräva att CI går igenom innan pull requests får mergas (ställs in i GitHub repo-inställningar).
- **Egna regler**: Anpassa ruff.toml efter projektets behov.

## 5. Nästa steg

- Lägg till fler jobb för testning, bygg eller deployment när projektet växer.
- Utforska GitHub Actions Marketplace för fler actions och integrationer.

---

Med denna setup kontrolleras din kod automatiskt för stilproblem och kodfel varje gång du pushar eller öppnar en pull request.
