# Övning: Skapa en GitHub Actions Workflow för Ruff-lintning

I denna övning kommer du att skapa en GitHub Actions workflow för att köra Ruff-lintning på ditt projekt. Du kan använda ett befintligt projekt eller skapa ett nytt.

## Steg för steg

1. **Förbered ditt projekt**
   - Se till att ditt projekt har en `requirements.txt`-fil med alla nödvändiga beroenden.
   - Om du inte har ett projekt, skapa ett enkelt Python-projekt med en `app.py` och `requirements.txt`.

2. **Skapa en workflow-fil**
   - Skapa en mapp `.github/workflows/` i ditt projekt om den inte redan finns.
   - Skapa en fil `linting.yml` i denna mapp.

3. **Definiera din workflow**
   - Använd följande YAML-konfiguration som en mall:

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

4. **Testa din workflow**
   - Gör en commit och pusha dina ändringar till GitHub.
   - Gå till fliken "Actions" i ditt GitHub-repo för att se din workflow i aktion.

5. **Felsökning och förbättringar**
   - Om din workflow misslyckas, kontrollera loggarna för att se vad som gick fel.
   - Lägg till fler steg i din workflow för att köra tester eller andra verktyg.

## Tips och ledtrådar

- **Använd rätt Python-version**: Se till att `python-version` i din workflow matchar den version du använder i ditt projekt.
- **Kontrollera beroenden**: Se till att alla nödvändiga paket finns i `requirements.txt`.
- **Utforska GitHub Actions**: Det finns många färdiga actions i GitHub Marketplace som kan hjälpa dig att automatisera olika delar av din CI/CD-process.
