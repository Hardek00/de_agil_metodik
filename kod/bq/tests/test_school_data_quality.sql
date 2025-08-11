-- Test: Alla skolor borde ha namn
SELECT school_id
FROM {{ ref('dim_schools') }}
WHERE school_name IS NULL 
   OR TRIM(school_name) = ''