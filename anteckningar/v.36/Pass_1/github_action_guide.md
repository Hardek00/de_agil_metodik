## GitHub Actions CD to Google Cloud Run (GUI-only, no CLI)

This guide walks you and your students through building a Continuous Deployment pipeline that ships a simple FastAPI service to Google Cloud Run using GitHub Actions and OpenID Connect (OIDC) — all via the web UIs only. No terminal commands.

What you already have in this repo:
- `app.py`: minimal FastAPI app with `/` and `/healthz`.
- `Dockerfile` and `requirements.txt`: production container setup.
- `.github/workflows/deploy-cloudrun.yml`: workflow that builds the image, pushes to Artifact Registry, and deploys to Cloud Run using OIDC.

You will set up:
- Google Cloud project, APIs, Artifact Registry repository, Service Account, and Workload Identity Federation (OIDC) trust for GitHub.
- GitHub Actions repository Variables and Secrets that the workflow reads.

Outcome:
- On every push to `main`, the app is containerized, pushed, and deployed to Cloud Run. The workflow prints the live URL.

### 1) Prerequisites (quick checks)
- You have a Google Cloud project with billing enabled.
- You have Owner or Admin rights to configure IAM and APIs.
- You can edit Settings in your GitHub repository.

### 2) Enable required Google Cloud APIs (Console UI)
1. Open Google Cloud Console → Navigation menu → APIs & Services → Library.
2. Enable these APIs (search each name and click Enable):
   - Cloud Run Admin API
   - Artifact Registry API
   - IAM Service Account Credentials API

### 3) Create an Artifact Registry repository (for container images)
1. Navigation menu → Artifact Registry → Repositories → Create repository.
2. Set:
   - Repository name: your desired name (example: `cloud-run-repo`).
   - Format: Docker.
   - Location type: Region.
   - Region: choose your region (example: `europe-central2`). Save this; you will use it as `GAR_LOCATION`.
3. Click Create.

### 4) Create a deployer Service Account and grant roles
1. Navigation menu → IAM & Admin → Service Accounts → Create service account.
2. Name: `gh-actions-deployer` (or your preference). Click Create and continue.
3. Grant these roles to the service account:
   - Cloud Run Admin
   - Artifact Registry Writer
   - (Optional) Viewer
4. Click Done.

Note: Cloud Run also needs a runtime service account for the service itself. The default compute service account is fine for this demo. If you later use a custom runtime SA, grant your deployer SA the “Service Account User” role on that runtime SA.

### 5) Configure Workload Identity Federation (OIDC) for GitHub Actions
This links GitHub Actions to your Google Cloud project without long‑lived keys.

1. Navigation menu → IAM & Admin → Workload Identity Federation.
2. Click "Create Pool":
   - Name: `github-actions` (any name is fine).
   - Click Continue.
3. Create a Provider in this pool:
   - Provider type: OpenID Connect (OIDC).
   - Provider name: `github` (any display name is fine).
   - Provider ID: `github` (any short ID is fine; must start with a letter and contain only lowercase letters, digits, and hyphens; unique within the pool).
   - Issuer URL: `https://token.actions.githubusercontent.com`.
   - JWK file: leave empty (not required for GitHub; keys are public at the issuer).
   - (Keep default attribute mappings or add)
     - `google.subject` → `assertion.sub`
     - `attribute.repository` → `assertion.repository`
     - `attribute.ref` → `assertion.ref`
   - Attribute conditions (recommended security):
     - `attribute.repository == "<OWNER>/<REPO>"`
       - Optionally also: `attribute.ref == "refs/heads/main"` to restrict to main branch.
   - Click Create.
4. Grant the provider permission to impersonate your deployer service account:
   - Still in Workload Identity Federation → Pools → your pool → your provider → Grant access.
   - Select Service account: choose `gh-actions-deployer` you created.
   - Select principals: choose From the same provider, and add the same attribute condition(s) as above.
   - Role: Workload Identity User. Click Save/Grant.
5. Copy the Provider resource name. You’ll need it in GitHub. It looks like:
   - `projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<POOL_ID>/providers/<PROVIDER_ID>`
   - Example (no https prefix): `projects/627443857788/locations/global/workloadIdentityPools/github-actions/providers/github`
