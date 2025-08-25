# GCP BigQuery Data Pipeline Guide

## Overview
This guide covers creating a simple data pipeline that:
1. Fetches data from an external source
2. Runs locally in Docker
3. Uploads raw data to BigQuery

## Prerequisites
- Google Cloud Platform account
- Docker installed locally
- GCP CLI installed (gcloud)

## 1. GCP Setup

### Create a GCP Project
```bash
# Set project ID
export PROJECT_ID="your-project-id"

# Create project (if needed)
gcloud projects create $PROJECT_ID

# Set current project
gcloud config set project $PROJECT_ID
```

### Enable Required APIs
```bash
# Enable BigQuery API
gcloud services enable bigquery.googleapis.com

# Enable other APIs if needed
gcloud services enable storage.googleapis.com
```

### Create Service Account
```bash
# Create service account
gcloud iam service-accounts create data-pipeline-sa \
    --description="Service account for data pipeline" \
    --display-name="Data Pipeline SA"

# Grant BigQuery permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:data-pipeline-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:data-pipeline-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

# Create and download key
gcloud iam service-accounts keys create ./service-account-key.json \
    --iam-account=data-pipeline-sa@$PROJECT_ID.iam.gserviceaccount.com
```

## 2. Create BigQuery Dataset and Table

### Using gcloud CLI
```bash
# Create dataset
bq mk --dataset $PROJECT_ID:raw_data

# Create table (example schema)
bq mk --table $PROJECT_ID:raw_data.sample_data \
    id:STRING,name:STRING,value:FLOAT,timestamp:TIMESTAMP
```

### Using BigQuery Console
1. Go to BigQuery in GCP Console
2. Create dataset: `raw_data`
3. Create table with your desired schema

## 3. Python Code Implementation

### Create the main Python script (`main.py`)
```python
import requests
import json
import os
from datetime import datetime
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd

class DataPipeline:
    def __init__(self):
        # Initialize BigQuery client
        self.client = bigquery.Client()
        self.project_id = os.environ.get('GCP_PROJECT_ID')
        self.dataset_id = os.environ.get('BQ_DATASET_ID', 'raw_data')
        self.table_id = os.environ.get('BQ_TABLE_ID', 'sample_data')
        
    def fetch_data(self):
        """Fetch data from external source"""
        try:
            # Example: Fetch from JSONPlaceholder API
            response = requests.get('https://jsonplaceholder.typicode.com/posts')
            response.raise_for_status()
            
            data = response.json()
            
            # Add timestamp to each record
            for record in data:
                record['fetched_at'] = datetime.utcnow().isoformat()
            
            print(f"Fetched {len(data)} records")
            return data
            
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            raise
    
    def create_table_if_not_exists(self):
        """Create BigQuery table if it doesn't exist"""
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        
        try:
            self.client.get_table(table_ref)
            print(f"Table {self.table_id} already exists")
        except NotFound:
            # Define schema
            schema = [
                bigquery.SchemaField("userId", "INTEGER"),
                bigquery.SchemaField("id", "INTEGER"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("body", "STRING"),
                bigquery.SchemaField("fetched_at", "TIMESTAMP"),
            ]
            
            table = bigquery.Table(table_ref, schema=schema)
            table = self.client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
    
    def upload_to_bigquery(self, data):
        """Upload data to BigQuery"""
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        
        # Convert to DataFrame for easier handling
        df = pd.DataFrame(data)
        
        # Configure load job
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",  # Append to existing data
            source_format=bigquery.SourceFormat.PARQUET,  # More efficient than JSON
        )
        
        try:
            # Load data
            job = self.client.load_table_from_dataframe(
                df, table_ref, job_config=job_config
            )
            
            # Wait for job to complete
            job.result()
            
            print(f"Loaded {len(data)} rows into {self.dataset_id}.{self.table_id}")
            
        except Exception as e:
            print(f"Error uploading to BigQuery: {e}")
            raise
    
    def run_pipeline(self):
        """Run the complete pipeline"""
        print("Starting data pipeline...")
        
        # Create table if needed
        self.create_table_if_not_exists()
        
        # Fetch data
        data = self.fetch_data()
        
        # Upload to BigQuery
        self.upload_to_bigquery(data)
        
        print("Pipeline completed successfully!")

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
```

