# SSH: Säker anslutning till fjärrsystem

## Mål
Efter denna guide ska du kunna:
- Förstå vad SSH är och varför det behövs.
- Skapa och hantera SSH-nycklar.
- Ansluta säkert till GitHub via SSH.
- Ansluta till fjärrservrar (t.ex. molnservrar).

---

## Vad är SSH?

SSH (Secure SHell) är ett protokoll för att skapa en **säker, krypterad anslutning** mellan två datorer över ett osäkert nätverk.

**Varför är det viktigt för oss?**
1. **Säker GitHub-autentisering:** Istället för att skriva lösenord/token varje gång du `push`ar, använder du ett SSH-nyckelpar. Det är säkrare och smidigare.
2. **Serveradministration:** När du ska ansluta till en virtuell maskin i Google Cloud (eller annan molnleverantör) använder du SSH.

---

## Hur SSH-nycklar fungerar

Du skapar ett **nyckelpar**:
- **Privat nyckel (`id_rsa`):** Denna håller du **hemlig** på din dator. Den är som ditt pass.
- **Publik nyckel (`id_rsa.pub`):** Denna kan du ge till andra system (som GitHub eller en GCP-server). Den är som ett visum som du klistrar in i ett annat lands system.

När du ansluter, använder systemet din publika nyckel för att verifiera att du äger den matchande privata nyckeln, utan att den privata nyckeln någonsin lämnar din dator.

**Fördelar:**
- **Säkrare:** Ingen risk att lösenord avlyssnas eller läcker.
- **Smidigare:** Inget lösenord att komma ihåg eller skriva varje gång.
- **Flexibelt:** En nyckel kan ge åtkomst till flera system.

---

## SSH-Agent: Din nyckelhanterare

**SSH-agent** är en bakgrundsprocess som håller dina SSH-nycklar i minnet så du inte behöver skriva lösenord varje gång.

```bash
# Starta SSH-agent
eval "$(ssh-agent -s)"
# Startar agent och sätter miljövariabler så andra kommandon kan hitta den

# Lägg till din privata nyckel till agenten
ssh-add ~/.ssh/id_rsa
# Laddar din privata nyckel i minnet

# Lägg till en specifik nyckel (om du har flera)
ssh-add ~/.ssh/hardek_github
# Laddar en nyckel med anpassat namn
```

**Varför behövs detta?**
- **Bekvämlighet:** Skriv lösenord EN gång, inte vid varje git push
- **Säkerhet:** Nyckeln hålls säkert i minnet, inte på disk
- **Flera nycklar:** Hantera olika nycklar för olika tjänster

---

## SSH-setup för GitHub

### Steg 1: Skapa SSH-nyckelpar
```bash
# Generera nyckelpar med din email
ssh-keygen -t rsa -b 4096 -C "din.email@example.com"

# När du tillfrågas:
# - Filnamn: Tryck Enter för default (id_rsa) eller ange eget namn
# - Lösenord: Valfritt, men rekommenderat för extra säkerhet
```

### Steg 2: Starta SSH-agent och lägg till nyckel
```bash
# Starta SSH-agent
eval "$(ssh-agent -s)"

# Lägg till nyckeln
ssh-add ~/.ssh/id_rsa
# (eller ssh-add ~/.ssh/ditt_filnamn om du valde annat namn)
```

### Steg 3: Kopiera publik nyckel till GitHub
```bash
# Visa din publika nyckel
cat ~/.ssh/id_rsa.pub

# Kopiera hela outputen (börjar med ssh-rsa...)
```

1. Gå till GitHub.com → Settings → SSH and GPG keys
2. Klicka "New SSH key"
3. Klistra in din publika nyckel
4. Ge den ett beskrivande namn (t.ex. "Min laptop")

### Steg 4: Testa anslutningen
```bash
# Testa SSH-anslutning till GitHub
ssh -T git@github.com

# Förväntat svar:
# "Hi username! You've successfully authenticated, but GitHub does not provide shell access."
```

### Steg 5: Använd SSH för Git-operationer
```bash
# Klona med SSH (nya projekt)
git clone git@github.com:username/repository.git

# Ändra befintligt repo från HTTPS till SSH
git remote set-url origin git@github.com:username/repository.git

# Verifiera att det ändrades
git remote -v
```

---

## Skillnad: HTTPS vs SSH för GitHub

**HTTPS (med token):**
```bash
git clone https://github.com/username/repo.git
git remote set-url origin https://github.com/username/repo.git
```
- Kräver GitHub Personal Access Token eller lösenord
- Måste ange credentials vid varje push/pull

