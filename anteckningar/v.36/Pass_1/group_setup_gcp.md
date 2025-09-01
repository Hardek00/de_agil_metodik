## Övning: Sätt upp ert GCP‑projekt (Grupp)

### Syfte
Lägga en stabil grund i GCP för ert kursprojekt: projekt, budget, IAM, servicekonto, och ett BigQuery‑dataset. Ingen kod/CI i denna övning.

### Förutsättningar
- Google‑konton (alla i teamet)
- En person utpekad som Project Owner (även ansvarig för billing)
- Lokalt: Git, Docker, WSL
- Läs: `anteckningar/v.35/Pass_1/iam.md` (IAM‑grunder) och `anteckningar/v.35/Pass_2/collab_in_gcp.md` (samarbetsguide)


### Output (minimal dokumentation i repo under `docs/team-setup/`)
- `project_info.md` (Project ID, region, ägare, teamlista)
- `access.md` (vilka roller vem har och på vilken nivå)
- `bq_setup.md` (vilket dataset skapades och i vilken region)

### Steg
1) Projekt och budget (Project Owner)
- Skapa GCP‑projekt (namn: `team_<grupp>_<kortnamn>`). Notera `PROJECT_ID`.
- Koppla billing. Sätt budget + alerts: 25%, 50%, 75%, 90% till teamets e‑post.

2) IAM och åtkomst
- Skapa en Google‑grupp för teamet (om möjligt). Alternativt lista medlemmar.
- Tilldela roller enligt least privilege:
  - 1–2 personer: `roles/owner` (tillfälligt; minska efter setup)
  - Utvecklare: BigQuery Job User + Data Editor (på projekt eller dataset‑nivå)
  - Läsare/observatörer: Viewer/Data Viewer
- Dokumentera i `access.md` vilka roller tilldelats och på vilken nivå (projekt/dataset).
- Referens: se `iam.md` och "Best practices" i `collab_in_gcp.md`.

3) Servicekonto (SA=service account) och nycklar (se filen `service_account.md` )
- Vem gör vad (övertydligt):
  1. Project Owner skapar servicekontot i projektet: `ingest-sa@<PROJECT_ID>.iam.gserviceaccount.com`.
  2. Project Owner tilldelar behörigheter till servicekontot (inte till personer): minst `roles/bigquery.jobUser` och `roles/bigquery.dataEditor` på projektet eller dataset‑nivå. .
  3. Project Owner väljer användningsmodell:
     - Modell A – med nyckel (rekommenderas för kursen nu): generera EN nyckel för servicekontot, dela säkert till teamet. Varje medlem sparar lokalt som `service-account-key.json`. Ingen extra IAM‑tilldelning till individer krävs för att använda nyckeln – rättigheterna ligger på SA:t.
     - Modell B – utan nyckel (avancerat): tilldela utvecklare rollen `roles/iam.serviceAccountTokenCreator` på servicekontot så att de kan agera som ("impersonera") SA:t med sin egen inloggning. Detta är valfritt och ingår inte i denna övning.
- Skapa nyckel endast om ni valt Modell A. Lagra nyckeln lokalt – aldrig i Git.
- Lägg till/uppdatera `.gitignore` med:
```gitignore
service-account-key.json
.env
```
  (Skriv i `access.md` vem som förvarar nyckeln lokalt; detaljerad rotation tas i senare pass.)

4) BigQuery‑setup
- Skapa ETT dataset med team‑prefix, t.ex.: `team_<grupp>_raw`
- Välj region (t.ex. `EU`) och dokumentera i `bq_setup.md`.


6) Repo (minimalt)
- Lägg bara in `docs/team-setup/` och fyll `project_info.md`, `access.md`, `bq_setup.md`.


8) Verifiera (checklista)
- IAM:
  - [ ] Alla i teamet har åtkomst enligt plan
  - [ ] Minst en utvecklare utan Owner kan starta BQ‑jobb
- SA:
  - [ ] `service-account-key.json` finns lokalt (om använt) och är o‑committad
  - [ ] `.env` funkar lokalt
- BQ:
  - [ ] Datasets finns i rätt region och är åtkomliga
  - [ ] Ett testjobb (t.ex. SELECT 1) går igenom
 



