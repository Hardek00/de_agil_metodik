import json
import os
from datetime import datetime
from google.cloud import bigquery
import pandas as pd

class DataTransformer:
    def __init__(self, project_id):
        self.client = bigquery.Client(project=project_id)
        self.project_id = project_id
    
    def extract_schools_from_raw(self, source_dataset, source_table, target_dataset, target_table):
        """
        Transformera RAW data till strukturerad skol-data
        """
        print(f"🔄 Transformerar data från {source_dataset}.{source_table}")
        
        # SQL för att extrahera och strukturera data från RAW
        transform_sql = f"""
        CREATE OR REPLACE TABLE `{self.project_id}.{target_dataset}.{target_table}` AS
        SELECT 
            fetched_at,
            source_url,
            JSON_EXTRACT_SCALAR(school, '$.id') as school_id,
            JSON_EXTRACT_SCALAR(school, '$.name') as school_name,
            JSON_EXTRACT_SCALAR(school, '$.street') as street,
            JSON_EXTRACT_SCALAR(school, '$.postalcode') as postal_code,
            JSON_EXTRACT_SCALAR(school, '$.locality') as locality,
            CAST(JSON_EXTRACT_SCALAR(school, '$.students') AS INT64) as student_count,
            JSON_EXTRACT_SCALAR(school, '$.type') as school_type,
            JSON_EXTRACT_SCALAR(school, '$.operation') as operation_type,
            CAST(JSON_EXTRACT_SCALAR(school, '$.lat') AS FLOAT64) as latitude,
            CAST(JSON_EXTRACT_SCALAR(school, '$.long') AS FLOAT64) as longitude,
            JSON_EXTRACT_SCALAR(school, '$.url') as website_url,
            JSON_EXTRACT_SCALAR(school, '$.source') as source_code,
            
            -- Lägg till beräknade fält
            CASE 
                WHEN JSON_EXTRACT_SCALAR(school, '$.type') = 'FS' THEN 'Förskola'
                WHEN JSON_EXTRACT_SCALAR(school, '$.type') = 'GR' THEN 'Grundskola'
                WHEN JSON_EXTRACT_SCALAR(school, '$.type') = 'FD' THEN 'Familjedaghem'
                ELSE 'Okänd'
            END as school_type_name,
            
            CASE 
                WHEN JSON_EXTRACT_SCALAR(school, '$.operation') = 'K' THEN 'Kommunal'
                WHEN JSON_EXTRACT_SCALAR(school, '$.operation') = 'F' THEN 'Fristående'
                ELSE 'Okänd'
            END as operation_type_name,
            
            -- Kategorisera efter storlek
            CASE 
                WHEN CAST(JSON_EXTRACT_SCALAR(school, '$.students') AS INT64) < 30 THEN 'Liten'
                WHEN CAST(JSON_EXTRACT_SCALAR(school, '$.students') AS INT64) < 100 THEN 'Medel'
                ELSE 'Stor'
            END as size_category,
            
            CURRENT_TIMESTAMP() as transformed_at
            
        FROM `{self.project_id}.{source_dataset}.{source_table}`,
        UNNEST(JSON_EXTRACT_ARRAY(raw_json, '$.results')) as school
        WHERE DATE(fetched_at) = CURRENT_DATE()  -- Bara dagens data
        """
        
        # Kör transformation
        job = self.client.query(transform_sql)
        job.result()
        
        # Kontrollera resultat
        result_table = self.client.get_table(f"{self.project_id}.{target_dataset}.{target_table}")
        print(f"✅ Transformation klar!")
        print(f"📊 Skapade {result_table.num_rows} strukturerade rader")
        
        return result_table.num_rows
    
    def create_analytics_views(self, dataset_id, table_id):
        """
        Skapa analytiska vyer för enkel rapportering
        """
        print("📈 Skapar analytiska vyer...")
        
        # View 1: Sammanfattning per typ
        summary_sql = f"""
        CREATE OR REPLACE VIEW `{self.project_id}.{dataset_id}.school_summary` AS
        SELECT 
            school_type_name,
            operation_type_name,
            COUNT(*) as antal_enheter,
            SUM(student_count) as totalt_antal_barn,
            AVG(student_count) as genomsnitt_barn_per_enhet,
            MIN(student_count) as minsta_enhet,
            MAX(student_count) as storsta_enhet
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        GROUP BY school_type_name, operation_type_name
        ORDER BY totalt_antal_barn DESC
        """
        
        # View 2: Geografisk fördelning
        geo_sql = f"""
        CREATE OR REPLACE VIEW `{self.project_id}.{dataset_id}.school_geography` AS
        SELECT 
            locality,
            school_type_name,
            COUNT(*) as antal_enheter,
            SUM(student_count) as totalt_barn,
            ARRAY_AGG(school_name ORDER BY student_count DESC LIMIT 3) as storsta_enheterna
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        GROUP BY locality, school_type_name
        ORDER BY locality, totalt_barn DESC
        """
        
        # View 3: Storlekskategorier
        size_sql = f"""
        CREATE OR REPLACE VIEW `{self.project_id}.{dataset_id}.school_sizes` AS
        SELECT 
            size_category,
            school_type_name,
            COUNT(*) as antal_enheter,
            AVG(student_count) as genomsnittlig_storlek,
            STRING_AGG(school_name, ', ' ORDER BY student_count DESC) as enheter
        FROM `{self.project_id}.{dataset_id}.{table_id}`
        GROUP BY size_category, school_type_name
        ORDER BY 
            CASE size_category 
                WHEN 'Liten' THEN 1 
                WHEN 'Medel' THEN 2 
                WHEN 'Stor' THEN 3 
            END,
            school_type_name
        """
        
        # Kör alla vyer
        for view_name, sql in [
            ("summary", summary_sql),
            ("geography", geo_sql), 
            ("sizes", size_sql)
        ]:
            job = self.client.query(sql)
            job.result()
            print(f"  ✓ Skapade view: {dataset_id}.school_{view_name}")
        
        print("📊 Alla analytiska vyer skapade!")

def main():
    """
    Kör transformation pipeline
    """
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "din-project-id")
    
    print("=== Data Transformation Pipeline ===")
    print(f"Projekt: {PROJECT_ID}")
    print()
    
    transformer = DataTransformer(PROJECT_ID)
    
    try:
        # 1. Transformera RAW data till strukturerad data
        rows_created = transformer.extract_schools_from_raw(
            source_dataset="raw_data",
            source_table="sample_data", 
            target_dataset="processed_data",
            target_table="schools_structured"
        )
        
        # 2. Skapa analytiska vyer
        transformer.create_analytics_views("processed_data", "schools_structured")
        
        print()
        print("🎉 Transformation Pipeline Klar!")
        print("🔍 Testa med dessa queries:")
        print(f"   SELECT * FROM `{PROJECT_ID}.processed_data.school_summary`")
        print(f"   SELECT * FROM `{PROJECT_ID}.processed_data.school_geography`") 
        print(f"   SELECT * FROM `{PROJECT_ID}.processed_data.school_sizes`")
        
    except Exception as e:
        print(f"❌ Transformation fel: {e}")
        raise

if __name__ == "__main__":
    main()