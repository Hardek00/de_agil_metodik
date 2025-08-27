# Service Account (GCP) – Vad, varför, när

## Vad är ett Service Account?
- En särskild identitet i GCP för icke‑mänskliga användare (jobb, appar, CI/CD, tjänster).
- Får roller/behörigheter (IAM) precis som människor – men används av kod/arbetslaster.
- Exempel: en Cloud Run‑tjänst eller ett lokalt skript som behöver åtkomst till BigQuery.

Skillnad mot användarkonto:
- Användare loggar in med sina Google‑konton; roller knutna till personen.
- Service account har egna roller; koden agerar “som” servicekontot, oberoende av vem som kör den.

## Varför behövs det?
- Säker åtkomst för jobb och tjänster utan att använda personliga konton.
- Minsta möjliga behörigheter (least privilege) kan tilldelas specifikt för en applikation.
- Spårbarhet i loggar: “vilket konto” gjorde vad i projektet.

## När använder man det?
- Cloud Run/Functions/VMs som behöver åtkomst till GCP‑resurser (BQ, GCS, Pub/Sub …).
- CI/CD‑pipelines som deployar/kör mot GCP.
- Lokala skript under utveckling (gemensamt servicekonto i kursen).

## Hur funkar behörigheter (IAM)?
- Roller binds till identiteter på en nivå: Org/Folder/Projekt/Resurs (ärvs nedåt).
- Tilldela snäva, predefined roller framför breda (undvik Owner/Editor).
- Exempel för BigQuery: `roles/bigquery.jobUser` + `roles/bigquery.dataEditor`.

## Två sätt att använda ett Service Account
1) Nyckelfil (JSON) – enklast att börja med
- Project Owner skapar ett servicekonto och tilldelar roller till servicekontot.
- En (1) nyckel laddas ned som `service-account-key.json`.
- Varje utvecklare sparar nyckeln lokalt (aldrig i Git) och sätter miljövariabel:
  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json
  ```
- Fördelar: enkelt att komma igång lokalt. Nackdel: hantering/rotation av nycklar.

2) Utan nyckel (impersonation) – mer avancerat
- Project Owner ger utvecklare rollen `roles/iam.serviceAccountTokenCreator` på SA:t.
- Utvecklare kan då agera som servicekontot via sin egen inloggning, t.ex.:
  ```bash
  gcloud auth login
  gcloud config set project <PROJECT_ID>
  gcloud auth print-identity-token --impersonate-service-account=<SA_EMAIL>
  # eller köra verktyg/SDK som använder samma impersonation‑kontext
  ```
- Exempel:
  ```bash
  # Servicekont exempel ingest-sa@my-student-proj-123.iam.gserviceaccount.com
  gcloud auth login
  gcloud config set project my-student-proj-123
  gcloud auth print-identity-token --impersonate-service-account=ingest-sa@my-student-proj-123.iam.gserviceaccount.com
  ```
- Fördelar: inga nycklar att läcka. Nackdel: lite mer setup/kunskap.

I kursen: börja med nyckelfil (enkelt). Lär impersonation senare.

## Lokalt vs i molnet (ADC)
- Lokalt (utveckling):
  - Alternativ A: Nyckelfil (JSON) + `GOOGLE_APPLICATION_CREDENTIALS=service-account-key.json`.
  - Alternativ B: `gcloud auth application-default login` (använder din användare via ADC).
  - Alternativ C: Impersonation av servicekonto (ingen nyckel) med `--impersonate-service-account`.
  - Viktigt: checka aldrig in nycklar; dela dem säkert om ni använder nyckel.
- I molnet (Cloud Run/Functions/VM):
  - Ingen nyckelfil behövs. Bifoga servicekontot till tjänsten så används Application Default Credentials (ADC) automatiskt.
- CI/CD (senare):
  - Använd Workload Identity Federation istället för nyckelfiler.

## Bästa praxis (kort)
- Minsta möjliga roller; undvik Owner/Editor.
- En SA per applikation/miljö (dev/test/prod) om möjligt.
- Nycklar: dela säkert, förvara lokalt, rotera regelbundet.
- Lägg `service-account-key.json` och `.env` i `.gitignore`.
- Aktivera relevanta loggar och följ upp åtkomst.

## Vanliga misstag
- Checka in nycklar i repo → absolut förbjudet.
- Ge för breda roller (Editor) på projektet “för att det funkar”.
- Fel projekt valt i gcloud/ADC → “permission denied”.
- Glömt aktivera API:er (t.ex. BigQuery API) i projektet.



## Vidare läsning
- IAM‑översikt och best practices: se `anteckningar/v.35/Pass_1/iam.md`
- Team‑samarbete i GCP (roller/arbetsflöden): `anteckningar/v.35/Pass_2/collab_in_gcp.md`
- Gruppens setup‑övning: `anteckningar/v.35/Pass_2/group_setup_gcp.md`
