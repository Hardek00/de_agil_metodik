### FastAPI on Cloud Run via GitHub → Cloud Build (GUI guide)

This exercise guides you to deploy a simple FastAPI app to Cloud Run using Cloud Build triggers from GitHub. It includes a ready-to-use app, `dockerfile`, `cloudbuild.yaml`, and `requirements.txt`.

## Prerequisites
- GCP project (Owner or Editor)
- Billing enabled
- GitHub repo connected to your account
- Enable APIs: Cloud Build API, Cloud Run Admin API, Artifact Registry API, Service Usage API, IAM API

## One-time setup (Console UI)
1) Enable APIs
- Console → Navigation menu → APIs & Services → Library
- Enable the APIs listed above

2) Create Artifact Registry repository
- Console → Artifact Registry → Repositories → Create
- Name: `de-pipeline` (or your chosen name)
- Format: Docker
- Location type: Region
- Region: `europe-north2` (or your chosen region; keep consistent)

3) Grant Cloud Build permissions
- Console → IAM & Admin → IAM
- Principal: `PROJECT_NUMBER@cloudbuild.gserviceaccount.com`
- Grant roles:
  - Cloud Run Admin
  - Service Account User
  - Artifact Registry Writer

4) Connect GitHub repo and create a trigger
- Console → Cloud Build → Triggers → Connect repository
- Choose GitHub (Cloud Build GitHub App), authorize, select this repo
- Click Create trigger
- Name: `cloud-run-deploy`
- Event: Push to a branch
- Branch (regex): `^main$` (or your branch)
- Configuration: `cloudbuild.yaml`

Note on logs and service account
- If you set a custom Trigger service account, builds may require a logs bucket.
- The `cloudbuild.yaml` below sets `options.logging: CLOUD_LOGGING_ONLY` to avoid that requirement.

## Repository contents

Place these files at the project root (or adjust paths accordingly):

app.py
```python
from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "method": "Cloud Build",
        "message": "Hello from Cloud Run via Cloud Build!",
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

# .pyc cache off to keep image clean
ENV PYTHONDONTWRITEBYTECODE=1
# Unbuffered logs for immediate output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
```

cloudbuild.yaml
```yaml
# Cloud Build pipeline for FastAPI → Artifact Registry → Cloud Run
# Region/repository are set for europe-north2 and de-pipeline; adjust if needed

steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: [
      'build',
      '-t', 'europe-north2-docker.pkg.dev/$PROJECT_ID/de-pipeline/fastapi-demo:${SHORT_SHA}',
      '-f', 'dockerfile',
      '.',
    ]

  - name: 'gcr.io/cloud-builders/docker'
    args: [
      'push',
      'europe-north2-docker.pkg.dev/$PROJECT_ID/de-pipeline/fastapi-demo:${SHORT_SHA}',
    ]

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args: [
      'run', 'deploy', 'fastapi-demo',
      '--image', 'europe-north2-docker.pkg.dev/$PROJECT_ID/de-pipeline/fastapi-demo:${SHORT_SHA}',
      '--region', 'europe-north2',
      '--platform', 'managed',
      '--allow-unauthenticated',
      '--port', '8080',
      '--quiet',
    ]

images:
  - 'europe-north2-docker.pkg.dev/$PROJECT_ID/de-pipeline/fastapi-demo:${SHORT_SHA}'

options:
  logging: CLOUD_LOGGING_ONLY
```

## Run the trigger (first time)
1) In Cloud Build → Triggers, click `cloud-run-deploy` → Run → choose latest commit
2) Watch Logs → ensure all steps succeed

## Verify deployment
- Console → Cloud Run → Service `fastapi-demo` in `europe-north2`
- Click the URL → you should see the JSON response
- Health check: append `/healthz` → `{ "status": "ok" }`

## Subsequent deployments
- Push commits to the configured branch; Cloud Build will build, push, and deploy automatically

## Local development (optional)
```bash
pip install -r requirements.txt
python app.py
# Visit http://localhost:8080/
```

## Notes
- The Dockerfile is named `dockerfile` (lowercase); the build step references it via `-f dockerfile`
- The example uses region `europe-north2`, repository `de-pipeline`, and service `fastapi-demo`

## Troubleshooting
- Permission errors: verify Cloud Build SA roles (Run Admin, SA User, AR Writer)
- Artifact Registry path/region mismatches: ensure repo and Cloud Run region align
- Logs: check Cloud Build build logs and Cloud Run service logs