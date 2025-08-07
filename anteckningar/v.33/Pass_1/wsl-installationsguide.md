# Guide: Installera WSL på Windows

WSL (Windows Subsystem for Linux) låter dig köra en komplett Linux-miljö direkt på Windows, utan behov av traditionella virtuella maskiner eller dual boot.

## Systemkrav
-   **Windows 10 version 2004 (Build 19041) eller senare**
-   **Windows 11 (alla versioner)**
-   64-bitars processor med virtualiseringsstöd (standard på moderna datorer).
-   Minst 4 GB RAM (8 GB rekommenderas).

---

## Steg 1: Snabbinstallation (Rekommenderad metod)

För de flesta moderna system är detta det enda kommandot du behöver. Det hanterar alla nödvändiga steg automatiskt.

1.  **Öppna PowerShell som Administratör:**
    -   Högerklicka på Start-menyn och välj "Terminal (Admin)" eller "Windows PowerShell (Admin)".

2.  **Kör installationskommandot:**
    ```powershell
    wsl --install
    ```
    Detta kommando kommer att:
    -   Aktivera nödvändiga Windows-funktioner (WSL och Virtual Machine Platform).
    -   Ladda ner och installera den senaste Linux-kärnan.
    -   Installera **Ubuntu** som din standard-distribution.
    -   Sätta WSL2 som standard.

3.  **Starta om datorn:**
    När kommandot är klart, starta om din dator för att slutföra installationen.

4.  **Konfigurera din Linux-distribution:**
    Efter omstart, öppna **Ubuntu** från Start-menyn. Första gången det startar kommer du att behöva:
    -   Skapa ett **användarnamn** (t.ex. `anna`).
    -   Skapa ett **lösenord**.
    *Detta är ditt Linux-konto och är helt separat från ditt Windows-konto.*

Gå sedan till **"Steg 2: Verifiera din installation"** nedan.

---

## Felsökning: Manuell installation

Använd endast dessa steg om `wsl --install` misslyckas eller om du vill ha mer detaljerad kontroll över processen.

### Steg 1.1: Aktivera WSL-funktioner manuellt
Öppna PowerShell som administratör och kör följande två kommandon:
```powershell
# Aktiverar själva WSL-funktionen
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Aktiverar funktionen för virtuella maskiner
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
Starta om datorn efter detta.

### Steg 1.2: Installera WSL2 Kernel Update
Om du får ett felmeddelande om att "WSL 2 requires an update to its kernel component", ladda ner och installera uppdateringen manuellt.
-   **Länk:** [WSL2 Linux kernel update package for x64 machines](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi)
-   Kör den nedladdade `.msi`-filen och följ installationsanvisningarna.

### Steg 1.3: Sätt WSL2 som standardversion
Detta säkerställer att alla framtida Linux-distributioner installeras med den modernare och mer högpresterande version 2. Kör i PowerShell (som administratör):
```powershell
wsl --set-default-version 2
```

### Steg 1.4: Installera en Linux-distribution
Gå till **Microsoft Store**, sök efter den distribution du vill ha (t.ex. `Ubuntu 22.04 LTS`) och klicka på "Installera". När den är klar, starta den från Start-menyn för att skapa ditt användarnamn och lösenord.

---

## Steg 2: Verifiera din installation

Oavsett vilken installationsmetod du använde, är det bra att verifiera att allt fungerar som det ska.

1.  **Öppna PowerShell eller Terminal.**
2.  **Lista dina installationer:**
    ```powershell
    wsl --list --verbose
    ```
    Outputen bör se ut ungefär så här, där du ser din distribution (t.ex. Ubuntu) med `VERSION` satt till `2`.
    ```
      NAME      STATE           VERSION
    * Ubuntu    Running         2
    ```
3.  **Starta din WSL-miljö:**
    Skriv helt enkelt `wsl` i terminalen. Din prompt bör ändras till en Linux-prompt.
    ```powershell
    PS C:\Users\Anna> wsl
    anna@Datornamn:~$
    ```
    Grattis, du är nu inne i Linux!

---

## Användbara kommandon och vidare steg

### WSL-kommandon (körs från PowerShell/Windows Terminal)
-   `wsl --shutdown`: Stänger av WSL helt. Bra för felsökning.
-   `wsl --update`: Letar efter och installerar uppdateringar till WSL-kärnan.
-   `wsl --status`: Visar generell status för din WSL-konfiguration.
-   `wsl --set-version <distribution> <version>`: Byter version (t.ex. från 1 till 2) för en specifik distribution.

### Nästa steg
Nu när du har en fungerande Linux-miljö kan du:
-   Följa vår **Bash-grundkurs**.
-   Installera utvecklingsverktyg som `git`, `python`, `node`, `docker`.
-   Integrera WSL med Visual Studio Code för en smidig utvecklingsupplevelse. 