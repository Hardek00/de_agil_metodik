## Övningar

### Övning 1: Ditt första lokala repository
1.  Skapa en ny mapp: `mkdir mitt-första-repo && cd mitt-första-repo`
2.  Initiera ett Git-repository: `git init`
3.  Skapa en fil: `echo "Hello, Git!" > README.md`
4.  Kolla status: `git status` (Du bör se `README.md` som "untracked").
5.  Lägg till filen i Staging Area: `git add README.md`
6.  Kolla status igen: `git status` (Nu är den "staged").
7.  Gör din första commit: `git commit -m "Initial commit: Add README.md"`
8.  Se din historik: `git log`

### Övning 2: Branching & Merging
1.  Skapa en ny branch för att lägga till mer information: `git branch add-description`
2.  Byt till den nya branchen: `git checkout add-description`
3.  Lägg till mer text i din README: `echo "This is my first project with Git." >> README.md`
4.  Staga och committa ändringen: `git add README.md` och `git commit -m "Add project description"`
5.  Byt tillbaka till huvudbranchen: `git checkout main`
6.  Titta på `README.md` (`cat README.md`). Beskrivningen är borta!
7.  Slå ihop din feature-branch: `git merge add-description`
8.  Titta på `README.md` igen. Nu är beskrivningen där!

