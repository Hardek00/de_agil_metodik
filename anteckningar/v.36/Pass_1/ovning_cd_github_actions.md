### FastAPI on Cloud Run via GitHub Actions (predefined workflow)

This exercise deploys the same FastAPI app as in the Cloud Build exercise, but using GitHub Actions → New workflow → “Build and Deploy to Cloud Run”.

## Prerequisites
- GCP project with billing enabled
- APIs enabled: Cloud Run Admin API, Artifact Registry API, IAM API (and Service Usage API)
- GitHub repository with this code

## Repository contents (same app as before)

app.py
```python
from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "method": "GitHub Actions",
        "message": "Hello from Cloud Run via GitHub Actions!",
        "framework": "FastAPI",
    }


@app.get("/healthz")
def read_healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
```

requirements.txt
```txt
fastapi>=0.111.0,<0.112.0
uvicorn[standard]>=0.30.0,<0.31.0
```

dockerfile
```docker
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

## One-time GCP setup
1) Create an Artifact Registry repository
- Console → Artifact Registry → Repositories → Create
- Repository: `de-pipeline` (Docker), Region: `europe-north2` (or your region)

2) Create service accounts (simple course setup)
- Runtime: `app-sa` (used by Cloud Run service)
- Deploy: `deploy-sa` (used by GitHub Actions via Workload Identity Federation)

3) Grant minimal roles
- `deploy-sa`:
  - `roles/run.admin`
  - `roles/artifactregistry.writer`
  - `roles/iam.serviceAccountUser` on `app-sa`
- `app-sa` (if your app needs BQ later):
  - `roles/bigquery.jobUser`
  - `roles/bigquery.dataEditor` (or dataset-scoped equivalent)

4) Configure Workload Identity Federation (recommended)
- Follow the prompts in GitHub’s predefined workflow to set up a WIF pool/provider and connect your repo
- You’ll end up with two repo secrets:
  - `GCP_WORKLOAD_IDENTITY_PROVIDER`
  - `GCP_SERVICE_ACCOUNT` (the `deploy-sa` email)

Note: If WIF is not feasible, you can use a JSON key secret, but avoid it if possible.

## Create the workflow in GitHub
1) GitHub → Actions → New workflow → search “Cloud Run”
2) Select “Build and Deploy to Cloud Run” (by Google)
3) In the generated YAML, only update these fields in `env`:
   - `PROJECT_ID`: your GCP project id
   - `REGION`: e.g., `europe-north2`
   - `SERVICE`: e.g., `fastapi-demo` (also used as the Artifact Registry repo name by the template)
   - `WORKLOAD_IDENTITY_PROVIDER`: the full resource name from your WIF provider
4) Follow on‑screen prompts to finish WIF setup, then commit the workflow

Why no YAML here? The predefined workflow already includes the correct actions, auth, Docker build/push, and deployment steps. Keeping to the template reduces copy/paste errors and stays updated over time.

## Run it
- Push to `main`
- Watch the Actions tab → your workflow should build, push, and deploy

## Verify
- Console → Cloud Run → open service `fastapi-demo`
- Open URL → should return JSON
- Health: append `/healthz` → `{ "status": "ok" }`

## Troubleshooting
- “permission denied”: check roles on `deploy-sa` and `iam.serviceAccountUser` on `app-sa`
- image not found/region mismatch: verify Artifact Registry region matches `REGION`
- OIDC/WIF errors: re-check provider settings and repo bindings; secrets must match values from GCP


