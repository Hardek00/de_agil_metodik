{% macro test_data_freshness(model, column_name, max_age_hours=24) %}

    SELECT COUNT(*)
    FROM {{ model }}
    WHERE {{ column_name }} < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {{ max_age_hours }} HOUR)

{% endmacro %}