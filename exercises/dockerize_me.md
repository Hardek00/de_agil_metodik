# Övning: Containerisera Python-appar

I denna övning kommer du att klona ett GitHub-repo och containerisera tre enkla Python-appar. Du kommer att använda Docker för att skapa och köra containers för varje app.

## Steg för steg:

1. **Klona GitHub-repot**
   - Öppna en terminal och kör följande kommando för att klona repot:
     ```bash
     git clone https://github.com/Hardek00/containerize_me.git
     ```
   - Navigera in i den klonade mappen:
     ```bash
     cd containerize_me
     ```

2. **Utforska projektstrukturen**
   - Du kommer att se tre mappar: `cli_tool`, `data_processor`, och `web_app`.
   - Varje mapp innehåller en enkel Python-app som du ska containerisera.

3. **Skapa Dockerfile för varje app**
   - För varje mapp, skapa en `Dockerfile`
     ```
     Tips: 
     **Anpassa `CMD`-raden** för att matcha huvudfilen i varje app.

4. **Bygg Docker-images**
   - Bygg en Docker-image för varje app:
     ```bash
     docker build -t cli_tool_image ./cli_tool
     docker build -t data_processor_image ./data_processor
     docker build -t web_app_image ./web_app
     ```

5. **Kör containers**
   - Starta en container för varje app :
     ```bash
     docker run cli_tool_image
     docker run data_processor_image
     docker run -p 8080:8080 web_app_image
     ```

6. **Testa och verifiera**
   - För `web_app`, öppna en webbläsare och navigera till `http://localhost:8080` för att se appen i aktion.
   - För `cli_tool` och `data_processor`, kontrollera terminalutdata för att verifiera att de körs korrekt.

7. **Rensa upp containers**
   - Använd `docker ps -a` för att lista alla containers.
   - Ta bort de stoppade containers med `docker rm <container_id>`.

## Tips och ledtrådar:
- **Kontrollera beroenden**: Se till att alla nödvändiga paket finns i `requirements.txt` för varje app.
- **Portmappning**: För `web_app`, se till att portmappningen i `docker run`-kommandot matchar den port som appen lyssnar på.
- **Utforska Docker**: Använd `docker ps` för att se körande containers och `docker logs` för att felsöka.

Lycka till med containeriseringen! 🚀