### Övning 3: Koppla till GitHub (HTTPS-metoden)
1.  Gå till [GitHub](https://github.com) och skapa ett nytt, tomt repository (utan README eller .gitignore).
2.  Kopiera HTTPS-URL:en för ditt nya repository.
3.  I din lokala terminal (i `mitt-första-repo`), lägg till din GitHub-repo som en "remote":
    ```bash
    git remote add origin <klistra-in-din-https-url-här>
    ```
4.  Verifiera att den har lagts till: `git remote -v`
5.  Skicka (`push`) din `main`-branch till GitHub: `git push origin main`
6.  Gå till din repository-sida på GitHub och uppdatera. Dina filer ska nu finnas där!

### Övning 4: SSH-autentisering med GitHub
1.  **Generera en SSH-nyckel** (om du inte redan har en):
    ```bash
    ssh-keygen -t rsa -b 4096 -C "din.email@example.com"
    ```
    Tryck Enter på alla frågor för att acceptera standardvärdena.
2.  **Visa och kopiera din publika nyckel:**
    ```bash
    cat ~/.ssh/id_rsa.pub
    ```
    Markera och kopiera hela outputen (från `ssh-rsa` till slutet).
3.  **Lägg till nyckeln på GitHub:**
    -   Gå till GitHub > Settings > SSH and GPG keys.
    -   Klicka på "New SSH key".
    -   Ge den en titel (t.ex. "Min WSL-dator") och klistra in din nyckel i "Key"-fältet. Spara.
4.  **Klona ditt repo med SSH:**
    -   Gå till din GitHub-repositorysida och klicka på "Code". Välj fliken "SSH" och kopiera URL:en.
    -   Gå till en annan mapp på din dator (`cd ~`).
    -   Klona repot: `git clone <klistra-in-din-ssh-url-här>`
5.  **Testa att pusha:**
    -   Gå in i den nya mappen: `cd mitt-första-repo`
    -   Gör en ändring: `echo "SSH is working!" >> README.md`
    -   Committa: `git add . && git commit -m "Test SSH push"`
    -   Pusha: `git push origin main`. Du bör **inte** behöva ange lösenord!

Grattis! Du har nu en komplett, säker och professionell setup för att hantera kod.

---

### Övning 5: Samarbete i Team (Feature Branch & Pull Request Workflow)

**Mål:** Simulera ett verkligt team-projekt där flera personer bidrar till samma kodbas utan att skapa kaos.

**Grupp:** Denna övning görs i grupper om 2-3 personer.

#### Steg 1: Förberedelser (En person i gruppen gör detta)

1.  **Skapa ett nytt repo:** En person i gruppen (”repo-ägaren”) skapar ett nytt, **publikt** repository på GitHub. Kalla det `team-projekt`. **Viktigt:** Inkludera en `README.md`-fil från start.
2.  **Bjud in medarbetare:**
    -   Gå till `Settings` > `Collaborators`.
    -   Lägg till de andra gruppmedlemmarnas GitHub-användarnamn.
3.  **Alla andra klonar:**
    -   De andra medlemmarna måste acceptera inbjudan (de får ett mail).
    -   **Alla** i gruppen (inklusive ägaren) klonar nu det nya repot till sin lokala dator med SSH: `git clone <ssh-url-till-team-projekt>`

#### Steg 2: Arbetsflödet (Alla i gruppen gör detta för sin egen del)

**Scenario:** Varje person ska lägga till sitt namn och sin favorit-molntjänst i `README.md`.

1.  **Synka alltid först!**
    Innan du börjar arbeta, se till att din lokala `main`-branch är uppdaterad:
    ```bash
    # Se till att du är på main-branchen
    git checkout main

    # Hämta de senaste ändringarna från GitHub
    git pull origin main
    ```

2.  **Skapa en egen branch:**
    Skapa en ny branch för just din ändring. Döp den efter ditt namn och vad du ska göra.
    ```bash
    # Exempel för någon som heter Anna
    git checkout -b anna-adds-profile
    ```

3.  **Gör din ändring:**
    -   Öppna `README.md`.
    -   Lägg till ditt namn och din favorit-molntjänst på en ny rad.
    -   Spara filen.

4.  **Committa din ändring:**
    ```bash
    git add README.md
    git commit -m "feat: Add Anna's profile"
    ```

5.  **Pusha din branch (INTE main!):**
    Skicka upp just *din* branch till GitHub.
    ```bash
    git push origin anna-adds-profile
    ```

#### Steg 3: Pull Request och Kodgranskning

1.  **Skapa en Pull Request (PR):**
    -   Gå till repositoryt på GitHub.
    -   En gul banner kommer föreslå att du skapar en Pull Request från din nya branch. Klicka på den.
    -   Ge din PR en titel (t.ex. "Add Anna's profile") och en kort beskrivning.
    -   Till höger, under "Reviewers", välj en av dina teammedlemmar att granska din kod.
    -   Klicka "Create Pull Request".

2.  **Granska och Godkänn (Teammedlemmen gör detta):**
    -   Den utsedda granskaren får en notis.
    -   Gå till fliken "Pull Requests" i repot.
    -   Klicka på PR:en, gå till "Files Changed" för att se ändringarna.
    -   Om allt ser bra ut, klicka "Review changes" > "Approve" > "Submit review".

3.  **Slå ihop (Merge) PR:en (Den som skapade PR:en gör detta):**
    -   När din PR är godkänd, kommer du se en grön knapp "Merge pull request". Klicka på den och bekräfta.
    -   **Viktigt:** Klicka på "Delete branch" efter att du har mergat. Detta håller repot rent och snyggt.

#### Steg 4: Håll alla synkade

Nu har en ny ändring lagts till i `main`-branchen på GitHub. **Alla i teamet** måste nu uppdatera sin lokala `main`-branch genom att repetera steg 1:
```bash
git checkout main
git pull origin main
```
Nu har alla den senaste versionen av `README.md`, inklusive den nya profilen. Processen upprepas för nästa person som ska lägga till sin profil.

---

### Bonus: Hantera en Merge-konflikt

Vad händer om två personer ändrar på **samma rad**?
1.  **Person A** gör sin ändring på rad 5, skapar en PR och den blir mergad.
2.  **Person B**, som *inte* har kört `git pull`, gör sin ändring på rad 5 på sin branch.
3.  När Person B pushar sin branch och försöker skapa en PR, kommer GitHub att varna för en **merge-konflikt**.
4.  **Lösning (Person B gör detta):**
    -   Synka `main`: `git checkout main` och `git pull origin main`.
    -   Gå tillbaka till din branch: `git checkout <din-branch>`
    -   Försök nu merga `main` *in i din branch*: `git merge main`
    -   Git kommer att misslyckas och meddela att det finns en konflikt. Öppna den konfliktdrabbade filen. Du kommer se:
        ```
        <<<<<<< HEAD
        Din ändring här
        =======
        Ändringen från main-branchen här
        >>>>>>> main
        ```
    -   **Redigera filen manuellt.** Ta bort `<<<`, `===`, `>>>`-markörerna och bestäm vilken kod som ska vara kvar (oftast en kombination av båda).
    -   Spara filen.
    -   Gör en ny commit för att lösa konflikten: `git add .` och `git commit -m "fix: Resolve merge conflict"`
    -   Pusha din branch igen: `git push origin <din-branch>`. Nu ska konflikten vara borta på GitHub! 