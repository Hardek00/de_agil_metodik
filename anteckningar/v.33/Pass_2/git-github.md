# Git & GitHub: Versionshantering och Samarbete

## Mål
Efter denna lektion ska du kunna:
- Hantera kodversioner lokalt med **Git**.
- Samarbeta och lagra kod i molnet med **GitHub**.
- Förstå grundläggande Git-arbetsflöde och GitHub-samarbete.

---

## 1. Git: Din lokala tidsmaskin

### Vad är Git?
Git är ett **distribuerat versionshanteringssystem**. Det är ett verktyg som körs på din lokala dator för att spåra ändringar i dina filer över tid.

**Varför är det viktigt?**
- **Ångra misstag:** Du kan backa till vilken tidigare version som helst av din kod.
- **Experimentera säkert:** Skapa "grenar" (branches) för att testa nya idéer utan att förstöra det som fungerar.
- **Förstå historik:** Se exakt vem som ändrade vad, när och varför.

### Kärnkoncept
- **Repository (Repo):** En mapp som Git "tittar" på. Hela projektet och dess historik.
- **Staging Area:** Ett mellanområde där du förbereder de ändringar du vill spara.
- **Commit:** En "ögonblicksbild" av dina filer. En sparad punkt i historiken.
- **Branch:** En oberoende utvecklingslinje. Huvudlinjen heter oftast `main` (tidigare `master`).

### Viktiga kommandon
| Kommando | Beskrivning |
|---|---|
| `git init` | Initierar ett nytt Git-repository i den nuvarande mappen. |
| `git status` | Visar status för dina filer (ändrade, o-trackade, etc.). |
| `git add <fil>` | Lägger till en fil i Staging Area. (`git add .` för alla) |
| `git commit -m "Meddelande"` | Skapar en commit med ändringarna från Staging Area. |
| `git log` | Visar en logg över alla commits. |
| `git log --oneline` | Kompakt vy av commit-historik. |
| `git branch <namn>` | Skapar en ny branch. |
| `git checkout <namn>` | Byter till en annan branch. |
| `git checkout -b <namn>` | Skapar och byter till en ny branch. |
| `git merge <namn>` | Slår ihop en annan branch med din nuvarande branch. |

### Grundläggande arbetsflöde
```
1. Ändra filer → 2. git add . → 3. git commit -m "Beskrivning" → 4. Upprepa
```

---

## 2. GitHub: Ditt projekts hem i molnet

### Vad är GitHub?
GitHub är en **webbplattform** som hostar Git-repositories. Det är en social plattform för kod.

**Varför är det viktigt?**
- **Samarbete:** Flera personer kan arbeta på samma projekt.
- **Backup:** Din kod är säkert lagrad i molnet.
- **Portfolio:** Visa upp dina projekt för framtida arbetsgivare.
- **CI/CD & Automation:** Starta automatiska tester och deployments (t.ex. GitHub Actions).

### Kärnkoncept
- **Remote:** En koppling till ett repository på en annan plats (som GitHub). Standardnamnet är `origin`.
- **Push:** Skicka dina lokala commits till ett remote repository.
- **Pull:** Hämta ändringar från ett remote repository och slå ihop dem med din lokala branch.
- **Clone:** Skapa en lokal kopia av ett repository från GitHub.
- **Pull Request (PR):** En förfrågan om att slå ihop dina ändringar från en branch till en annan (oftast `main`). Detta är kärnan i samarbetet, där andra kan granska din kod innan den går in i huvudprojektet.
- **Fork:** Skapa din egen kopia av någon annans repository på GitHub (i ditt eget GitHub-konto).

### Fork vs Clone: När används vilket?

**Clone** = Kopiera repo till din dator (lokal kopia)
- Använd när: Du har skriv-åtkomst till repot (ditt eget eller du är collaborator)
- Resultat: Lokal mapp på din dator som är länkad till original-repot
- Exempel: Klona ditt eget projekt eller företagets repo där du jobbar

**Fork** = Skapa din egen kopia på GitHub (remote kopia)
- Använd när: Du vill bidra till någon annans öppna projekt (open source)
- Resultat: En kopia av repot i ditt GitHub-konto som du kan ändra fritt
- Workflow: Fork → Clone din fork → Gör ändringar → PR tillbaka till original

**Kombinerat exempel:**
1. Fork ett open source-projekt (skapar `ditt-användarnamn/projekt`)
2. Clone din fork lokalt (`git clone git@github.com:ditt-användarnamn/projekt.git`)
3. Gör ändringar och push till din fork
4. Skapa PR från din fork till original-projektet

### Viktiga kommandon
| Kommando | Beskrivning |
|---|---|
| `git clone <url>` | Laddar ner ett repository från GitHub till din dator. |
| `git remote add origin <url>` | Lägger till en koppling till ett GitHub-repo. |
| `git remote -v` | Visar alla remote-anslutningar. |
| `git push origin <branch>` | Skickar din branch till GitHub. |
| `git push -u origin <branch>` | Skickar och sätter upstream (första gången). |
| `git pull origin <branch>` | Hämtar och slår ihop ändringar från GitHub. |
| `git fetch` | Hämtar ändringar utan att slå ihop dem. |
| `git fetch origin` | Hämtar alla branches och uppdateringar från remote. |

### Komplett samarbetsflöde med Pull Requests

