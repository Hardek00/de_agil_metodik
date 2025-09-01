### Continuous Delivery (CD) – Practical notes for this course

Keep CD simple: build once, deploy on merges to main, verify quickly, and be able to roll back.

## What CD is (in our scope)
- Build a container image, push to Artifact Registry, deploy to Cloud Run (or Functions gen2).
- Triggered automatically after code is merged to `main`.

## Trigger strategy (when should deploy happen?)
- Use "main-only" deploys so students work on feature branches and open PRs.
- CI (tests/lint) can run on PRs, but CD (deploy) runs only on `main`.

GitHub Actions
```yaml
on:
  push:
    branches: [ "main" ]
```

Cloud Build (trigger)
- Event: Push to a branch
- Branch (regex): `^main$`


## Permissions and authentication
- Runtime (Cloud Run) uses a runtime service account (`app-sa`). No key files.
- Cloud Build uses its default SA; GitHub Actions uses Workload Identity Federation with a `deploy-sa`.
- Minimal roles:
  - Deploy: `roles/run.admin`, `roles/artifactregistry.writer`, and `roles/iam.serviceAccountUser` on `app-sa`.
  - Runtime (if using BigQuery): `roles/bigquery.jobUser`, `roles/bigquery.dataEditor`.

## Artifacts and image naming
- Tag images with commit SHA for traceability.
- Keep region/repo consistent across steps.

GitHub Actions (example tag)
```bash
DOCKER_TAG="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:${GITHUB_SHA::7}"
```

Cloud Build (example tag)
```yaml
images:
  - 'europe-north2-docker.pkg.dev/$PROJECT_ID/de-pipeline/fastapi-demo:${SHORT_SHA}'
```

## Rollback (+ traffic)
- Easiest: redeploy the previous known-good image tag.
- Cloud Run also supports traffic splitting/rollbacks in Console; for class, use simple redeploy.

## Health checks and smoke tests
- Expose a `/healthz` endpoint returning `{ "status": "ok" }`.
- After deploy, curl the service URL (manual step is fine for class).

## Observability
- Where to look:
  - Build logs: Cloud Build Logs or GitHub Actions logs.
  - Runtime logs: Cloud Run → Logs.

## Safety guardrails (defaults to copy)
- Concurrency: one deploy at a time per service to avoid overlap.

GitHub Actions
```yaml
concurrency:
  group: cloud-run-deploy
  cancel-in-progress: false
```

## Simple defaults for this course
- Region: `europe-north2` (or one you choose—keep it consistent).
- Artifact Registry repo: `de-pipeline` (or reuse service name).
- Service name: `fastapi-demo`.
- Triggers: deploy only on `main`.
- Auth: WIF for GitHub Actions; default SA for Cloud Build.

## Checklist before enabling CD
- APIs enabled: Artifact Registry, Cloud Run, IAM, Cloud Build (and Functions if used).
- Repos connected and triggers created.
- `app-sa` and `deploy-sa` created with minimal roles.
- Dockerfile builds locally; app listens on `PORT`.

## When something breaks
- Permission denied → check SA roles and regions.
- Image not found → verify repo/region and tag (SHA) match.
- 404 after deploy → confirm service name and that the route exists.


