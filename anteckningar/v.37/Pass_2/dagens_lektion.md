# Dagens Lektion: Pass 2 – Mer dbt, ML Deployment och Cloud Functions

## Agenda

1. **Recap**  
   En snabb genomgång av tidigare ämnen.

2. **Projektöversikt**  
   Titta på projektet: [Project.pptx.pdf](../project/Project.pptx.pdf) och en titt i mappen [model](../project/model).

3. **Genomgång av dbt**  
   Vi tittar på sources, testing och macros i dbt: [More_dbt.pdf](./More_dbt.pdf).

4. **Hur deployar vi en ML-modell i molnet (GCP)**  
   Genomgång: [Deploying_ML_model.pdf](./Deploying_ML_model.pdf).

5. **Kort genomgång om Cloud Run Functions**  
   Genomgång: [Cloud Functions.pdf](./Cloud Functions.pdf).

## Obs!
Vi kan bygga EL-delen av vår ELT-pipeline på olika sätt. Som grupp väljer ni hur ni vill göra. Samma ingest/load-kod körs på tre olika sätt:

- **Cloud Run (FastAPI)**
- **Cloud Run Job**
- **Cloud Functions (2nd gen)**

Studera arkitekturen, jämför koden sida vid sida och uppskatta skillnader/likheter. Läs respektive anteckningar för varje metod.

## Relaterad Kod och Läsningsmaterial (GitHub)
- **FastAPI kod**: [fetch_write_data](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/fetch_write_data)  
- **FastAPI anteckning**: [fastapi_ingestion.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/fetch_write_data/fastapi_ingestion.md)  
- **Job kod**: [cloud_run_job](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/cloud_run_job)  
- **Job anteckning**: [cloud_run_job.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/cloud_run_job/cloud_run_job.md)  
- **Function kod**: [function](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/function)  
- **Function anteckning**: [functions.md](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/function/functions.md)

6. **Projekt-workshop**  
   Praktisk tid för att arbeta på projektet.