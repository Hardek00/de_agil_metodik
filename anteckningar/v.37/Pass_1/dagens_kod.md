# Dagens Kod: dbt Exempel och Resurser

## Data för Övningar
- [Sample data files](https://github.com/Hardek00/demo_ingestion_pipeline/tree/main/dbt_exe_write_data/data)

## Helper Scripts för Datauppladdning till BigQuery
**OBS!** Se till att uppdatera scripten med dina egna tabeller och dataset.

- [write_data_raw.py (för nested JSON)](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_raw.py)
- [write_data_semi_raw.py (för unnested JSON, endast customers.json)](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt_exe_write_data/write_data_semi_raw.py)

## Exempel på dbt Staging Models
- **För primitiv (unnested) JSON**: [stg_customers.sql](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt/models/staging/stg_customers.sql)
- **För nested JSON**: [stg_customers_raw.sql](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt/models/staging/stg_customers_raw.sql)
- **För väderdata**: [stg_weather_raw.sql](https://github.com/Hardek00/demo_ingestion_pipeline/blob/main/dbt/models/staging/stg_weather_raw.sql)

Dessa exempel kan användas som referens för att bygga dina egna staging models i övningen.


