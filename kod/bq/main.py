import requests
import json
from datetime import datetime
from google.cloud import bigquery
import os

def fetch_tomelilla_schools_data():
    """Hämta skol- och förskolaData från Tomelilla kommun"""
    url = "https://data.tomelilla.se/rowstore/dataset/3617552e-4c28-4a46-9b74-ac8bbbfee33f"
    
    print("Hämtar data från Tomelilla kommun...")
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    print(f"Hämtade {data['resultCount']} skolor och förskolor")
    
    return data

def upload_raw_to_bigquery(data, project_id, dataset_id, table_id):
    """Ladda upp RAW data till BigQuery"""
    client = bigquery.Client(project=project_id)
    
    # Skapa dataset om det inte finns
    dataset_ref = client.dataset(dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_id} finns redan")
    except:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "EU"
        client.create_dataset(dataset)
        print(f"Skapade dataset {dataset_id}")
    
    # Definiera tabell-referens
    table_ref = dataset_ref.table(table_id)
    
    # Äkta RAW data - bara metadata + hela JSON-responsen som en blob
    raw_record = {
        "fetched_at": datetime.utcnow().isoformat(),
        "source_url": "https://data.tomelilla.se/rowstore/dataset/3617552e-4c28-4a46-9b74-ac8bbbfee33f",
        "raw_json": json.dumps(data)  # Hela API-responsen som en stor JSON-sträng
    }
    
    # Konfigurera BigQuery job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True
    )
    
    # Ladda upp RAW record
    job = client.load_table_from_json([raw_record], table_ref, job_config=job_config)
    job.result()  # Vänta på att jobbet ska slutföras
    
    # Kontrollera resultat
    table = client.get_table(table_ref)
    print(f"Laddade upp data till {project_id}.{dataset_id}.{table_id}")
    print(f"Tabellen har nu {table.num_rows} rader")

def main():
    # Konfiguration
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "din-project-id")
    DATASET_ID = "raw_data"
    TABLE_ID = "sample_data"
    
    print("=== Tomelilla Skol- och Förskoledata Pipeline ===")
    print(f"Projekt: {PROJECT_ID}")
    print(f"Dataset: {DATASET_ID}")
    print(f"Tabell: {TABLE_ID}")
    print()
    
    try:
        # 1. Hämta data
        schools_data = fetch_tomelilla_schools_data()
        
        # 2. Ladda upp RAW till BigQuery
        upload_raw_to_bigquery(schools_data, PROJECT_ID, DATASET_ID, TABLE_ID)
        
        print("✅ Pipeline klar!")
        print(f"Kolla data i BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")
        
    except Exception as e:
        print(f"❌ Fel: {e}")
        raise

if __name__ == "__main__":
    main()
