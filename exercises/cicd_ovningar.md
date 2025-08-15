## Övningar

### Övning 1: Grundläggande CI Pipeline
1. Skapa ett nytt GitHub repository med en enkel Python-app
2. Lägg till pytest-tester
3. Skapa en GitHub Actions workflow som kör testerna vid varje push
4. Trigga en build och verifiera att den fungerar

### Övning 2: Docker CI/CD
1. Lägg till en Dockerfile till ditt projekt
2. Uppdatera din workflow för att bygga Docker-imagen
3. Lägg till ett steg som testar den byggda imagen
4. Spara Docker-imagen som en GitHub artifact
5. Ladda ner och testa den sparade imagen lokalt


### Övning 3: Matrix Testing
1. Konfigurera din workflow för att testa mot flera Python-versioner
2. Testa mot både Ubuntu och Windows runners
3. Analysera resultaten och förstå varför matrix builds är viktiga