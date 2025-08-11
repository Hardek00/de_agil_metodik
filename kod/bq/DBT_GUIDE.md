# dbt (data build tool) - Komplett Guide

## 🎯 Vad är dbt?

dbt (data build tool) är **branschstandard** för **transformationer** i moderna ELT-pipelines. Istället för att skriva Python-scripts för att transformera data, använder vi SQL och dbt:s kraftfulla funktioner.

### Grundkonceptet:
```
RAW Data (BigQuery) → dbt (SQL transformations) → Analytics-ready Data
```

## 🏗️ dbt Projektstruktur

```
dbt_project/
├── dbt_project.yml          # Projektkonfiguration
├── profiles.yml             # Databasinställningar  
├── models/                  # SQL-filer för transformationer
│   ├── staging/             # Första nivån: clean RAW data
│   └── marts/               # Andra nivån: business logic
├── tests/                   # Data quality tester
├── macros/                  # Återanvändbara SQL-funktioner
└── seeds/                   # Statisk data (CSV-filer)
```

## 📋 Steg 1: Projektinställning

### 1.1 `dbt_project.yml` - Huvudkonfiguration
```yaml
# Projektet heter 'tomelilla_schools'
name: 'tomelilla_schools'
version: '1.0.0'
config-version: 2

# Vilken profil används (kopplar till profiles.yml)
profile: 'tomelilla_schools'

# Var ligger olika typer av filer
model-paths: ["models"]
test-paths: ["tests"]
macro-paths: ["macros"]

# Konfiguration för models
models:
  tomelilla_schools:
    +materialized: table      # Default: skapa tabeller
    staging:
      +materialized: view     # Staging: skapa vyer (snabbare)
    marts:
      +materialized: table    # Marts: skapa tabeller (performance)
```

### 1.2 `profiles.yml` - Databasanslutning
```yaml
tomelilla_schools:
  target: dev                          # Default environment
  outputs:
    dev:                              # Development environment
      type: bigquery
      method: service-account
      keyfile: /app/service-account-key.json
      project: zeta-axiom-468312-f1
      dataset: dbt_dev                # Alla dbt-tabeller hamnar här
      threads: 4
      location: EU
    prod:                            # Production environment  
      type: bigquery
      method: service-account
      keyfile: /app/service-account-key.json
      project: zeta-axiom-468312-f1
      dataset: dbt_prod              # Prod-data hamnar här
      location: EU
```

## 📂 Steg 2: Sources - Definiera RAW Data

### 2.1 `models/staging/_sources.yml`
```yaml
version: 2

sources:
  - name: raw_data                    # Namnet på vårt RAW dataset
    description: Raw data från våra API-källor
    tables:
      - name: sample_data             # Vår RAW tabell
        description: RAW skol- och förskoledata från Tomelilla
        columns:
          - name: fetched_at
            description: När data hämtades
            tests:
              - not_null              # Data quality test
          - name: source_url
            description: URL till datakällan
          - name: raw_json
            description: Hela API-responsen som JSON-sträng
            tests:
              - not_null
```

**Vad händer:** 
- Vi berättar för dbt var vår RAW data ligger
- Vi definierar kolumner och deras betydelse
- Vi lägger till basic data quality tester

## 🧹 Steg 3: Staging - Rensa och Extrahera

