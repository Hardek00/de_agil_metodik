# Guide: Integrera WSL med Visual Studio Code

Visual Studio Code har utmärkt stöd för WSL genom WSL-tillägget. Detta gör det möjligt att utveckla direkt i din Linux-miljö från Windows.

## Förutsättningar
- WSL installerat och konfigurerat (se WSL-installationsguiden)
- Visual Studio Code installerat på Windows
- En Linux-distribution installerad (t.ex. Ubuntu)

---

## Steg 1: Installera WSL-tillägget

1. Öppna Visual Studio Code
2. Klicka på Extensions-ikonen i sidopanelen (`Ctrl+Shift+X`)
3. Sök efter "WSL" av Microsoft
4. Klicka "Install" på "WSL" extension av Microsoft

**Tips:** Överväg att installera hela "Remote Development" extension pack från Microsoft. Det inkluderar WSL, SSH och Containers, vilket ger dig en komplett verktygslåda för fjärrutveckling.

---

## Steg 2: Anslut till WSL

Det finns flera sätt att ansluta VS Code till din WSL-miljö:

### Metod 1: Från Command Palette (Rekommenderas)
1. Öppna VS Code.
2. Tryck **`Ctrl+Shift+P`** för att öppna Command Palette.
3. Skriv `WSL: Connect to WSL` och välj det.
4. Ett nytt VS Code-fönster öppnas som kör helt och hållet i din WSL-miljö.

### Metod 2: Från WSL-terminalen
1. Öppna din vanliga WSL-terminal (t.ex. Ubuntu från Start-menyn).
2. Navigera till din projektmapp: `cd /path/to/your/project`
3. Kör kommandot: `code .`
4. VS Code startar automatiskt och ansluter till WSL, med den nuvarande mappen öppen.

### Metod 3: Från Remote Explorer
1. Klicka på Remote Explorer-ikonen i sidopanelen (en grön ikon längst ner till vänster).
2. Under "WSL Targets" ser du dina installerade distributioner.
3. Klicka på anslutningsikonen bredvid din distribution.

---

## Steg 3: Bekräfta WSL-anslutning

När du är korrekt ansluten ser du tydliga indikatorer:

-   **Grön fjärrikon:** Längst ner till vänster i statusfältet ser du en grön ruta där det står `WSL: Ubuntu` (eller din distributions namn).
-   **Terminalen:** När du öppnar den integrerade terminalen (`Ctrl+\``), kommer du se din Linux-prompt (t.ex. `user@datornamn:~$`), inte en PowerShell- eller CMD-prompt.

Kör `uname -a` i terminalen. Om du får en Linux-relaterad output (t.ex. `...Linux...Microsoft...`) är du korrekt ansluten.

---

## Steg 4: Hantera Tillägg (Extensions) i WSL

**Viktigt:** Tillägg måste installeras separat för WSL-miljön. Dina lokala Windows-tillägg kommer inte automatiskt att fungera.

1.  Öppna Extensions-panelen (`Ctrl+Shift+X`).
2.  Du kommer att se två huvudsektioner:
    -   **LOCAL - INSTALLED**: Tillägg installerade på Windows.
    -   **WSL: UBUNTU - INSTALLED**: Tillägg installerade i din WSL-miljö.
3.  För varje tillägg du behöver (t.ex. Python, Docker, GitLens), måste du klicka på den gröna knappen "Install in WSL".

VS Code är oftast smart nog att rekommendera vilka av dina lokala tillägg som bör installeras i WSL när du ansluter första gången.

### Rekommenderade tillägg att installera i WSL:
-   **Python** (Microsoft)
-   **Docker** (Microsoft)
-   **GitLens**
-   **Prettier** (för kodformatering)

---

## Steg 5: Förstå filsystemet

Detta är en vanlig källa till förvirring och prestandaproblem.

### Prestandaregeln
> **Arbeta ALLTID med dina projektfiler inuti WSL:s filsystem för bäst prestanda.**

-   **BRA (Snabbt):** `cd ~/projects` (vilket är samma som `/home/ditt_namn/projects`)
-   **DÅLIGT (Långsamt):** `cd /mnt/c/Users/DittNamn/Documents/projects`

Att redigera filer från WSL som ligger på Windows-disken (`/mnt/c`) är betydligt långsammare.

### Åtkomst till filer
-   **Från Windows till WSL:** Öppna Utforskaren och skriv `\\wsl$` i adressfältet. Där ser du en mapp för din distribution (t.ex. `Ubuntu`) och kan navigera i dess filsystem.
-   **Från WSL till Windows:** Dina Windows-diskar är monterade under `/mnt/`. Din C-disk finns på `/mnt/c/`.

---

## Steg 6: Ett typiskt arbetsflöde

1.  **Starta VS Code och anslut till WSL** med `Ctrl+Shift+P` > "Connect to WSL".
2.  **Öppna en terminal** (`Ctrl+\``). Du är nu i din WSL-hemkatalog.
3.  **Klona ett projekt från GitHub:** `git clone git@github.com:anvandare/repo.git`
4.  **Navigera in i projektet:** `cd repo`
5.  **Öppna projektmappen i VS Code:** `code . -r` (flaggan `-r` återanvänder samma fönster).
6.  **Installera dependencies** med Linux-verktyg: `npm install`, `pip install -r requirements.txt`, etc.
7.  **Kör din applikation:** `npm start`, `python app.py`.
8.  **Port Forwarding:** VS Code vidarebefordrar automatiskt portar. Om din app körs på port 3000 i WSL kan du öppna `http://localhost:3000` i din Windows-webbläsare.

---

## Felsökning

-   **Problem: `code .` fungerar inte i WSL-terminalen.**
    -   **Lösning:** VS Code lägger normalt till sig själv i PATH-variabeln under installationen. Om det misslyckats, se till att du är ansluten till WSL *från VS Code* först. Den fjärranslutningen brukar lösa det.
-   **Problem: Långsam prestanda.**
    -   **Lösning:** Kontrollera att dina projektfiler ligger i WSL:s filsystem (`~/...`) och inte på Windows-disken (`/mnt/c/...`).
-   **Problem: Extensions fungerar inte.**
    -   **Lösning:** Dubbelkolla att du har installerat dem specifikt för WSL (se Steg 4). 