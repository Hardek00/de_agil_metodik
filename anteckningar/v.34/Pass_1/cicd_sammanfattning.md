# CI/CD – Verktyg & Automation

## Grupprogrammering
- Större team → mer struktur behövs.
- För lite struktur = kaos. För mycket i små team → minskad produktivitet.
- Anpassa utvecklarvanor: mer kommunikation, mindre YOLO.

---

## CI/CD – Grundidé
- Kör automatiska pipelines vid kodändringar för att hitta buggar.
- Snabb feedback till utvecklare.
- Gemensamma regler → bättre kodkvalitet.
- Främjar transparens & kunskapsdelning.

---

## CI/CD i praktiken
1. Utveckla kod.
2. Commit & push till GitHub.
3. GitHub triggar CI som installerar projektet.
4. Tester körs, fel rapporteras.
5. Utvecklare fixar & kör om.

---

## Projektets CI/CD-flöde
- Klona repo från GitHub.
- Installera Python-krav.
- Kolla kodstil/format.
- Köra tester.

**Konfiguration (GitHub Actions)**  
`my-repo/.github/workflows/example.yaml`
- Trigga: t.ex. vid pull request.
- OS & Python-version.
- Steg: checkout → install dependencies → pytest.

---

## Kodformattering
### Black – Kodformatterare
- Standardiserar kodstil, endast kosmetiska ändringar.
- Lättare att läsa, undviker stilkonflikter.

### isort – Importsortering
- Delar upp: inbyggda → tredjepart → projekt-specifika.

---

## Testning
- Identifierar problem och oönskade bieffekter.
- Dokumenterar avsedd funktionalitet.
- Typer:
  - **Unit tests** – minsta testbara enhet.
  - **Integration tests** – interaktion mellan moduler.
  - **Regression tests** – upptäcker oväntade ändringar.
  - Andra: acceptance, performance, security.

**Pytest**
- Populär testframework för Python.
- Hittar filer/funktioner som börjar med `test`.

---

## Övriga verktyg
- **Flake8** – statisk kodanalys, t.ex. oanvända variabler.
- **Ruff** – snabb, kombinerar funktionalitet från många verktyg.

---

**Källor:**
- https://github.com/psf/black
- https://github.com/PyCQA/isort
- https://docs.pytest.org/
- https://pre-commit.com/
- https://flake8.pycqa.org/
- https://github.com/astral-sh/ruff