**SSH (med nycklar):**
```bash
git clone git@github.com:username/repo.git
git remote set-url origin git@github.com:username/repo.git
```
- Använder SSH-nycklar för autentisering
- Ingen inmatning efter initial setup
- Säkrare och smidigare

---

## SSH för serveranslutning

### Anslut till fjärrserver
```bash
# Grundläggande anslutning
ssh username@server-ip

# Exempel
ssh ubuntu@35.123.456.789

# Med specifik nyckel
ssh -i ~/.ssh/my_server_key ubuntu@35.123.456.789

# Med specifik port
ssh -p 2222 username@server-ip
```

### Skapa SSH-nyckel för server
```bash
# Skapa nyckel specifikt för en server
ssh-keygen -t rsa -b 4096 -C "server-access" -f ~/.ssh/my_server_key

# Kopiera publik nyckel till server (om du har lösenordsåtkomst)
ssh-copy-id -i ~/.ssh/my_server_key.pub username@server-ip

# Eller manuellt: kopiera innehållet i my_server_key.pub 
# till ~/.ssh/authorized_keys på servern
```

---

## Hantera flera SSH-nycklar

### SSH Config-fil
Skapa `~/.ssh/config` för att hantera flera anslutningar:

```
# GitHub
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa

# Produktionsserver
Host prod-server
    HostName 35.123.456.789
    User ubuntu
    IdentityFile ~/.ssh/prod_key
    Port 22

# Utvecklingsserver  
Host dev-server
    HostName dev.example.com
    User developer
    IdentityFile ~/.ssh/dev_key
    Port 2222
```

Användning:
```bash
git clone git@github.com:username/repo.git  # Använder github.com-config
ssh prod-server                             # Ansluter till prod med rätt nyckel
ssh dev-server                              # Ansluter till dev med rätt nyckel
```

---

## Felsökning SSH

### Kontrollera SSH-agent och nycklar
```bash
# Lista alla nycklar i SSH-agent
ssh-add -l

# Ta bort alla nycklar från agent
ssh-add -D

# Lägg till nyckel igen
ssh-add ~/.ssh/id_rsa
```

### Debugga SSH-anslutning
```bash
# Detaljerad output för felsökning
ssh -T -v git@github.com

# Ännu mer detaljerad output
ssh -T -vv git@github.com

# Testa specifik nyckel
ssh -T -i ~/.ssh/specific_key git@github.com
```

### Vanliga problem och lösningar

**Problem:** `Permission denied (publickey)`
**Lösning:**
- Kontrollera att nyckeln är laddad: `ssh-add -l`
- Lägg till nyckel: `ssh-add ~/.ssh/id_rsa`
- Verifiera att publik nyckel är korrekt tillagd på GitHub

**Problem:** `Bad permissions` på nyckelfiler
**Lösning:**
```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

**Problem:** SSH-agent startar inte automatiskt
**Lösning:** Lägg till i `~/.bashrc` eller `~/.zshrc`:
```bash
# Auto-start SSH agent
if [ -z "$SSH_AUTH_SOCK" ] ; then
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
fi
```

---

## Viktiga kommandon - Sammanfattning

| Kommando | Beskrivning |
|---|---|
| `ssh-keygen -t rsa -b 4096 -C "email"` | Genererar nytt SSH-nyckelpar |
| `eval "$(ssh-agent -s)"` | Startar SSH-agent |
| `ssh-add ~/.ssh/id_rsa` | Laddar privat nyckel i SSH-agent |
| `ssh-add -l` | Listar alla nycklar i agent |
| `cat ~/.ssh/id_rsa.pub` | Visar publik nyckel för kopiering |
| `ssh -T git@github.com` | Testar SSH-anslutning till GitHub |
| `ssh username@hostname` | Ansluter till fjärrserver |
| `ssh-copy-id -i ~/.ssh/key.pub user@host` | Kopierar publik nyckel till server |

---

## Säkerhetsrekommendationer

1. **Använd starka lösenord** på dina privata nycklar
2. **Håll privata nycklar hemliga** - dela ALDRIG din `id_rsa`-fil
3. **Rotera nycklar regelbundet** (årligen i företagsmiljö)
4. **Använd olika nycklar** för olika ändamål (GitHub, servrar, etc.)
5. **Backup av nycklar** - men lagra säkert (krypterat)
6. **Ta bort gamla nycklar** från GitHub/servrar när de inte används

SSH ger dig säker, bekväm åtkomst till både GitHub och fjärrservrar - en essentiell färdighet för alla utvecklare!