#### Scenario 1: Ditt eget projekt eller team-projekt
```bash
# 1. Klona och gå till main
git clone git@github.com:username/projekt.git
cd projekt
git checkout main

# 2. Skapa feature-branch
git checkout -b feature/ny-funktion

# 3. Gör ändringar och commita
# ... ändra filer ...
git add .
git commit -m "Implementera ny funktion"

# 4. Push feature-branch
git push -u origin feature/ny-funktion

# 5. Skapa Pull Request på GitHub
# (via webbgränssnittet: Compare & pull request)

# 6. Efter merge - rensa upp lokalt
git checkout main
git pull origin main          # Hämta den mergade koden
git branch -d feature/ny-funktion  # Ta bort lokal branch
git push origin --delete feature/ny-funktion  # Ta bort remote branch (valfritt)
```

#### Scenario 2: Open source-bidrag (fork workflow)
```bash
# 1. Fork projektet på GitHub (via webbgränssnittet)

# 2. Klona din fork
git clone git@github.com:ditt-användarnamn/projekt.git
cd projekt

# 3. Lägg till original som "upstream"
git remote add upstream git@github.com:original-ägare/projekt.git
git remote -v  # Verifiera: origin (din fork), upstream (original)

# 4. Skapa feature-branch
git checkout -b feature/min-förbättring

# 5. Gör ändringar och commita
git add .
git commit -m "Fixa bug i komponenten"

# 6. Push till din fork
git push -u origin feature/min-förbättring

# 7. Skapa PR från din fork till original-repo på GitHub

# 8. Efter merge i original-repo - synka din fork
git checkout main
git pull upstream main      # Hämta senaste från original
git push origin main        # Uppdatera din fork
git branch -d feature/min-förbättring  # Rensa lokal branch
```

#### Varför gå tillbaka till main efter merge?
- **Synka med senaste:** Andra kan ha mergat sina PRs medan du jobbade
- **Ren utgångspunkt:** Nästa feature-branch börjar från uppdaterad main
- **Undvik konflikter:** Minska risk för merge-konflikter i framtida branches
- **Rensa upp:** Ta bort gamla feature-branches som inte längre behövs

### GitHub vs Git
- **Git** = Verktyget (lokalt på din dator)
- **GitHub** = Tjänsten (molnplattform för Git-repos)
- **Alternativ till GitHub:** GitLab, Bitbucket, Azure DevOps

### Användbara GitHub-funktioner
- **Issues:** Spåra buggar och feature-requests
- **Projects:** Kanban-boards för projekthantering
- **Actions:** CI/CD-pipelines
- **Pages:** Hostar statiska webbsidor gratis
- **Releases:** Versionshantering med taggar

### HTTPS vs SSH för GitHub
- **HTTPS:** `https://github.com/user/repo.git` (kräver token/lösenord)
- **SSH:** `git@github.com:user/repo.git` (kräver SSH-nycklar, smidigare)

För SSH-setup, se separat guide: `ssh-guide.md`

---

## 3. Vanliga situationer och lösningar

### Ångra ändringar
```bash
git checkout -- <fil>          # Ångra ocommittade ändringar i fil
git reset HEAD~1                # Ångra senaste commit (behåll ändringar)
git reset --hard HEAD~1         # Ångra senaste commit (ta bort ändringar)
```

### Fetch vs Pull: Viktiga skillnader

**`git pull` = `git fetch` + `git merge`**

#### Git Fetch: "Kolla läget utan att ändra"
```bash
git fetch origin          # Hämta alla uppdateringar från remote
git fetch origin main     # Hämta bara main-branch
```

**Vad händer vid fetch:**
- Laddar ner nya commits från GitHub
- Uppdaterar remote-tracking branches (`origin/main`, `origin/feature-branch`)
- **Ändrar INTE din lokala arbetskopia eller nuvarande branch**
- Du kan inspektera ändringar innan du bestämmer dig för att slå ihop

**När använder man fetch:**
- **Innan du börjar jobba:** Se vad som hänt medan du var borta
- **Innan merge/rebase:** Kontrollera vad som kommer att slås ihop
- **I automatiserade scripts:** Hämta data utan att påverka arbetskopian
- **När du är osäker:** "Låt mig kolla vad som finns innan jag ändrar något"

#### Praktiskt exempel - fetch först, sedan merge:
```bash
# 1. Kolla vad som hänt på main
git fetch origin
git log --oneline main..origin/main    # Visa nya commits

# 2. Om det ser bra ut, slå ihop
git checkout main
git merge origin/main

# Eller använd pull direkt (gör samma sak)
git pull origin main
```

#### När är fetch extra användbart:
```bash
# Scenario 1: Kolla om din feature-branch konfliktar med main
git fetch origin
git checkout feature/min-branch
git merge origin/main    # Testa merge lokalt innan PR

# Scenario 2: Se alla nya branches som teamet skapat
git fetch origin
git branch -r            # Lista alla remote branches

# Scenario 3: Inspektera någon annans branch innan checkout
git fetch origin
git log origin/feature/andras-branch --oneline
git checkout origin/feature/andras-branch  # Read-only kolla
```

### Hantera merge-konflikter
1. Git pausar merge när konflikter uppstår
2. Öppna konfliktfilerna och välj vilken kod som ska behållas
3. `git add .` och `git commit` för att slutföra merge

### .gitignore
Skapa en `.gitignore`-fil för att undvika att committa oönskade filer:
```
# Python
__pycache__/
*.pyc
.venv/
.env

# Editor
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
```

## Sammanfattning

**Git** ger dig lokal versionskontroll – som en "undo"-funktion för hela projekt.
**GitHub** ger dig molnlagring och samarbetsverktyg för dina Git-repositories.

**Grundflöde:**
1. `git clone` eller `git init` → Starta
2. Ändra kod → `git add .` → `git commit -m "..."` → Spara lokalt
3. `git push` → Dela med världen via GitHub
4. `git pull` → Hämta andras ändringar

**För säker anslutning till GitHub, använd SSH-nycklar** (se `ssh-guide.md`).
