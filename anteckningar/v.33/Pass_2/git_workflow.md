# Git/GitHub Workflow – Eget projekt vs. Samarbete

## **EGET PROJEKT**

### Initialt
```bash
git init
# skriv kod
git add .
git commit -m "första commit"
# skapa ett GitHub-repo (tomt) via webben
git remote add origin <URL-till-repot>
git branch -M main    # valfritt, men standard är ofta main
git push -u origin main
```

### Vid fortsatt arbete
```bash
git pull origin main  # hämta ev. ändringar från GitHub
# jobba med kod
git add .
git commit -m "beskrivning av ändring"
git push
```

---

## **COLLAB / TEAM**

### Initialt
```bash
git clone <URL-till-repot>
git checkout -b min-feature-branch   # skapa egen branch från main
# jobba med kod
git add .
git commit -m "beskrivning av ändring"
git push -u origin min-feature-branch
# skapa pull request på GitHub
# när PR är godkänd -> merge till main
```

### Fortsättningsvis
```bash
git checkout main
git pull origin main  # uppdatera din main
git checkout -b ny-feature-branch
```

---

## **Tips & Bra Att Tänka På**
- Använd `git remote add origin` i eget projekt så Git vet var det ska pusha.
- Lägg till `-u` vid första push till en branch: `git push -u origin <branch>`.
- Alltid `git pull` innan du börjar jobba för att undvika konflikter.
- I samarbete: undvik att committa direkt på `main` – jobba via feature-branches och pull requests.
- Vid större team kan `git fetch` + `git merge` eller `git rebase` vara bra för att hålla historiken ren.
