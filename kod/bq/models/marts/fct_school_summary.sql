{{
  config(
    materialized='table',
    description='Faktatabell med aggregerad skolstatistik'
  )
}}

SELECT 
    -- Dimensioner
    school_type_name,
    operation_type_name,
    size_category,
    locality,
    
    -- Aggregerade mått
    COUNT(*) as school_count,
    COUNT(CASE WHEN student_count IS NOT NULL THEN 1 END) as schools_with_student_data,
    
    -- Student statistik
    SUM(COALESCE(student_count, 0)) as total_students,
    AVG(student_count) as avg_students_per_school,
    MIN(student_count) as min_students,
    MAX(student_count) as max_students,
    
    -- Geografisk spridning
    COUNT(DISTINCT locality) as localities_covered,
    
    -- Metadata
    MAX(fetched_at) as latest_data_date,
    CURRENT_TIMESTAMP() as summary_created_at

FROM {{ ref('dim_schools') }}

GROUP BY 
    school_type_name,
    operation_type_name, 
    size_category,
    locality

ORDER BY 
    total_students DESC,
    school_count DESC