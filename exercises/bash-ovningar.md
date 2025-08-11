# Bash Övningar

## Mål
Dessa övningar är designade för att ge dig praktisk erfarenhet av de grundläggande Bash-kommandona för att navigera, hantera filer och automatisera enkla uppgifter.

---

### Övning 1: Navigera och skapa struktur
1.  Öppna din WSL-terminal. Du bör starta i din hemkatalog (`~`).
2.  Skapa en ny katalog för kursen: `mkdir data_engineering_kurs`
3.  Gå in i den nya katalogen: `cd data_engineering_kurs`
4.  Verifiera att du är i rätt katalog med `pwd`.
5.  Skapa underkatalogerna `projekt1`, `anteckningar` och `skript`.
6.  Använd `ls -l` för att se den struktur du har skapat.

---

### Övning 2: Filhantering
1.  Gå in i katalogen `anteckningar`.
2.  Skapa en tom fil med namnet `bash_kommandon.md` med kommandot `touch`.
3.  Använd `echo` och redirection (`>`) för att lägga till en rubrik i filen:
    ```bash
    echo "# Bash Kommandon" > bash_kommandon.md
    ```
4.  Använd `cat` för att verifiera att texten finns i filen.
5.  Använd `echo` och append (`>>`) för att lägga till ett kommando på en ny rad:
    ```bash
    echo "- ls: Lista filer" >> bash_kommandon.md
    ```
6.  Kopiera `bash_kommandon.md` till en ny fil `backup_anteckningar.md`.
7.  Byt namn på `backup_anteckningar.md` till `gamla_anteckningar.md` med `mv`.
8.  Ta bort `gamla_anteckningar.md` med `rm`.
9.  Gå upp en nivå (`cd ..`) och ta bort den tomma `skript`-katalogen med `rmdir`.

---

### Övning 3: Sökning och pipes
1.  Gå till din `projekt1`-katalog.
2.  Skapa en loggfil: `touch app.log`
3.  Lägg till flera rader i loggfilen (kör varje rad separat):
    ```bash
    echo "INFO: Applikationen startad" >> app.log
    echo "DEBUG: Ansluter till databas" >> app.log
    echo "ERROR: Kunde inte hitta användare 123" >> app.log
    echo "INFO: Operation slutförd" >> app.log
    echo "WARNING: Diskutrymme nästan fullt" >> app.log
    ```
4.  Använd `grep` för att hitta raden som innehåller "ERROR".
5.  Använd `cat` och en pipe (`|`) för att göra samma sak: `cat app.log | grep "ERROR"`
6.  Lista alla filer i din hemkatalog (`~`) och använd en pipe för att hitta alla rader som innehåller namnet på din `data_engineering_kurs`-katalog. (Tips: `ls -la ~ | grep "data_engineering_kurs"`)

---

### Övning 4: Ett enkelt skript
1.  Se till att du står i `data_engineering_kurs`-katalogen.
2.  Skapa en fil som heter `setup_projekt.sh`: `touch setup_projekt.sh`
3.  Öppna filen i en textredigerare (t.ex. `nano setup_projekt.sh` eller öppna den från VS Code) och klistra in följande:
    ```bash
    #!/bin/bash
    # Ett skript för att skapa en standard projektstruktur

    echo "Skapar projektstruktur..."
    mkdir -p nytt_projekt/src nytt_projekt/data nytt_projekt/tests

    touch nytt_projekt/README.md
    touch nytt_projekt/src/main.py
    touch nytt_projekt/data/raw_data.csv

    echo "Projekt 'nytt_projekt' har skapats!"
    ls -R nytt_projekt
    ```
4.  Spara och stäng filen.
5.  Gör skriptet körbart: `chmod +x setup_projekt.sh`
6.  Kör skriptet: `./setup_projekt.sh`
7.  Verifiera att den nya katalogstrukturen har skapats. Grattis, du har skapat och kört ditt första Bash-skript!

---

### Övning 5: Processhantering och systemövervakning
1.  Visa aktiva processer på ditt system:
    ```bash
    # Lista alla processer
    ps aux
    
    # Visa bara processer som innehåller "bash"
    ps aux | grep bash
    
    # Realtid-övervakning (tryck 'q' för att avsluta)
    top
    ```
2.  Skapa en enkel loggfil som ständigt uppdateras:
    ```bash
    cd data_engineering_kurs
    
    # Skapa ett skript som simulerar en applikation
    echo '#!/bin/bash' > app_simulator.sh
    echo 'while true; do' >> app_simulator.sh
    echo '  echo "$(date): App is running, processing data..." >> app.log' >> app_simulator.sh
    echo '  sleep 2' >> app_simulator.sh
    echo 'done' >> app_simulator.sh
    
    chmod +x app_simulator.sh
    ```
3.  Kör applikationen i bakgrunden och övervaka:
    ```bash
    # Starta i bakgrunden
    ./app_simulator.sh &
    
    # Visa background jobs
    jobs
    
    # Följ loggfilen live (öppna ny terminal eller använd Ctrl+C för att avsluta)
    tail -f app.log
    ```
4.  Stoppa processen:
    ```bash
    # Hitta process-ID
    ps aux | grep app_simulator
    
    # Stoppa med job-nummer (eller kill PID)
    kill %1
    
    # Verifiera att den stoppat
    jobs
    ```

---