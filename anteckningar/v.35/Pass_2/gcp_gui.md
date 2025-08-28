# GCP BigQuery Data Pipeline Guide - Web Interface Version

## Overview
This guide shows students how to set up a data pipeline using the Google Cloud Platform web interface (GUI). This covers the same functionality as the CLI version but through point-and-click actions in the browser.


**What we'll build:**
1. Fetch data from an external source
2. Run locally in Docker
3. Upload raw data to BigQuery

## Prerequisites
- Google Cloud Platform account (free tier is sufficient)
- Docker installed locally
- Web browser (Chrome recommended)

---

## 1. GCP Project Setup

### Step 1.1: Create a New Project

1. **Go to Google Cloud Console**
   - Open [console.cloud.google.com](https://console.cloud.google.com)
   - Sign in with your Google account

2. **Create a new project**
   - Click the project dropdown at the top of the page (next to "Google Cloud Platform")
   - Click "NEW PROJECT"
   - Enter project name: `data-pipeline-demo` (or your preferred name)
   - Note the **Project ID** (you'll need this later)
   - Click "CREATE"
   - Wait for project creation to complete

3. **Select your project**
   - Click the project dropdown again
   - Select your newly created project

### Step 1.2: Enable Required APIs

1. **Navigate to APIs & Services**
   - In the left sidebar, click "APIs & services" → "Library"
   - Or use the search bar and type "APIs & Services"

2. **Enable BigQuery API**
   - In the API Library search bar, type "BigQuery"
   - Click on "BigQuery API"
   - Click the blue "ENABLE" button
   - Wait for activation to complete

3. **Enable Cloud Storage API (optional but recommended)**
   - Go back to API Library
   - Search for "Cloud Storage"
   - Click "Cloud Storage API"
   - Click "ENABLE"

---

## 2. Service Account Setup

### Step 2.1: Create Service Account

1. **Navigate to IAM & Admin**
   - In the left sidebar, click "IAM & Admin" → "Service Accounts"

2. **Create service account**
   - Click "CREATE SERVICE ACCOUNT" button
   - Fill in the details:
     - **Service account name**: `data-pipeline-sa`
     - **Service account ID**: `data-pipeline-sa` (auto-filled)
     - **Description**: `Service account for data pipeline operations`
   - Click "CREATE AND CONTINUE"

### Step 2.2: Grant Permissions #

1. **Add BigQuery roles**
   - In the "Grant this service account access to project" section:
   - Click "Select a role" dropdown
   - Type "BigQuery" in the search
   - Select "BigQuery Data Editor"
   - Click "ADD ANOTHER ROLE"
   - Select "BigQuery Job User"
   - Click "CONTINUE"
   - Click "DONE"

### Step 2.3: Create and Download Key

1. **Generate key file**
   - In the Service Accounts list, click on your newly created service account
   - Go to the "KEYS" tab
   - Click "ADD KEY" → "Create new key"
   - Select "JSON" format
   - Click "CREATE"
   - The key file will download automatically
   - **Important**: Save this file as `service-account-key.json` in your project folder

⚠️ **Security Note**: Never share this key file or commit it to version control!

---

## 3. BigQuery Setup

### Step 3.1: Navigate to BigQuery

1. **Open BigQuery**
   - In the left sidebar, click "BigQuery" → "SQL workspace"
   - Or search for "BigQuery" in the top search bar

2. **Familiarize yourself with the interface**
   - Left panel: Explorer (shows projects, datasets, tables)
   - Center: Query editor
   - Right panel: Query results

### Step 3.2: Create Dataset

1. **Create a new dataset**
   - In the Explorer panel, click on your project name
   - Click the three dots (⋮) next to your project name
   - Select "Create dataset"

2. **Configure dataset**
   - **Dataset ID**: `raw_data`
   - **Data location**: Choose your preferred region (e.g., `us-central1`)
   - **Default table expiration**: Leave blank (no expiration)
   - **Encryption**: Google-managed key (default)
   - Click "CREATE DATASET"

### Step 3.3: Create Table

1. **Create table in dataset**
   - Click on your `raw_data` dataset in the Explorer
   - Click "CREATE TABLE"

2. **Configure table creation**
   - **Source**: Empty table
   - **Destination**:
     - Project: Your project ID
     - Dataset: `raw_data`
     - Table: `sample_data`
   - **Schema**: Click "Add field" and add these fields:
     ```
     Field name: userId    | Type: INTEGER | Mode: NULLABLE
     Field name: id        | Type: INTEGER | Mode: NULLABLE  
     Field name: title     | Type: STRING  | Mode: NULLABLE
     Field name: body      | Type: STRING  | Mode: NULLABLE
     Field name: fetched_at| Type: TIMESTAMP| Mode: NULLABLE
     ```
   - Click "CREATE TABLE"

---

## 4. Test BigQuery Access

### Step 4.1: Run a Test Query

1. **Write a simple query**
   - In the query editor, paste:
   ```sql
   SELECT 
     'Hello BigQuery!' as message,
     CURRENT_TIMESTAMP() as current_time
   ```

2. **Execute the query**
   - Click the blue "RUN" button
   - Verify you see results in the bottom panel

### Step 4.2: Verify Table Structure

1. **Check your table**
   - In the Explorer, navigate to your project → `raw_data` → `sample_data`
   - Click on the table name
   - Click the "SCHEMA" tab to verify your fields are correct
   - Click "PREVIEW" tab (it will be empty since no data is loaded yet)

---

## 5. Local Development Setup

### Step 5.1: Create Project Structure

Create a folder structure like this:
```
data-pipeline/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── service-account-key.json  (downloaded from GCP)
```

### Step 5.2: Create the Python Code

**Create `main.py`:**
```python
import requests
import json
import os
from datetime import datetime
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataPipeline:
    def __init__(self):
        """Initialize the data pipeline with BigQuery client and configuration"""
        self.client = bigquery.Client()
        self.project_id = os.environ.get('GCP_PROJECT_ID')
        self.dataset_id = os.environ.get('BQ_DATASET_ID', 'raw_data')
        self.table_id = os.environ.get('BQ_TABLE_ID', 'sample_data')
        
        logger.info(f"Pipeline initialized for project: {self.project_id}")
        
    def fetch_data(self):
        """Fetch data from external API"""
        try:
            logger.info("Fetching data from JSONPlaceholder API...")
            response = requests.get('https://jsonplaceholder.typicode.com/posts', timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Add timestamp to each record
            current_time = datetime.now()
            for record in data:
               record['fetched_at'] = current_time
            
            logger.info(f"Successfully fetched {len(data)} records")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            raise
    
    def upload_to_bigquery(self, data):
        """Upload data to BigQuery table"""
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            logger.info(f"Prepared {len(df)} records for upload")
            
            # Configure load job
            job_config = bigquery.LoadJobConfig(
                write_disposition="WRITE_APPEND",
                autodetect=False,  # Use predefined schema
            )
            
            # Upload data
            logger.info("Starting BigQuery upload...")
            job = self.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            
            # Wait for completion
            job.result()
            
            # Get updated table info
            table = self.client.get_table(table_ref)
            logger.info(f"Upload complete! Table now has {table.num_rows} total rows")
            
        except Exception as e:
            logger.error(f"Error uploading to BigQuery: {e}")
            raise
    
    def run_pipeline(self):
        """Execute the complete data pipeline"""
        try:
            logger.info("=" * 50)
            logger.info("Starting Data Pipeline")
            logger.info("=" * 50)
            
            # Fetch data
            data = self.fetch_data()
            
            # Upload to BigQuery
            self.upload_to_bigquery(data)
            
            logger.info("=" * 50)
            logger.info("Pipeline completed successfully!")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
```

**Create `requirements.txt`:**
```txt
google-cloud-bigquery==3.13.0
pandas==2.1.4
requests==2.31.0
pyarrow==14.0.1
```

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY service-account-key.json .

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json

# Run the application
CMD ["python", "main.py"]
```

**Create `.env` file:**
```bash
GCP_PROJECT_ID=your-actual-project-id-here
BQ_DATASET_ID=raw_data
BQ_TABLE_ID=sample_data
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  data-pipeline:
    build: .
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
      - GCP_PROJECT_ID=${GCP_PROJECT_ID}
      - BQ_DATASET_ID=${BQ_DATASET_ID}
      - BQ_TABLE_ID=${BQ_TABLE_ID}
    volumes:
      - ./service-account-key.json:/app/service-account-key.json:ro
```

---

## 6. Running the Pipeline

### Step 6.1: Prepare Environment

1. **Update the .env file**
   - Replace `your-actual-project-id-here` with your actual GCP project ID
   - You can find this in the GCP Console at the top of the page

2. **Verify files are in place**
   - Ensure `service-account-key.json` is in your project folder
   - All other files should be created as shown above

### Step 6.2: Build and Run

**Option 1: Using Docker directly**
```bash
# Build the image
docker build -t data-pipeline .

# Run the container
docker run --env-file .env data-pipeline
```

**Option 2: Using Docker Compose (recommended)**
```bash
# Build and run in one command
docker-compose up --build

# To run and then clean up
docker-compose up --build && docker-compose down
```

---

## 7. Verify Results in BigQuery

### Step 7.1: Check Data Upload

1. **Go back to BigQuery in GCP Console**
   - Navigate to your project → `raw_data` → `sample_data`

2. **Preview the data**
   - Click on your table name
   - Click the "PREVIEW" tab
   - You should see 100 records from the JSONPlaceholder API

### Step 7.2: Run Verification Queries

1. **Count total records**
   ```sql
   SELECT COUNT(*) as total_records 
   FROM `your-project-id.raw_data.sample_data`
   ```

2. **View sample data**
   ```sql
   SELECT userId, id, title, fetched_at
   FROM `your-project-id.raw_data.sample_data`
   ORDER BY fetched_at DESC
   LIMIT 10
   ```

3. **Check data freshness**
   ```sql
   SELECT 
     MIN(fetched_at) as earliest_fetch,
     MAX(fetched_at) as latest_fetch,
     COUNT(*) as total_records
   FROM `your-project-id.raw_data.sample_data`
   ```

---

## 8. Monitoring and Management

### Step 8.1: View Job History

1. **Check BigQuery job history**
   - In BigQuery, click "Job history" in the left panel
   - You'll see all your data loading jobs
   - Click on any job to see details, duration, and bytes processed

### Step 8.2: Monitor Costs

1. **View billing information**
   - Go to "Billing" in the left sidebar
   - Click "Reports" to see cost breakdown
   - BigQuery has generous free tier limits

### Step 8.3: Set up Alerts (Optional)

1. **Create budget alerts**
   - Go to "Billing" → "Budgets & alerts"
   - Click "CREATE BUDGET"
   - Set a monthly budget limit (e.g., $10)
   - Configure email alerts at 50%, 90%, and 100%

---



### GCP Documentation
- [BigQuery Documentation](https://cloud.google.com/bigquery/docs)
- [Service Account Best Practices](https://cloud.google.com/iam/docs/best-practices-for-service-accounts)
- [BigQuery Pricing](https://cloud.google.com/bigquery/pricing)

### Learning Paths
- [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
- [BigQuery for Data Analysts](https://cloud.google.com/training/data-ml#bigquery-path)
- [Google Cloud Professional Data Engineer](https://cloud.google.com/certification/data-engineer)

### Community Resources
- [Google Cloud Community](https://cloud.google.com/community)
- [Stack Overflow - Google BigQuery](https://stackoverflow.com/questions/tagged/google-bigquery)
- [Reddit - r/googlecloud](https://reddit.com/r/googlecloud)

---

**Congratulations!** 🎉 You've successfully created a data pipeline that fetches external data and loads it into BigQuery using the Google Cloud Platform web interface. This foundation can be extended for more complex data engineering tasks.