### Create requirements file (`requirements.txt`)
```txt
google-cloud-bigquery==3.13.0
pandas==2.1.4
requests==2.31.0
pyarrow==14.0.1
```

## 4. Docker Configuration

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Copy service account key
COPY service-account-key.json .

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Run the application
CMD ["python", "main.py"]
```

### Create docker-compose.yml (optional)
```yaml
version: '3.8'

services:
  data-pipeline:
    build: .
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
      - GCP_PROJECT_ID=your-project-id
      - BQ_DATASET_ID=raw_data
      - BQ_TABLE_ID=sample_data
    volumes:
      - ./service-account-key.json:/app/service-account-key.json:ro
```

### Create .env file
```bash
GCP_PROJECT_ID=your-project-id
BQ_DATASET_ID=raw_data
BQ_TABLE_ID=sample_data
```

## 5. Running the Pipeline

### Build and run with Docker
```bash
# Build the Docker image
docker build -t data-pipeline .

# Run the container
docker run --env-file .env \
    -v $(pwd)/service-account-key.json:/app/service-account-key.json:ro \
    data-pipeline
```

### Run with docker-compose
```bash
# Start the pipeline
docker-compose up --build

# Run once and remove
docker-compose up --build && docker-compose down
```

## 6. Verification

### Check data in BigQuery
```bash
# Query the data
bq query --use_legacy_sql=false \
    'SELECT COUNT(*) as total_records FROM `your-project-id.raw_data.sample_data`'

# View sample data
bq query --use_legacy_sql=false \
    'SELECT * FROM `your-project-id.raw_data.sample_data` LIMIT 10'
```

### Using BigQuery Console
1. Go to BigQuery in GCP Console
2. Navigate to your dataset and table
3. Click "Preview" to see the data

## 7. Best Practices

### Error Handling
```python
import logging
from google.cloud.exceptions import GoogleCloudError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_with_retry(self, data, max_retries=3):
    """Upload with retry logic"""
    for attempt in range(max_retries):
        try:
            self.upload_to_bigquery(data)
            return
        except GoogleCloudError as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Security
- Never commit service account keys to version control
- Use environment variables for sensitive data
- Consider using GCP Workload Identity in production
- Rotate service account keys regularly

### Monitoring
```python
from google.cloud import monitoring_v3

def send_metrics(self, record_count):
    """Send custom metrics to Cloud Monitoring"""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{self.project_id}"
    
    # Create time series data
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/data_pipeline/records_processed"
    series.resource.type = "global"
    
    point = series.points.add()
    point.value.int64_value = record_count
    point.interval.end_time.seconds = int(time.time())
    
    client.create_time_series(name=project_name, time_series=[series])
```

## 8. Scheduling (Optional)

### Using Cloud Scheduler + Cloud Run
1. Deploy as Cloud Run service
2. Create Cloud Scheduler job to trigger HTTP endpoint
3. Set up appropriate IAM permissions

### Using Kubernetes CronJob
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: data-pipeline
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: data-pipeline
            image: your-registry/data-pipeline:latest
            env:
            - name: GCP_PROJECT_ID
              value: "your-project-id"
          restartPolicy: OnFailure
```

## 9. Troubleshooting

### Common Issues
1. **Authentication errors**: Check service account permissions and key file
2. **BigQuery quota exceeded**: Monitor usage and consider batching
3. **Network timeouts**: Implement retry logic with exponential backoff
4. **Schema mismatches**: Validate data before upload

### Debugging
```bash
# Check container logs
docker logs <container-id>

# Run container interactively
docker run -it --entrypoint /bin/bash data-pipeline

# Test BigQuery connection
bq ls --project_id=your-project-id
```

## 10. Next Steps

- Implement data validation and cleaning
- Add data transformation logic
- Set up monitoring and alerting
- Consider using Apache Airflow for complex workflows
- Implement incremental data loading
- Add data quality checks
