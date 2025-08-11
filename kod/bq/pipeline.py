#!/usr/bin/env python3
"""
Komplett ELT Pipeline: Extract -> Load -> Transform
"""

import os
import sys
from main import fetch_tomelilla_schools_data, upload_raw_to_bigquery
from transform import DataTransformer

def run_full_pipeline():
    """
    Kör hela ELT-pipelinen i rätt ordning
    """
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "din-project-id")
    
    print("🚀 === FULLSTÄNDIG ELT PIPELINE ===")
    print(f"📍 Projekt: {PROJECT_ID}")
    print()
    
    try:
        # === E: EXTRACT + LOAD ===
        print("1️⃣ === EXTRACT & LOAD (RAW DATA) ===")
        
        # Hämta data från API
        schools_data = fetch_tomelilla_schools_data()
        
        # Ladda upp RAW till BigQuery
        upload_raw_to_bigquery(
            data=schools_data,
            project_id=PROJECT_ID,
            dataset_id="raw_data", 
            table_id="sample_data"
        )
        
        print("✅ Extract & Load klar!")
        print()
        
        # === T: TRANSFORM ===
        print("2️⃣ === TRANSFORM (STRUCTURED DATA) ===")
        
        transformer = DataTransformer(PROJECT_ID)
        
        # Transformera RAW till strukturerad data
        rows_created = transformer.extract_schools_from_raw(
            source_dataset="raw_data",
            source_table="sample_data",
            target_dataset="processed_data", 
            target_table="schools_structured"
        )
        
        # Skapa analytiska vyer
        transformer.create_analytics_views("processed_data", "schools_structured")
        
        print("✅ Transform klar!")
        print()
        
        # === SAMMANFATTNING ===
        print("🎉 === PIPELINE KOMPLETT! ===")
        print()
        print("📊 Data nu tillgänglig:")
        print(f"   🗄️  RAW: `{PROJECT_ID}.raw_data.sample_data`")
        print(f"   📋 STRUCTURED: `{PROJECT_ID}.processed_data.schools_structured`")
        print()
        print("📈 Analytiska Vyer:")
        print(f"   📊 `{PROJECT_ID}.processed_data.school_summary`")
        print(f"   🗺️  `{PROJECT_ID}.processed_data.school_geography`") 
        print(f"   📏 `{PROJECT_ID}.processed_data.school_sizes`")
        print()
        print("🔍 Testa i BigQuery:")
        print("   SELECT * FROM `processed_data.school_summary`")
        print("   SELECT * FROM `processed_data.school_geography` WHERE locality = 'Tomelilla'")
        print("   SELECT * FROM `processed_data.school_sizes` WHERE size_category = 'Stor'")
        
    except Exception as e:
        print(f"❌ Pipeline misslyckades: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_full_pipeline()