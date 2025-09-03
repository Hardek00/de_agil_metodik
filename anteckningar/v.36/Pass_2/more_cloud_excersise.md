# Hands‑on: Build and run a tiny pipeline on GCP

You will deploy two tiny services, wire CI/CD triggers, orchestrate with Workflows, and schedule runs using the Google Cloud Console.

What you will build
- Producer (Cloud Run): GET /produce returns a JSON greeting; reads a secret
- Consumer (Cloud Run): POST /write saves received JSON to a GCS bucket
- CI/CD: two Cloud Build triggers, each filtered to its folder
- Orchestration: a Workflow that calls Producer → Consumer with OIDC
- Scheduling: Cloud Scheduler triggers the Workflow daily

Use code from: https://github.com/Hardek00/demo_ingestion_pipeline
exercise_producer 
and
exercise_consumer



Repo structure
```
  exercise_producer/
    app.py
    cloudbuild.yaml
    dockerfile
    requirements.txt
  exercise_consumer/
    app.py
    cloudbuild.yaml
    dockerfile
    requirements.txt
```

Important placeholders in this guide
- PROJECT_ID: your GCP project ID
- PROJECT_NUMBER: numeric project number (Console → Home → Project info)
- REGION: pick one (e.g., europe‑north2 for Cloud Run/AR; europe‑west1 for Workflows)
- BUCKET: the name of a GCS bucket you own
- PRODUCER_URL / CONSUMER_URL: URLs shown on each Cloud Run service page after deploy

——————————————

## 1) Create the Secret
1. Console → Security → Secret Manager → Create Secret
2. Name: EXERCISE_SECRET
3. Secret value: any non‑empty text (e.g., super‑secret)
4. Create
5. Open the secret → Permissions → Grant access
   - Principal: PROJECT_NUMBER@cloudbuild.gserviceaccount.com
   - Role: Secret Manager Secret Accessor → Save
   (You will grant the Producer runtime account later after the first deploy.)

## 2) Create an Artifact Registry repository
1. Console → Artifact Registry → Repositories → Create Repository
2. Name: ingestion‑pipepline
3. Format: Docker
4. Location type: Region; Location: REGION (e.g., europe‑north2)
5. Create

## 2a) Create a GCS bucket (for the consumer to write to)
1. Console → Cloud Storage → Buckets → Create
2. Bucket name: globally unique, lowercase (e.g., `my-demo-bucket-<random>`)
3. Location type: Region; Location: pick the same or a nearby region as Cloud Run (e.g., europe‑north2)
4. Storage class: Standard (default is fine)
5. Access control: Uniform bucket‑level access (recommended)
6. Protection & encryption: keep defaults (Google‑managed encryption)
7. Create
Note: You do not need to pre‑create the `exercise/` folder. The consumer writes objects with that prefix.

