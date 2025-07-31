# Git, GitHub & SSH: Grunden för Samarbete och Cloud

## Mål
Efter denna lektion ska du kunna:
-   Hantera kodversioner lokalt med **Git**.
-   Samarbeta och lagra kod i molnet med **GitHub**.
-   Ansluta säkert till fjärrsystem och GitHub med **SSH**.

---

## 1. Git: Din lokala tidsmaskin

### Vad är Git?
Git är ett **distribuerat versionshanteringssystem**. Det är ett verktyg som körs på din lokala dator för att spåra ändringar i dina filer över tid.

**Varför är det viktigt?**
-   **Ångra misstag:** Du kan backa till vilken tidigare version som helst av din kod.
-   **Experimentera säkert:** Skapa "grenar" (branches) för att testa nya idéer utan att förstöra det som fungerar.
-   **Förstå historik:** Se exakt vem som ändrade vad, när och varför.

### Kärnkoncept
-   **Repository (Repo):** En mapp som Git "tittar" på. Hela projektet och dess historik.
-   **Staging Area:** Ett mellanområde där du förbereder de ändringar du vill spara.
-   **Commit:** En "ögonblicksbild" av dina filer. En sparad punkt i historiken.
-   **Branch:** En oberoende utvecklingslinje. Huvudlinjen heter oftast `main` (tidigare `master`).

![Git Staging Area](https://git-scm.com/images/about/areas.png)

### Viktiga kommandon
| Kommando | Beskrivning |
|---|---|
| `git init` | Initierar ett nytt Git-repository i den nuvarande mappen. |
| `git status` | Visar status för dina filer (ändrade, o-trackade, etc.). |
| `git add <fil>` | Lägger till en fil i Staging Area. (`git add .` för alla) |
| `git commit -m "Meddelande"` | Skapar en commit med ändringarna från Staging Area. |
| `git log` | Visar en logg över alla commits. |
| `git branch <namn>` | Skapar en ny branch. |
| `git checkout <namn>` | Byter till en annan branch. (`git checkout -b <namn>` skapar och byter) |
| `git merge <namn>` | Slår ihop en annan branch med din nuvarande branch. |

---

## 2. GitHub: Ditt projekts hem i molnet

### Vad är GitHub?
GitHub är en **webbplattform** som hostar Git-repositories. Det är en social plattform för kod.

**Varför är det viktigt?**
-   **Samarbete:** Flera personer kan arbeta på samma projekt.
-   **Backup:** Din kod är säkert lagrad i molnet.
-   **Portfolio:** Visa upp dina projekt för framtida arbetsgivare.
-   **CI/CD & Automation:** Starta automatiska tester och deployments (t.ex. GitHub Actions).

### Kärnkoncept
-   **Remote:** En koppling till ett repository på en annan plats (som GitHub). Standardnamnet är `origin`.
-   **Push:** Skicka dina lokala commits till ett remote repository.
-   **Pull:** Hämta ändringar från ett remote repository och slå ihop dem med din lokala branch.
-   **Clone:** Skapa en lokal kopia av ett repository från GitHub.
-   **Pull Request (PR):** En förfrågan om att slå ihop dina ändringar från en branch till en annan (oftast `main`). Detta är kärnan i samarbetet, där andra kan granska din kod innan den går in i huvudprojektet.

### Viktiga kommandon
| Kommando | Beskrivning |
|---|---|
| `git clone <url>` | Laddar ner ett repository från GitHub till din dator. |
| `git remote add origin <url>` | Lägger till en koppling till ett GitHub-repo. |
| `git push origin <branch>` | Skickar din branch till GitHub. |
| `git pull origin <branch>` | Hämtar och slår ihop ändringar från GitHub. |

---

## 3. SSH: Din säkra nyckel till molnet

### Vad är SSH?
SSH (Secure SHell) är ett protokoll för att skapa en **säker, krypterad anslutning** mellan två datorer över ett osäkert nätverk.

**Varför är det viktigt för oss?**
1.  **Säker GitHub-autentisering:** Istället för att skriva lösenord/token varje gång du `push`ar, använder du ett SSH-nyckelpar. Det är säkrare och smidigare.
2.  **Serveradministration:** När du ska ansluta till en virtuell maskin i Google Cloud (eller annan molnleverantör) använder du SSH.

### Hur fungerar det?
Du skapar ett **nyckelpar**:
-   **Privat nyckel (`id_rsa`):** Denna håller du **hemlig** på din dator. Den är som ditt pass.
-   **Publik nyckel (`id_rsa.pub`):** Denna kan du ge till andra system (som GitHub eller en GCP-server). Den är som ett visum som du klistrar in i ett annat lands system.

När du ansluter, använder systemet din publika nyckel för att verifiera att du äger den matchande privata nyckeln, utan att den privata nyckeln någonsin lämnar din dator.

### Viktiga kommandon
| Kommando | Beskrivning |
|---|---|
| `ssh-keygen -t rsa -b 4096` | Genererar ett nytt SSH-nyckelpar. |
| `cat ~/.ssh/id_rsa.pub` | Visar din publika nyckel så att du kan kopiera den. |
| `ssh user@hostname` | Ansluter till en fjärrserver. |

---