### 3.1 `models/staging/stg_schools_raw.sql`
```sql
{{
  config(
    materialized='view',
    description='Staging: Extraherar strukturerad data från RAW JSON'
  )
}}

WITH raw_schools AS (
    -- Hämta RAW data från source
    SELECT 
        fetched_at,
        source_url,
        raw_json
    FROM {{ source('raw_data', 'sample_data') }}  -- dbt referens till source
    WHERE DATE(fetched_at) = CURRENT_DATE()       -- Bara dagens data
),

extracted_schools AS (
    -- Extrahera individual skolor från JSON array
    SELECT 
        fetched_at,
        source_url,
        school_data
    FROM raw_schools,
    UNNEST(JSON_EXTRACT_ARRAY(raw_json, '$.results')) AS school_data
)

-- Extrahera alla fält från JSON till kolumner
SELECT 
    fetched_at,
    source_url,
    
    -- Grundläggande fält
    JSON_EXTRACT_SCALAR(school_data, '$.id') as school_id,
    JSON_EXTRACT_SCALAR(school_data, '$.name') as school_name,
    JSON_EXTRACT_SCALAR(school_data, '$.street') as street,
    JSON_EXTRACT_SCALAR(school_data, '$.postalcode') as postal_code,
    JSON_EXTRACT_SCALAR(school_data, '$.locality') as locality,
    JSON_EXTRACT_SCALAR(school_data, '$.type') as school_type_code,
    JSON_EXTRACT_SCALAR(school_data, '$.operation') as operation_code,
    JSON_EXTRACT_SCALAR(school_data, '$.url') as website_url,
    JSON_EXTRACT_SCALAR(school_data, '$.source') as source_code,
    
    -- Numeriska fält (med säker casting)
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.students') AS INT64) as student_count,
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.lat') AS FLOAT64) as latitude,
    SAFE_CAST(JSON_EXTRACT_SCALAR(school_data, '$.long') AS FLOAT64) as longitude,
    
    CURRENT_TIMESTAMP() as processed_at

FROM extracted_schools
```

**Vad händer:**
1. **CTE (Common Table Expression)** → Organiserar SQL i steg
2. **source()** → dbt-funktion som refererar till våra sources
3. **JSON extraction** → Parsar RAW JSON till strukturerade kolumner
4. **SAFE_CAST** → Konverterar säkert (NULL om det misslyckas)

## 🏢 Steg 4: Marts - Business Logic

### 4.1 `models/marts/dim_schools.sql` - Dimension Tabell
```sql
{{
  config(
    materialized='table',
    description='Dimension tabell för skolor med berikad data'
  )
}}

WITH school_base AS (
    -- Hämta från staging
    SELECT * FROM {{ ref('stg_schools_raw') }}  -- dbt referens till annan model
),

enriched_schools AS (
    SELECT 
        *,
        
        -- Berika school_type med human-readable namn
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
        
        -- Skapa business key för uniqueness
        CONCAT(school_type_code, '-', operation_code, '-', school_id) as school_business_key
        
    FROM school_base
)

SELECT 
    -- Primary Key (genererad av dbt)
    {{ dbt_utils.generate_surrogate_key(['school_business_key', 'fetched_at']) }} as school_key,
    
    -- Business Key
    school_business_key,
    
    -- Alla andra fält...
    school_id,
    school_name,
    street,
    postal_code, 
    locality,
    school_type_code,
    school_type_name,
    operation_code,
    operation_type_name,
    size_category,
    student_count,
    latitude,
    longitude,
    website_url,
    source_code,
    source_url,
    fetched_at,
    processed_at

FROM enriched_schools
```

### 4.2 `models/marts/fct_school_summary.sql` - Faktatabell
```sql
{{
  config(
    materialized='table',
    description='Faktatabell med aggregerad skolstatistik'
  )
}}

SELECT 
    -- Dimensioner (GROUP BY)
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
    
    -- Metadata
    MAX(fetched_at) as latest_data_date,
    CURRENT_TIMESTAMP() as summary_created_at

FROM {{ ref('dim_schools') }}  -- Referens till dimension tabellen

GROUP BY 
    school_type_name,
    operation_type_name, 
    size_category,
    locality

ORDER BY 
    total_students DESC
```

**Vad händer:**
1. **ref()** → dbt-funktion som refererar till andra models
2. **Enrichment** → Lägger till business logic och beräkningar
3. **Surrogate keys** → Genererar tekniska nycklar
4. **Aggregations** → Skapar summary-tabeller för analys

## 🧪 Steg 5: Tests - Data Quality

### 5.1 `tests/test_school_data_quality.sql`
```sql
-- Test: Alla skolor borde ha namn
SELECT school_id
FROM {{ ref('dim_schools') }}
WHERE school_name IS NULL 
   OR TRIM(school_name) = ''
```

