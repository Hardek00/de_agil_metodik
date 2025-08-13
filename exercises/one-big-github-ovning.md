Övning: Från WSL‑terminal till GitHub (Python)

Syfte: Träna terminalflöde i WSL/Ubuntu, virtuell miljö, arbeta med ett befintligt repo, skapa egna ändringar och publicera till ett eget GitHub‑repo via SSH.

Du övar på:

- Navigering i terminalen (mkdir, cd)
- Python‑miljöer (venv), pip install, pip freeze
- Git‑grund: status, add, commit, remote, push
- Skapa `.gitignore` för ett Python‑projekt (utan facit)
- Skapa repo på GitHub och pusha via SSH

Förkunskaper/krav:

- WSL + Ubuntu klart, VS Code integrerat med WSL
- Testa SSH: `ssh -T git@github.com`
- `python3 --version`, `git --version`

Steg (kör i WSL/Ubuntu):

1) Skapa arbetsmapp och klona repot

- Välj en lämplig plats i din hemkatalog för projekt.
- Klona detta repo via SSH och gå in i projektmappen: `git@github.com:Hardek00/one_big_github_ovning.git`.
- Kontrollera att du har en ren arbetsyta och att fjärren pekar rätt.

2) Skapa och aktivera virtuell miljö, installera beroenden

- Skapa en virtuell miljö i projektet och aktivera den.
- Kontrollera Python‑versionen i miljön.
- Installera beroenden om det finns en `requirements.txt`.

3) Prova starta/validera koden
- Kör projektet eller dess tester och notera eventuella fel.

4) Skapa en `.gitignore` för detta Python‑projekt (utan facit)

- Utgå från vilka filer/mappar som inte ska versionshanteras i ett typiskt Python‑projekt.
- Tänk i kategorier: temporära/kompilerade artefakter, cache, lokala miljömappar, editor‑metadata, hemligheter/konfiguration.
- Verifiera med `git status` att oönskade filer inte längre är otrackade.
- Tips: GitHub har språk‑specifika `.gitignore`‑mallar som referens (använd gärna som inspiration, men skriv din egen).

5) Gör ändringar i koden (bugfix/feature), och skapa en commit

- Genomför en liten förbättring eller fix.
- Skapa en tydlig, atomisk commit med en meningsfull commit‑text.

6) Skapa nytt GitHub‑repo och pusha via SSH

- Skapa ett tomt repo på GitHub.
- Kontrollera att din SSH‑nyckel fungerar mot GitHub.
- Sätt fjärr (origin) till ditt nya repo, använd `main` som default‑branch och pusha första versionen.

```bash
git remote remove origin || true
git remote add origin git@github.com:<ditt-anv>/<ditt-nya-repo>.git
git branch -M main
git push -u origin main
```

Bonus (branch + PR):

- Skapa en ny feature‑branch, gör en ändring och skapa en PR mot `main` i ditt repo.
- Beskriv syfte, hur man testar och eventuella risker i PR‑beskrivningen.

Klara kriterier:

- Virtuell miljö skapad och använd.
- `.gitignore` skapad och fungerar (oönskade filer trackas inte).
- Kod går att köra eller felsökning dokumenterad.
- Nytt GitHub‑repo skapat och första push genomförd via SSH.
- (Bonus) PR skapad från en feature‑branch.
