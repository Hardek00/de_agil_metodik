### Dagens Lektion: Pass 2, v.36

## 1. Recap
- Kort återkoppling från förra passet och status i projekten.

## 2. Genomgång: Mer Cloud + demo ingestion‑pipeline
- Läs/presentera: [more_cloud.pdf](./more_cloud.pdf)

## 3. Projektet
- Genomgång: [Project.pptx.pdf](./Project.pptx.pdf)

## 4. Övning: Deploya två tjänster, orkestrera med Workflows och schemalägg med Cloud Scheduler
- Instruktion: [more_cloud_excersise.md](./more_cloud_excersise.md)

## 5. Jämför körningssätt för EL‑delen
Vi kan bygga EL‑delen av vår ELT‑pipeline på olika sätt. Som grupp väljer ni hur ni vill göra. Samma ingest/load‑kod körs på tre olika sätt:
- Cloud Run (FastAPI)
- Cloud Run Job
- Cloud Functions (2nd gen)

Studera arkitekturen, jämför koden sida vid sida och uppskatta skillnader/likheter. Läs respektive anteckningar för varje metod.

Relaterad kod och läsning (GitHub):
- FastAPI kod: [fetch_write_data](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/fetch_write_data)
- FastAPI anteckning: [fastapi_ingestion.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/fetch_write_data/fastapi_ingestion.md)
- Job kod: [cloud_run_job](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/cloud_run_job)
- Job anteckning: [cloud_run_job.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/cloud_run_job/cloud_run_job.md)
- Function kod: [function](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/function)
- Function anteckning: [functions.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/function/functions.md)

## 6. Grupphandledning
- Jag sitter gärna med på era standups och hjälper till med blockerare.

## 7. Resurser
- Cloud Run
  - [Kom igång med Cloud Run](https://cloud.google.com/run/docs/quickstarts/deploy-container)
  - [Cloud Run Jobs – översikt](https://cloud.google.com/run/docs/execute/jobs)
  - [Tjänster vs Jobs – jämförelse](https://cloud.google.com/run/docs/compare/services-and-jobs)
- Cloud Functions (2nd gen)
  - [Deploy med gcloud (2nd gen)](https://cloud.google.com/functions/docs/deploy#deploying)
- Orkestrering och schemaläggning
  - [Workflows – översikt](https://cloud.google.com/workflows/docs)
  - [Cloud Scheduler – översikt](https://cloud.google.com/scheduler/docs)
- Logging/Observability
  - [Cloud Logging – kom igång](https://cloud.google.com/logging/docs)



