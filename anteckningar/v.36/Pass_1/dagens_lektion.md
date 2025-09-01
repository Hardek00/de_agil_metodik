### Dagens Lektion: Pass 1, v.36

## 1. Recap v.35
- Kort återkoppling från förra veckan (Docker, CI, ingestion‑pipeline).

## 2. Kort genomgång: IAM för projektet
- Läs: [clarification_iam.md](./clarification_iam.md) (det du faktiskt behöver).

## 3. Kort genomgång: CD i kursen
- Läs: [cd.md](./cd.md) (triggers på main, roller, rollback, loggar).

## 4. Övningar – Continuous Delivery
- Cloud Build → Cloud Run: [ovning_cd_cloudbuild.md](./ovning_cd_cloudbuild.md)
- GitHub Actions → Cloud Run: [ovning_cd_github_actions.md](./ovning_cd_github_actions.md)

## 5. Kort genomgång: Logging
- Läs: [logging.md](./logging.md)

## 6. Övning – Logging
- Gör: [ovning_logging.md](./ovning_logging.md)

## 7. Som grupp – GCP‑setup
- Gör: [group_setup_gcp.md](./group_setup_gcp.md)

## 8. Projektarbete
- Sätt upp CI/CD‑pipeline (eller delar av den):
  - Deploy triggas endast på `main`.
  - WIF för GitHub Actions (eller Cloud Build trigger).
  - Exponera `/healthz` och verifiera efter deploy.


## 9. Resurser


- Cloud Build
  - [Översikt: Cloud Build](https://cloud.google.com/build/docs/overview)
  - [cloudbuild.yaml – konfiguration och steg](https://cloud.google.com/build/docs/build-config-file-schema)
  - [Bygga och deploya till Cloud Run med Cloud Build](https://cloud.google.com/build/docs/deploying-builds/deploy-cloud-run)

- GitHub Actions → GCP
  - [Google GitHub Actions – auth (WIF)](https://github.com/google-github-actions/auth)
  - [Deploy to Cloud Run action](https://github.com/google-github-actions/deploy-cloudrun)
  - [Workflow‑exempel för Cloud Run](https://github.com/google-github-actions/deploy-cloudrun#example-workflows)

- Cloud Run och Functions
  - [Cloud Run – kom igång](https://cloud.google.com/run/docs/quickstarts/deploy-container)
  - [Cloud Functions (2nd gen) – deploy med gcloud](https://cloud.google.com/functions/docs/deploy#deploying)
  - [Autentisering och servicekonton i Cloud Run](https://cloud.google.com/run/docs/authenticating/service-to-service)

- Artifact Registry
  - [Skapa Docker‑repository och pusha images](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)

- BigQuery (för ingestion)
  - [BigQuery – roller och behörigheter](https://cloud.google.com/bigquery/docs/access-control)
  - [Python klientbibliotek – snabbstart](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries)

- Logging och Observability
  - [Cloud Logging – kom igång](https://cloud.google.com/logging/docs)
  - [Strukturerade loggar (JSON) i Cloud Run](https://cloud.google.com/run/docs/logging#structured-logging)
  - [Log Explorer – filtrera och felsöka](https://cloud.google.com/logging/docs/view/overview)

