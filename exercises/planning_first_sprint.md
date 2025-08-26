## Övning: Planera er första sprint

### Syfte
Att som team planera och starta Sprint 1 för ert kursprojekt: sätta upp repo, definiera sprintmål, skapa sprint backlog med user stories, etablera DoR/DoD, och få ett första minimalt flöde (CI + enkel ingestion) i drift.

### Förutsättningar (ni har redan)
- WSL, Docker, Git
- Testat enkla ingestion‑pipelines lokalt
- Enkla CI‑flöden (t.ex. Ruff)

### Tidbox
- Planering: 60 min?
- Sprintlängd: 1 vecka (förslag)

### Scenario (ramar)
- Dataset: Välj EN publik API‑källa (Task 2) eller weatherAPI (Task 1) och EN enkel destination: fil (JSON/CSV) eller lokal Postgres (Docker Compose) alternativt till cloud (BQ).
- Körning: batch‑jobb (skript eller FastAPI‑endpoint) som kan köras lokalt eller i container.
- Scope: håll det minimalt så att ni kan demo:a fungerande flöde i slutet av sprinten.

### Uppgift – planeringssteg
1) Sätt upp repo
   - Skapa nytt GitHub‑repo med `README.md`, `LICENSE`, `.gitignore` (inkl. `.env`), `docs/`.
   - Lägg `docs/sprint-01/` för planeringsartefakter.
   - Skapa `README` med kort projektsyfte och körinstruktioner.

2) Etablera arbetssätt
   - Skapa GitHub Project board (To do / In progress / Review / Done) eller använd någon annan kanban board.
   - Roller: utse PO och Scrum Master (rotera i nästa sprint).
   - Branch‑strategi: `main` skyddad, feature‑branches (`feature/<kort-namn>`), PR‑flöde med review.
   - Verktyg (utforska):
     - Kanban/issue: GitHub Projects, Jira, Trello, Linear
     - Diagram/skisser: Miro, Excalidraw, draw.io/diagrams.net, Mermaid i `docs/`
     - Dokumentation: `README`, `docs/` (arkitektur, beslut/ADR, demo‑plan)

3) Sprintmål (Sprint Goal)
   - 1–2 meningar som beskriver vad ni vill uppnå (värdet), t.ex.:
     "Som team vill vi kunna hämta väderdata från en publik API och spara den till JSON via ett körbart skript i Docker, validerat av CI (lint)."

4) Backlog → Sprint Backlog
   - Skapa 5–8 små tasks eller user stories (issues). OBS. Ni behöver inte använda user story metoden, ni kan hålla er till tasks.
   - Exempelstory:
     - User story: "Som dataingenjör vill jag köra ett skript som hämtar data från <API> och skriver till `data/raw/YYYY-MM-DD.json` för att kunna analysera datat lokalt."
     - AC (exempel):
       - Given giltig konfiguration i `.env`, When jag kör `make ingest` eller `docker run ...`, Then skapas en JSON‑fil med ≥1 fält från källan.
       - When API är nere, Then loggas tydligt fel och program avslutas med kod ≠ 0.

5) DoD
   - Definition of Done (DoD) – en task eller story är "done" om  tex:

     - Kod pushad, PR reviewad och mergad
     - Lint (Ruff) grön i CI
     - Körbart lokalt (skript eller Docker) med uppdaterad `README`
     - Loggning finns på INFO‑nivå vid start/slut

     Ni får i teamet själva bestäma och beskriva DoD.

6) CI/CD och skelettkod
   - Lägg till GitHub Actions workflow för Ruff (och valfritt: `pytest -q` placeholder).
   - Lägg till `Dockerfile` för ingestion‑skriptet (frivilligt: `docker-compose.yml` om Postgres används).
   - Lägg till `.env.example` och beskriv hur man kör utan hemligheter i repo.

7) Risker och beroenden
   - Lista 3–5 risker (t.ex. API otillgängligt, tidsbrist, otydlig scope) med plan för mitigering.

8) Demo‑plan
   - Vad visar ni på sprint review? Exakt kommando/URL och förväntad output.

### Leverabler (checklista i `docs/sprint-01/`)
- `sprint-goal.md` (1–2 meningar)
- `sprint-backlog.md` (länk till issues + summering SP)
- `DoR_DoD.md`
- `risker.md`
- `demo-plan.md`
- Länk till Project board och repo‑badge för CI‑status i `README`

### Minimikrav för implementation i Sprint 1
- En körbar ingestion (skript eller FastAPI‑endpoint) som:
  - Hämtar data från vald API
  - Skriver till fil (eller Postgres lokalt/BQ i molnet)
  - Har grundläggande loggning (INFO)
- CI som kör Ruff på PR till `main`

### Hints
- Välj en källa utan auth om möjligt första sprinten (minska friktion).
- Begränsa scope till "happy path"; felhantering kan bli en story.
- Skriv `.env.example` och dokumentera exakt körkommando.
- Om ni använder FastAPI: lägg till `/health` för enkel kontroll och demo.