## 3) Cloud Build trigger for Producer
1. Console → Cloud Build → Triggers → Create Trigger
2. Name: exercise‑producer
3. Event: Push to a branch; Branch: ^main$
4. Repository: select your GitHub/Cloud Source repo connected to this project
5. Build configuration: Cloud Build configuration file (yaml or json)
6. Location: Repository; File location: exercise_producer/cloudbuild.yaml
7. Click Show included and ignored files filters → Included files filter: add a line with
   - exercise_producer/**
8. Substitutions: Skip adding substitutions unless you want to override a default from `exercise_producer/cloudbuild.yaml`. The provided YAML already contains sensible defaults (region/repo/image/service/secret). You can always edit the YAML later if you need different values.
9. Create

Run once to deploy
- In Triggers list → exercise‑producer → Run → choose main → Run
- Wait for success → Console → Cloud Run → Services → exercise‑producer
- Copy the service URL; open /health in a new tab. It may show has_secret=false until we grant runtime access in step 6.

## 4) Cloud Build trigger for Consumer
1. Console → Cloud Build → Triggers → Create Trigger
2. Name: exercise‑consumer
3. Event: Push to a branch; Branch: ^main$
4. Build configuration: Cloud Build configuration file
5. File location: exercise_consumer/cloudbuild.yaml
6. Included files filter: exercise_consumer/**
7. Substitutions: Double‑check the defaults defined in `exercise_consumer/cloudbuild.yaml`. If `_BUCKET` in the YAML isn’t your bucket, override it here by adding a substitution with Name `_BUCKET` and Value set to your bucket (e.g., `my-demo-bucket`). Otherwise, you can leave substitutions empty.
8. Create

Run once to deploy
- Triggers → exercise‑consumer → Run
- After success: Cloud Run → Services → exercise‑consumer → copy service URL

## 5) Grant Producer runtime access to the secret
1. Cloud Run → Services → exercise‑producer → Details → Security → Service account → note the email (e.g., PROJECT_NUMBER‑compute@developer.gserviceaccount.com or a custom one)
2. Security → Secret Manager → EXERCISE_SECRET → Permissions → Grant access
   - Principal: the Producer service account email noted above
   - Role: Secret Manager Secret Accessor → Save
3. Redeploy Producer to pick up permission (easiest path): Cloud Build → Triggers → Run the producer trigger again. Then check /health shows has_secret=true.

## 6) Smoke test the services
- Producer: open https://PRODUCER_URL/produce?name=Alice → should return JSON
- Consumer: Cloud Run → exercise‑consumer → Testing tab →
  - Method: POST, Path: /write
  - Body: {"name":"Alice","demo":true}
  - Send request → check in GCS: gs://BUCKET/exercise/… file is created

## 7) Create a Workflow to orchestrate Producer → Consumer
A) Create a dedicated workflow service account
1. IAM & Admin → Service Accounts → Create Service Account
2. Name: wf‑exercise
3. Create and continue → Done (no roles now)

B) Allow this SA to invoke both Cloud Run services
1. Cloud Run → exercise‑producer → Permissions → Grant access
   - Principal: wf‑exercise@PROJECT_ID.iam.gserviceaccount.com
   - Role: Cloud Run Invoker → Save
2. Repeat for exercise‑consumer (same role)

C) Create the Workflow
1. Workflows → Create Workflow
2. Name: exercise‑orchestration; Region: europe‑west1 (or any Workflows region)
3. Service account: wf‑exercise@PROJECT_ID.iam.gserviceaccount.com
4. Environment variables (Runtime environment variables):
   - PRODUCER_URL = https://PRODUCER_URL
   - CONSUMER_URL = https://CONSUMER_URL
   - DEFAULT_NAME = Student
5. In the editor, paste the content of `workflows/exercise_orchestration.yaml` from this repo (it already uses those env vars and OIDC)
6. Deploy

D) Test the Workflow
1. Workflows → exercise‑orchestration → Execute
2. Input:
```
{ "input": { "name": "Alice" } }
```
3. Run → Inspect the execution logs; you should see 200s from both steps
4. Verify a new object appears in gs://BUCKET/exercise/

## 8) Schedule daily runs
1. Cloud Scheduler → Create Job
2. Name: exercise‑daily; Region: same region as Scheduler supports (e.g., europe‑west1)
3. Frequency (cron): 30 22 * * *; Timezone: Europe/Stockholm
4. Target type: Workflows
5. Workflow: exercise‑orchestration; Region: your Workflow region
6. Execution argument:
```
{ "input": {} }
```
7. Service account: App Engine default (PROJECT_NUMBER@appspot.gserviceaccount.com) or any SA with role Workflows Invoker
8. Create → Run now to test


## Troubleshooting (quick)
- 403 when reading secret: grant Secret Manager Secret Accessor to the Producer runtime service account; redeploy producer
- 401 calling services from Workflow: ensure wf‑exercise SA has Cloud Run Invoker on both services
- Scheduler cannot start Workflow: the Scheduler SA must have Workflows Invoker
- Consumer writes but no object: check BUCKET name and that the service account used by Cloud Run has Storage Object Admin on the bucket (Cloud Run’s runtime SA)


