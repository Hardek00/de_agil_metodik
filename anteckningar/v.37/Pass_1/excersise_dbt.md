# dbt Exercise: Creating Staging Models

## Overview
This exercise guides you through setting up a dbt project with BigQuery, ingesting sample data, and creating staging models. The goal is to practice unpacking, renaming, and casting data in dbt, using both nested and unnested JSON data.

By the end, you'll have transformed raw data into clean staging tables, ready for further modeling.

## Prerequisites
- Python installed (version 3.8+ recommended)
- Google Cloud account with BigQuery access
- A service account key for BigQuery (download from Google Cloud Console)
- Basic familiarity with terminal commands and SQL
- Refer to the dbt notes (dbt.md) for key concepts

## Step 1: Set Up Your Environment
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  
   ```

2. Update pip and install dbt for BigQuery:
   ```bash
   python -m pip install --upgrade pip
   pip install dbt-bigquery
   ```

## Step 2: Configure Google Cloud Credentials
1. Download your BigQuery service account key from the Google Cloud Console and rename it to something like `key.json` (or reuse an existing one).

2. Set the environment variable (replace `/path/to/key.json` with your actual path):
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
   ```
   **Tip**: On Windows, use `set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\key.json` instead.

## Step 3: Initialize dbt Project
1. Create a new directory for your dbt project (e.g., `my_dbt_project`) and navigate into it.

2. Initialize the project:
   ```bash
   dbt init .
   ```
   This generates the standard dbt project structure.

## Step 4: Configure dbt
1. Edit `~/.dbt/profiles.yml` to set your BigQuery region (change from 'EU' to your actual region, e.g., 'us-central1').

2. In your project, create `models/sources.yml` to declare your raw data sources. Example:
   ```yaml
   version: 2
   sources:
     - name: raw
       database: zeta-axiom-468312-f1     # Replace with your GCP project ID
       schema: raw_data                    # Replace with your BigQuery dataset
       tables:
         - name: weather_raw               # Your data tables
         - name: exercise_1_customers      # Note: Corrected spelling from 'excersise' and 'costumers'
         - name: exercise_2_customers
         - name: exercise_1_sessions
         - name: exercise_1_orders
         - name: exercise_1_playlists
   ```

## Step 5: Prepare Sample Data
1. In the root of your project, create a directory: `exercise_data/data`.

2. Create these files inside `data/`:
   - customers.json
   - orders.json
   - playlists.json  # Note: Corrected from 'playlist'
   - sessions.json   # Note: Corrected from 'session'

3. Copy the content from: [https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/dbt_exe_write_data/data](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/dbt_exe_write_data/data)

## Step 6: Upload Data to BigQuery
1. In `exercise_data/`, create two Python scripts to upload data (adjust table names to match your BigQuery tables):
   - `write_data_semi_raw.py`: For uploading customers.json as unpacked rows. Copy from: [https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_semi_raw.py](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_semi_raw.py)
   - `write_data_raw.py`: For uploading all files as nested JSON. Copy from: [https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_raw.py](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_raw.py)

2. Run the scripts:
   ```bash
   python write_data_semi_raw.py
   python write_data_raw.py
   ```

   **Tip**: Ensure your BigQuery dataset exists. If not, create it in the BigQuery console.

## Objective: Create Staging Models
Now that your data is in BigQuery, create staging models for the uploaded data. Start with customers.json.

- **Focus**: Unpacking nested structures, renaming columns, and casting data types.
- Create models for both unnested (from semi-raw script) and nested (from raw script) data. These should result in two different tables in BigQuery.
- You can use SQL (.sql files) or Python (.py files) models in dbt. Note: Python models create tables, while SQL creates views by default.
- Place models in `models/staging/`.
- Run them with: `dbt run -s your_model_name` (replace with your model file name, e.g., stg_customers.sql).

**Tips**:
- If using SQL, test your query directly in the BigQuery console first—dbt runs can take time.
- Use `{{ source('raw', 'table_name') }}` to reference sources.
- Add tests in schema.yml for data validation (e.g., not_null, unique).
- Common pitfalls: Ensure correct casing in table names, handle JSON nesting with UNNEST, and check for authentication errors.

## Verification
1. After running `dbt run`, check BigQuery for your new staging tables.
2. Run `dbt test` if you've added tests.
3. View results in BigQuery console to ensure data is unpacked, renamed, and cast correctly.

If you encounter issues, check the dbt logs (in target/run/) or consult the dbt documentation.

Great job! Once complete, try extending this to the other datasets (orders, playlists, sessions).


