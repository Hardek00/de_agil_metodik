{{
  config(
    materialized='table',
    description='Dimension tabell för skolor med berikad data'
  )
}}

WITH school_base AS (
    SELECT * FROM {{ ref('stg_schools_raw') }}
),

enriched_schools AS (
    SELECT 
        *,
        
        -- Berika school_type
        CASE 
            WHEN school_type_code = 'FS' THEN 'Förskola'
            WHEN school_type_code = 'GR' THEN 'Grundskola'  
            WHEN school_type_code = 'FD' THEN 'Familjedaghem'
            ELSE 'Okänd'
        END as school_type_name,
        
        -- Berika operation_type  
        CASE 
            WHEN operation_code = 'K' THEN 'Kommunal'
            WHEN operation_code = 'F' THEN 'Fristående'
            ELSE 'Okänd'
        END as operation_type_name,
        
        -- Kategorisera efter storlek
        CASE 
            WHEN student_count IS NULL THEN 'Okänd'
            WHEN student_count < 30 THEN 'Liten' 
            WHEN student_count < 100 THEN 'Medel'
            ELSE 'Stor'
        END as size_category,
        
        -- Skapa unik business key
        CONCAT(school_type_code, '-', operation_code, '-', school_id) as school_business_key
        
    FROM school_base
)

SELECT 
    -- Primary Key
    {{ dbt_utils.generate_surrogate_key(['school_business_key', 'fetched_at']) }} as school_key,
    
    -- Business Key
    school_business_key,
    
    -- Identifiers
    school_id,
    school_name,
    
    -- Address
    street,
    postal_code, 
    locality,
    
    -- School Info
    school_type_code,
    school_type_name,
    operation_code,
    operation_type_name,
    size_category,
    
    -- Metrics
    student_count,
    
    -- Geography
    latitude,
    longitude,
    
    -- Web
    website_url,
    
    -- Metadata
    source_code,
    source_url,
    fetched_at,
    processed_at

FROM enriched_schools