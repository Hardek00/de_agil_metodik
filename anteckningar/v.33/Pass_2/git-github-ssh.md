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

### SSH-Agent: Din nyckelhanterare

**SSH-agent** är en bakgrundsprocess som håller dina SSH-nycklar i minnet så du inte behöver skriva lösenord varje gång.

```bash
# Starta SSH-agent
eval "$(ssh-agent -s)"
# Startar agent och sätter miljövariabler så andra kommandon kan hitta den

# Lägg till din privata nyckel till agenten
ssh-add ~/.ssh/id_rsa
# Laddar din privata nyckel i minnet

# Lägg till en specifik nyckel (om du har flera)
ssh-add ~/.ssh/hardek
# Laddar en nyckel med custom namn
```

**Varför behövs detta?**
- **Bekvämlighet:** Skriv lösenord EN gång, inte vid varje git push
- **Säkerhet:** Nyckeln hålls säkert i minnet, inte på disk
- **Flera nycklar:** Hantera olika nycklar för olika tjänster

### GitHub SSH vs HTTPS

När du använder GitHub kan du ansluta på två sätt:

**HTTPS (med token):**
```bash
git clone https://github.com/Hardek00/mitt-repo.git
git remote set-url origin https://github.com/Hardek00/mitt-repo.git
```

**SSH (med nycklar):**
```bash
git clone git@github.com:Hardek00/mitt-repo.git
git remote set-url origin git@github.com:Hardek00/mitt-repo.git
```

**Skillnaden:**
- **`https://`** → Använder lösenord/token varje gång
- **`git@github.com:`** → Använder SSH-nycklar (smidigare)

### Komplett SSH-setup för GitHub

```bash
# 1. Generera nyckelpar
ssh-keygen -t rsa -b 4096 -C "din.email@example.com"
# Välj filnamn (tryck Enter för default) och lösenord

# 2. Starta SSH-agent
eval "$(ssh-agent -s)"

# 3. Lägg till nyckeln
ssh-add ~/.ssh/id_rsa

# 4. Kopiera publika nyckeln
cat ~/.ssh/id_rsa.pub
# Kopiera output och klistra in på GitHub → Settings → SSH Keys

# 5. Testa anslutningen
ssh -T git@github.com
# Ska svara: "Hi username! You've successfully authenticated..."

# 6. Ändra remote till SSH (om repo redan finns)
git remote set-url origin git@github.com:username/repo-namn.git
```

### Felsökning SSH

```bash
# Lista alla nycklar i SSH-agent
ssh-add -l

# Ta bort alla nycklar från agent
ssh-add -D

# Debugga SSH-anslutning
ssh -T -v git@github.com
# Visar detaljerad output för felsökning

# Kontrollera vilken nyckel som används
ssh-add -l | grep hardek
```

### Viktiga kommandon - Utökad
| Kommando | Beskrivning |
|---|---|
| `ssh-keygen -t rsa -b 4096` | Genererar ett nytt SSH-nyckelpar med 4096-bit kryptering. |
| `eval "$(ssh-agent -s)"` | Startar SSH-agent och sätter miljövariabler. |
| `ssh-add ~/.ssh/id_rsa` | Laddar privat nyckel i SSH-agent. |
| `ssh-add -l` | Listar alla nycklar som är laddade i agent. |
| `cat ~/.ssh/id_rsa.pub` | Visar din publika nyckel för kopiering. |
| `ssh -T git@github.com` | Testar SSH-anslutning till GitHub. |
| `git remote set-url origin git@github.com:user/repo.git` | Ändrar remote URL till SSH-format. |
| `ssh user@hostname` | Ansluter till en fjärrserver. |

---