### 5.2 Inbyggda tester i schema.yml
```yaml
# I models/staging/schema.yml
version: 2

models:
  - name: stg_schools_raw
    columns:
      - name: school_id
        tests:
          - unique          # Ska vara unik
          - not_null        # Får inte vara NULL
      - name: student_count
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000
```

## 🔧 Steg 6: Macros - Återanvändbar Kod

### 6.1 `macros/test_data_freshness.sql`
```sql
{% macro test_data_freshness(model, column_name, max_age_hours=24) %}

    SELECT COUNT(*)
    FROM {{ model }}
    WHERE {{ column_name }} < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {{ max_age_hours }} HOUR)

{% endmacro %}
```

**Användning:**
```sql
SELECT {{ test_data_freshness('dim_schools', 'fetched_at', 12) }} as old_data_count
```

## 🚀 Steg 7: Kör dbt

### 7.1 Setup Dependencies
```bash
# Installera dbt packages (om de används)
dbt deps

# Bygger alla models i ordning
dbt run

# Kör alla tester
dbt test

# Bygg dokumentation
dbt docs generate

# Visa dokumentation
dbt docs serve
```

### 7.2 Selektiv Körning
```bash
# Bara staging models
dbt run --models staging

# Bara en specifik model
dbt run --models dim_schools

# Bara models som ändrats
dbt run --select state:modified

# Bara downstream från en model
dbt run --models +dim_schools+
```

## 🐳 Steg 8: Docker Integration

### 8.1 `requirements.txt`
```txt
dbt-core==1.7.0
dbt-bigquery==1.7.0
```

### 8.2 `docker-compose-dbt.yml`
```yaml
version: '3.8'

services:
  dbt-transform:
    build: .
    command: sh -c "dbt deps && dbt run && dbt test"
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account-key.json
      - GCP_PROJECT_ID=zeta-axiom-468312-f1
      - DBT_PROFILES_DIR=/app                    # Var profiles.yml ligger
    volumes:
      - ./service-account-key.json:/app/service-account-key.json:ro
      - .:/app                                   # Hela projekt-mappen
```

## 🎯 Dataflöde - Slutresultat

```
RAW: raw_data.sample_data (JSON blob)
     ↓
STAGING: dbt_dev.stg_schools_raw (strukturerade rader)
     ↓
MARTS: dbt_dev.dim_schools (berikad dimension data)
     ↓
MARTS: dbt_dev.fct_school_summary (aggregerad data)
```

## 📊 Använda Resultatet

```sql
-- Vilka är de största förskolorna?
SELECT school_name, student_count, locality
FROM dbt_dev.dim_schools 
WHERE school_type_name = 'Förskola'
ORDER BY student_count DESC

-- Sammanfattning per typ och drift
SELECT * FROM dbt_dev.fct_school_summary
ORDER BY total_students DESC
```

## 🏆 Fördelar med denna Approach

### **vs Python Scripts:**
- ✅ **SQL-baserat** → Lättare för data analysts
- ✅ **Deklarativt** → Fokus på "vad", inte "hur"  
- ✅ **Testbart** → Inbyggda data quality checks
- ✅ **Dokumenterat** → Auto-genererad docs
- ✅ **Modulärt** → Återanvändbara komponenter
- ✅ **Lineage** → Visar hur data flödar

### **vs Manual SQL:**
- ✅ **Version control** → Git workflow
- ✅ **Dependencies** → Rätt körningsordning  
- ✅ **Testing** → Automatiska validationer
- ✅ **Documentation** → Håller sig uppdaterad
- ✅ **Environments** → Dev/Staging/Prod

## 🎉 Sammanfattning

dbt tar **SQL-transformationer** och gör dem:
- **Organiserade** (models, tests, docs)
- **Säkra** (tests och validering)
- **Repeterbara** (samma resultat varje gång)
- **Spårbara** (lineage och dokumentation)

Detta är varför dbt är **industry standard** för moderna data teams! 🚀