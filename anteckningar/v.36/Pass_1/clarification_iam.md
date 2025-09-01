### IAM – det du faktiskt behöver i projektet

- **Behöver vi en service account‑nyckelfil (JSON)?**
  - **Lokalt (utveckling/script)**: använd helst `gcloud auth application-default login` (ingen nyckelfil). Om ni måste, använd en gemensam JSON‑nyckel för teamet (aldrig i Git).
  - **Cloud Run/Functions i GCP**: **ingen nyckelfil**. Koppla ett servicekonto till tjänsten; Google sköter credentials.
  - **GitHub → Cloud Build → Cloud Run**: **ingen nyckelfil**. Cloud Build använder sitt eget servicekonto.
  - **GitHub Actions → Cloud Run**: **ingen nyckelfil** om ni använder Workload Identity Federation (rekommenderas). Endast i nödfall använd JSON‑nyckel.

- **Ingestionspipeline (fetch + skriv till BigQuery)**
  - Körs den på **Cloud Run**: koppla ett runtime‑servicekonto till tjänsten och ge BigQuery‑rollerna nedan. **Ingen nyckelfil**.
  - Körs den **lokalt**: använd `gcloud auth application-default login` eller en delad JSON‑nyckel.

- **Hur många servicekonton?**
  - För enkelhet och tydlighet, använd **två** servicekonton:
    - **`app-sa` (runtime)**: används av Cloud Run/Functions vid körning.
    - **`deploy-sa` (CI/CD)**: används av GitHub Actions (via WIF) eller av Cloud Build vid deploy.
  - Undvik ett enda super‑brett servicekonto för “allt”.

- **Minsta roller per scenario**
  - **Runtime (`app-sa`)**:
    - `roles/bigquery.jobUser`
    - `roles/bigquery.dataEditor` (eller snävare dataset‑specifika roller om ni vill)
    - Vid privata images: `roles/artifactregistry.reader`
  - **Cloud Build standard‑SA** (`PROJECT_NUMBER@cloudbuild.gserviceaccount.com`):
    - `roles/run.admin`
    - `roles/iam.serviceAccountUser` på `app-sa` (för att få deploya med det SA:t)
    - `roles/artifactregistry.writer`
  - **`deploy-sa` (GitHub Actions via WIF)**:
    - `roles/run.admin`
    - `roles/iam.serviceAccountUser` på `app-sa`
    - `roles/artifactregistry.writer`
  - **Manuell CLI‑deploy (din användare eller ett deploy‑SA)**:
    - Samma som deploy: `roles/run.admin`, `roles/artifactregistry.writer`, plus `roles/iam.serviceAccountUser` på `app-sa`.

- **API:er att aktivera (en gång per projekt)**
  - Artifact Registry, Cloud Run, Cloud Build, Cloud Functions (om ni använder det), BigQuery.

- **Snabb beslutsguide**
  - Kör du **lokalt**? → `gcloud auth application-default login` (ingen nyckel). Om ej möjligt: delad JSON‑nyckel.
  - Kör du på **Cloud Run/Functions**? → koppla `app-sa`. Ingen nyckel.
  - **CI/CD med Cloud Build**? → använd Cloud Builds SA. Ingen nyckel.
  - **CI/CD med GitHub Actions**? → använd WIF för att impersonera `deploy-sa`. Ingen nyckel.

- **Namnförslag (enkelt att känna igen)**
  - `app-sa@PROJECT_ID.iam.gserviceaccount.com`
  - `deploy-sa@PROJECT_ID.iam.gserviceaccount.com`

- **Säkerhet (minsta ni behöver tänka på)**
  - Checka aldrig in nycklar i Git.
  - Dela nycklar säkert om ni måste använda JSON.
  - Städa efter kursen: ta bort onödiga roller/nycklar och radera projektet.


