{{
  config(
    materialized='view',
    description='Staging: Extraherar strukturerad data från RAW JSON'
  )
}}

WITH raw_schools AS (
    SELECT 
        fetched_at,
        source_url,
        raw_json
    FROM {{ source('raw_data', 'sample_data') }}
    WHERE DATE(fetched_at) = CURRENT_DATE()  -- Bara dagens data
),

extracted_schools AS (
    SELECT 
        fetched_at,
        source_url,
        school_data
    FROM raw_schools,
    UNNEST(JSON_EXTRACT_ARRAY(raw_json, '$.results')) AS school_data
)

SELECT 
    fetched_at,
    source_url,
    
    -- Extrahera grundläggande fält
    JSON_EXTRACT_SCALAR(school_data, '$.id') as school_id,
    JSON_EXTRACT_SCALAR(school_data, '$.name') as school_name,
    JSON_EXTRACT_SCALAR(school_data, '$.street') as street,
    JSON_EXTRACT_SCALAR(school_data, '$.postalcode') as postal_code,
    JSON_EXTRACT_SCALAR(school_data, '$.locality') as locality,
    JSON_EXTRACT_SCALAR(school_data, '$.type') as school_type_code,
    JSON_EXTRACT_SCALAR(school_data, '$.operation') as operation_code,
    JSON_EXTRACT_SCALAR(school_data, '$.url') as website_url,
    JSON_EXTRACT_SCALAR(school_data, '$.source') as source_code,
    
    -- Numeriska fält
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.students') AS INT64) as student_count,
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.lat') AS FLOAT64) as latitude,
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.long') AS FLOAT64) as longitude,
    
    CURRENT_TIMESTAMP() as processed_at

FROM extracted_schools