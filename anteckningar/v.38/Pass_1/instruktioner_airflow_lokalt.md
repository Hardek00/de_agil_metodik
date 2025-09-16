Run Airflow (LocalExecutor) with Docker Compose

Prerequisites:
- Docker Desktop with Compose v2

Setup (run in project root):
```bash
mkdir -p ./dags ./logs ./plugins ./config
echo "AIRFLOW_UID=$(id -u)" > .env
```

Start services:
```bash
# Option A: one command (airflow-init runs automatically)
docker compose up -d

# Option B: explicit init then start
docker compose up airflow-init
docker compose up -d
```

Open the UI:
- http://localhost:8080
- Username: airflow
- Password: airflow

Place your DAGs in the `dags/` folder.



After you've fetched docker-compose.yaml we clean up the file to get a lightweight version, do the following:

1) Change the executor to LocalExecutor
   - Find `AIRFLOW__CORE__EXECUTOR` under `x-airflow-common.environment` and set it to `LocalExecutor` (replace `CeleryExecutor` if present).
```yaml
x-airflow-common:
  &airflow-common
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
```

2) Delete the Redis service block
   - Remove the entire `redis:` service and everything indented under it until the next top-level service (same indentation as `postgres:`).
```yaml
services:
  redis:              # DELETE this entire block
    image: redis:7.2-bookworm
    ...
```

3) Delete the Celery worker service
   - Remove the entire `airflow-worker:` service block.
```yaml
  airflow-worker:     # DELETE this entire block
    <<: *airflow-common
    command: celery worker
    ...
```

4) Delete the Triggerer service
   - Remove the entire `airflow-triggerer:` service block.
```yaml
  airflow-triggerer:  # DELETE this entire block
    <<: *airflow-common
    command: triggerer
    ...
```

5) Delete Flower (optional monitoring UI for Celery)
   - Remove the entire `flower:` service block, including its `profiles` and `ports`.
```yaml
  flower:             # DELETE this entire block
    <<: *airflow-common
    command: celery flower
    ...
```

6) Optional: Update the header comment
   - Change any mention of "CeleryExecutor with Redis" to "LocalExecutor".

7) Clean start (recommended when switching from Celery)
```bash
docker compose down -v
docker compose up -d
```

Managing the stack:
```bash
# Tail logs
docker compose logs -f | cat

# Stop containers
docker compose down

# Stop and remove volumes (clean reset)
docker compose down -v