### 6) Add GitHub Actions Variables and Secrets (GitHub UI)
In your GitHub repository → Settings → Secrets and variables → Actions.

- Click Variables → New repository variable. Create these variables (match your GCP setup):
  - `SERVICE`: the Cloud Run service name (example: `fastapi-cd-demo`).
  - `REGION`: Cloud Run region (example: `europe-central2`).
  - `GCP_PROJECT_ID`: your project ID (example: `my-gcp-project`).
  - `GAR_LOCATION`: your Artifact Registry region (example: `europe-central2`).
  - `REPOSITORY`: your Artifact Registry repo name (example: `cloud-run-repo`).

- Click Secrets → New repository secret. Create these secrets:
  - `WIF_PROVIDER`: paste the full provider resource name you copied in step 5 (starts with `projects/…/workloadIdentityPools/…`).
  - `SERVICE_ACCOUNT`: the deployer service account email (example: `gh-actions-deployer@<PROJECT_ID>.iam.gserviceaccount.com`).

### 7) Review the workflow that’s already included
Open `.github/workflows/deploy-cloudrun.yml` in your repo.

What it does on push to `main`:
- Authenticates to Google Cloud using OIDC and your service account.
- Configures Docker to push to Artifact Registry in `GAR_LOCATION`.
- Builds the container image from `Dockerfile` and tags it with the commit SHA.
- Pushes the image to Artifact Registry `REPOSITORY` in your project.
- Deploys to Cloud Run `SERVICE` in `REGION` and prints the service URL.

If you want to deploy from a different branch, change the `on.push.branches` value in the workflow and also update the attribute condition in your provider to match the branch (`attribute.ref`).

### 8) Trigger your first deployment (no terminal)
Option A (quick):
1. In GitHub → your repo → open `app.py`.
2. Click the edit pencil, change a string (e.g., the `message`), and click Commit changes directly to `main`.

Option B (create a PR):
1. Edit a file in a branch, open a Pull Request, then merge to `main`.

Then watch it deploy:
1. GitHub → Actions → select “Deploy to Cloud Run”.
2. Click the latest run. You should see steps: Checkout → Authenticate → Setup gcloud → Build & Push → Deploy.
3. When it finishes, the last step prints a URL. Click it.
4. Alternatively, in Google Cloud Console → Cloud Run → Services → click your service → click URL.

### 9) Verify health and behavior
- Open `/` on the service URL. You should see the JSON with method, message, and framework.
- Open `/healthz` to verify a 200 OK response.

### 10) Adjust Cloud Run settings (UI)
In Console → Cloud Run → Services → your service → Edit & deploy new revision:
- Set CPU/Memory, Min instances (0 for scale-to-zero, 1 for faster cold starts), Max instances, Concurrency.
- Add environment variables if needed.
- Save and deploy.

### 11) Common troubleshooting (UI-first)
- Not authorized / OIDC errors:
  - Recheck Workload Identity Federation provider conditions: repository and branch must match your workflow run (see the run details → “Ref” and “Repository”).
  - Ensure you granted Workload Identity User on the deployer service account to the provider.
- Artifact Registry push fails:
  - Verify `GAR_LOCATION` and `REPOSITORY` values match the repository you created.
  - Confirm Artifact Registry API is enabled.
- Cloud Run deploy fails:
  - Confirm Cloud Run Admin API is enabled and `SERVICE`, `REGION`, and `GCP_PROJECT_ID` variables are correct.
  - Ensure the deployer service account has Cloud Run Admin and Artifact Registry Writer roles.

### 12) Optional: Safer releases and approvals
- GitHub Environments (UI): Settings → Environments → New environment (e.g., `prod`) → Require reviewers → Add rule to protect deploy job. Update the workflow to target that environment.
- Branch protection: Settings → Branches → Add rule for `main` (e.g., require PRs).
- Restrict OIDC further: in your provider, add conditions for repository owner, branch, or workflow name.

You’re done! Each push to `main` now builds and deploys this repo to Cloud Run with fully keyless auth and zero CLI.


