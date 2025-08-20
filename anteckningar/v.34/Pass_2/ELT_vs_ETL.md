# ETL vs ELT - Data Processing Strategier

## Vad är ETL och ELT?

### ETL (Extract, Transform, Load)
**Traditionella metoden:** Bearbeta data INNAN den laddas in i måldatabasen.

```
Datakällor → EXTRACT → TRANSFORM → LOAD → Data Warehouse
```

### ELT (Extract, Load, Transform)
**Moderna metoden:** Ladda in rådata FÖRST, bearbeta sedan i måldatabasen.

```
Datakällor → EXTRACT → LOAD → TRANSFORM → Data Warehouse
```

---

## Grundläggande Skillnader

### ETL-flöde
```
1. EXTRACT: Hämta data från källor
   ├── API-calls
   ├── Databasfrågor  
   └── Fil-läsning

2. TRANSFORM: Bearbeta data (utanför måldatabasen)
   ├── Rensa data
   ├── Validera format
   ├── Konvertera typer
   ├── Aggregera värden
   └── Kombinera tabeller

3. LOAD: Ladda färdig data
   └── Skriv till data warehouse
```

### ELT-flöde
```
1. EXTRACT: Hämta data från källor
   ├── API-calls
   ├── Databasfrågor
   └── Fil-läsning

2. LOAD: Ladda rådata direkt
   └── Skriv till data warehouse (utan transformation)

3. TRANSFORM: Bearbeta data (inne i måldatabasen)
   ├── SQL-queries för rensning
   ├── Views för aggregering
   ├── Stored procedures
   └── dbt transformations
```

---

## Praktiska Exempel

### Scenario: E-handelsdata
Vi har försäljningsdata från olika källor som ska analyseras.

#### ETL-approach
```python
# ETL Pipeline Example
import pandas as pd
from datetime import datetime

def etl_pipeline():
    # 1. EXTRACT - Hämta data från olika källor
    orders_api = fetch_from_api('https://api.shop.com/orders')
    customers_db = fetch_from_database('SELECT * FROM customers')
    products_csv = pd.read_csv('products.csv')
    
    # 2. TRANSFORM - Bearbeta data utanför måldatabasen
    # Rensa ordrar
    orders_clean = clean_orders(orders_api)
    
    # Validera kunder
    customers_valid = validate_customers(customers_db)
    
    # Kombinera data
    enriched_orders = orders_clean.merge(customers_valid, on='customer_id')
    enriched_orders = enriched_orders.merge(products_csv, on='product_id')
    
    # Aggregera månadsdata
    monthly_sales = enriched_orders.groupby([
        enriched_orders['order_date'].dt.to_period('M'),
        'product_category'
    ]).agg({
        'total_amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    # 3. LOAD - Ladda färdig, bearbetad data
    load_to_warehouse(monthly_sales, table='monthly_sales_summary')

def clean_orders(orders_data):
    """Rensa och validera orderdata"""
    df = pd.DataFrame(orders_data)
    
    # Ta bort dubbletter
    df = df.drop_duplicates(subset=['order_id'])
    
    # Konvertera datum
    df['order_date'] = pd.to_datetime(df['order_date'])
    
    # Filtrera bort ogiltiga ordrar
    df = df[df['total_amount'] > 0]
    
    return df

# Kör ETL-pipeline
etl_pipeline()
```

#### ELT-approach
```python
# ELT Pipeline Example
def elt_pipeline():
    # 1. EXTRACT - Hämta data
    orders_api = fetch_from_api('https://api.shop.com/orders')
    customers_db = fetch_from_database('SELECT * FROM customers')
    products_csv = pd.read_csv('products.csv')
    
    # 2. LOAD - Ladda rådata direkt till warehouse
    load_raw_data(orders_api, table='raw_orders')
    load_raw_data(customers_db, table='raw_customers') 
    load_raw_data(products_csv, table='raw_products')
    
    # 3. TRANSFORM - Bearbeta med SQL i databasen
    execute_transformations()

def execute_transformations():
    """Kör transformationer i data warehouse med SQL"""
    
    # Steg 1: Rensa rådata
    sql_clean_orders = """
    CREATE OR REPLACE VIEW clean_orders AS
    SELECT DISTINCT
        order_id,
        customer_id,
        product_id,
        CAST(order_date AS DATE) as order_date,
        total_amount
    FROM raw_orders 
    WHERE total_amount > 0
      AND order_date IS NOT NULL
    """
    
    # Steg 2: Kombinera data
    sql_enriched_orders = """
    CREATE OR REPLACE VIEW enriched_orders AS
    SELECT 
        o.order_id,
        o.order_date,
        o.total_amount,
        c.customer_name,
        c.customer_segment,
        p.product_name,
        p.product_category
    FROM clean_orders o
    JOIN raw_customers c ON o.customer_id = c.customer_id
    JOIN raw_products p ON o.product_id = p.product_id
    """
    
    # Steg 3: Skapa aggregerad tabell
    sql_monthly_summary = """
    CREATE OR REPLACE TABLE monthly_sales_summary AS
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        product_category,
        SUM(total_amount) as total_sales,
        COUNT(order_id) as order_count
    FROM enriched_orders
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    
    # Exekvera SQL-kommandon
    execute_sql(sql_clean_orders)
    execute_sql(sql_enriched_orders)
    execute_sql(sql_monthly_summary)

# Kör ELT-pipeline
elt_pipeline()
```

---

## Fördelar och Nackdelar

### ETL Fördelar ✅
- **Kvalitetskontroll**: Data valideras innan det når warehouse
- **Säkerhet**: Känslig data kan rensas/maskeras innan lagring
- **Bandbredd**: Mindre data skickas till warehouse
- **Kompatibilitet**: Fungerar med äldre system och mindre databaser
- **Kontroll**: Exakt kontroll över vad som lagras

### ETL Nackdelar ❌
- **Bearbetningstid**: Långsammare - all transformation före load
- **Skalbarhet**: Begränsad av transform-serverns kapacitet
- **Flexibilitet**: Svårt att ändra transformationer i efterhand
- **Historisk data**: Förlorar rådata om transformation ändras
- **Kostnader**: Behöver kraftfull transform-server

### ELT Fördelar ✅
- **Prestanda**: Utnyttjar moderna data warehouse-prestanda
- **Skalbarhet**: Warehouse kan hantera massiv data
- **Flexibilitet**: Kan transformera data på olika sätt i efterhand
- **Historisk data**: Behåller alltid originaldata
- **Snabbhet**: Snabbare att få in rådata
- **Kostnadseffektivt**: Utnyttjar cloud-computing optimalt

### ELT Nackdelar ❌
- **Storage-kostnader**: Lagrar all rådata (även "dålig" data)
- **Säkerhet**: Rådata med känslig information lagras
- **Komplexitet**: Kräver avancerat data warehouse
- **Datavalidering**: Risk för "garbage in, garbage out"

---

## Tekniska Skillnader

### ETL-verktyg och teknologier
```python
# Traditionella ETL-verktyg
Enterprise:
- Informatica PowerCenter
- IBM DataStage  
- Microsoft SSIS
- Talend

Open Source:
- Apache Airflow (orchestration)
- Apache Nifi
- Pentaho Data Integration
- Luigi

Cloud:
- AWS Glue
- Azure Data Factory
- Google Cloud Dataflow
```

### ELT-verktyg och teknologier
```python
# Moderna ELT-verktyg
Data Warehouses:
- Snowflake
- BigQuery
- Amazon Redshift
- Azure Synapse

Transform-verktyg:
- dbt (data build tool)
- Dataform
- Apache Spark (för stora volymer)
- SQL-baserade transformationer

Orchestration:
- Airflow
- Prefect
- Dagster
```

### Kod-exempel: dbt för ELT-transformationer
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='view') }}

SELECT 
    order_id,
    customer_id,
    product_id,
    CAST(order_date AS DATE) as order_date,
    total_amount,
    CURRENT_TIMESTAMP() as loaded_at
FROM {{ source('raw', 'orders') }}
WHERE total_amount > 0
  AND order_date IS NOT NULL

-- models/marts/monthly_sales.sql
{{ config(materialized='table') }}

SELECT 
    DATE_TRUNC('month', o.order_date) as month,
    p.product_category,
    SUM(o.total_amount) as total_sales,
    COUNT(o.order_id) as order_count,
    COUNT(DISTINCT o.customer_id) as unique_customers
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_products') }} p 
  ON o.product_id = p.product_id
GROUP BY 1, 2
ORDER BY 1, 2
```

---

## När ska man använda vilken?

### Använd ETL när: 🔧
- **Äldre system** som inte klarar stora datamängder
- **Säkerhetskrav** - känslig data måste rensas innan lagring
- **Begränsad storage** - inte råd att lagra all rådata
- **Komplexa transformationer** som kräver specialverktyg
- **Reglering** kräver datavalidering före lagring
- **Begränsad bandbredd** mellan källa och mål

**Exempel:**
```
- Bankdata med PII som måste maskeras
- Legacy system med begränsad kapacitet
- Reglerade industrier (hälsa, finans)
- Embedded system med minimal storage
```

### Använd ELT när: ⚡
- **Moderna cloud data warehouses** (BigQuery, Snowflake)
- **Stora datavolymer** som behöver skalas
- **Snabb time-to-insight** - vill komma åt rådata snabbt
- **Flexibla analys-behov** - olika sätt att transformera data
- **Self-service analytics** - analytiker vill transformera själva
- **Realtids-/near-realtime data**

**Exempel:**
```
- IoT sensor-data i stor skala
- E-handelsanalys med varierande behov
- Machine learning pipelines
- Business intelligence för olika team
```

---

## Hybrid-approaches

### Lambda Architecture
Kombinerar batch och streaming:
```
Datakällor → Batch Layer (ETL) → Serving Layer
           ↘ Speed Layer (ELT) ↗
```

### Kappa Architecture  
Allt via streaming (ELT-approach):
```
Datakällor → Stream Processing → Serving Layer
```

### EtLT (Extract, transform, Load, Transform)
Minimal transformation, sedan mer transformation:
```
Källdata → Basic Clean → Load → Advanced Transform
```

**Exempel EtLT:**
```python
def etlt_pipeline():
    # 1. Extract
    raw_data = extract_from_api()
    
    # 2. Basic transform (minimal cleaning)
    cleaned_data = basic_clean(raw_data)  # Remove nulls, fix formats
    
    # 3. Load to staging
    load_to_staging(cleaned_data)
    
    # 4. Advanced transform in warehouse
    execute_sql_transformations()  # Complex business logic
```

---

## Praktisk Implementation

### ETL med Pandas + BigQuery
```python
import pandas as pd
from google.cloud import bigquery

def etl_to_bigquery():
    # Extract
    df = pd.read_csv('sales_data.csv')
    
    # Transform
    df['order_date'] = pd.to_datetime(df['order_date'])
    df = df[df['amount'] > 0]  # Filter invalid orders
    
    # Aggregera till månadsdata
    monthly = df.groupby([
        df['order_date'].dt.to_period('M'),
        'product_category'
    ]).agg({
        'amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    # Load
    client = bigquery.Client()
    table_id = "my-project.my_dataset.monthly_sales"
    
    job = client.load_table_from_dataframe(
        monthly, table_id, 
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE"
        )
    )
    job.result()
```

### ELT med BigQuery
```python
def elt_to_bigquery():
    # Extract & Load rådata
    df = pd.read_csv('sales_data.csv')
    
    client = bigquery.Client()
    raw_table = "my-project.my_dataset.raw_sales"
    
    # Load rådata direkt
    job = client.load_table_from_dataframe(df, raw_table)
    job.result()
    
    # Transform med SQL
    transform_query = """
    CREATE OR REPLACE TABLE `my-project.my_dataset.monthly_sales` AS
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        EXTRACT(MONTH FROM order_date) as month,
        product_category,
        SUM(amount) as total_sales,
        COUNT(*) as order_count
    FROM `my-project.my_dataset.raw_sales`
    WHERE amount > 0
    GROUP BY 1, 2, 3
    ORDER BY 1, 2, 3
    """
    
    client.query(transform_query).result()
```

---

## Performance-jämförelse

### ETL Performance-karakteristika
```
Datavolym: 1TB dagligen

ETL-flöde:
- Extract: 30 min
- Transform: 120 min (flaskhals)
- Load: 15 min
Total: 165 min

Resurser:
- Transform-server: 32 cores, 128GB RAM
- Network: 10Gbps
- Storage: SSD för temporära filer
```

### ELT Performance-karakteristika  
```
Datavolym: 1TB dagligen

ELT-flöde:
- Extract: 30 min  
- Load: 20 min (direkt till warehouse)
- Transform: 15 min (parallell SQL i warehouse)
Total: 65 min

Resurser:
- Warehouse: Auto-scaling (100-1000 nodes)
- Network: 100Gbps
- Storage: Distribuerad, kolumnbaserad
```

---

## Cost-jämförelse

### ETL-kostnader
```
Transform-server: $500/månad (alltid på)
Storage (temporära filer): $100/månad  
Development/maintenance: $2000/månad
Total: $2600/månad
```

### ELT-kostnader (Cloud)
```
BigQuery storage: $200/månad
BigQuery compute: $300/månad (pay-per-query)
dbt Cloud: $100/månad
Development/maintenance: $800/månad
Total: $1400/månad
```

**ELT är ofta mer kostnadseffektivt för cloud-baserade lösningar.**

---

## Beslutmatris

| Faktor | ETL | ELT | Kommentar |
|--------|-----|-----|-----------|
| **Datavolym** | < 1TB/dag | > 1TB/dag | ELT skalar bättre |
| **Transformation komplexitet** | Hög | Medium | ETL för komplexa algoritmer |
| **Säkerhetskrav** | Hög | Medium | ETL kan rensa känslig data |
| **Time-to-insight** | Långsam | Snabb | ELT ger snabbare tillgång |
| **Storage-kostnader** | Låg | Hög | ETL lagrar mindre data |
| **Utvecklingshastighet** | Långsam | Snabb | ELT enklare att iterera |
| **Historisk data** | Risk förlust | Bevaras | ELT behåller rådata |
| **Team-kunskap** | Python/Java | SQL | ELT mer SQL-fokuserat |

---

## Moderna Trends

### 1. ELT blir standard
```
2015: 80% ETL, 20% ELT
2024: 30% ETL, 70% ELT

Drivkrafter:
- Cloud data warehouses
- Billigare storage  
- Snabbare compute
- Self-service analytics
```

### 2. Real-time/Streaming
```
Traditionellt: Batch-processing (ETL)
Modernt: Stream-processing (ELT)

Verktyg:
- Apache Kafka + Apache Flink
- Google Pub/Sub + Dataflow
- AWS Kinesis + Lambda
```

### 3. DataOps och CI/CD
```
ETL: Svårt att versionshantera transformationer
ELT: dbt med Git-integration

Fördelar ELT för DataOps:
- Transformationer som kod
- Testning av data-transformationer
- Code reviews för SQL
- Automatiska deployments
```

---

## Sammanfattning

### Vad är ETL vs ELT?
- **ETL**: Transform data BEFORE loading (traditionellt)
- **ELT**: Transform data AFTER loading (modernt)

### Huvudskillnader:
- **Tid**: ETL långsammare, ELT snabbare initial load
- **Flexibilitet**: ELT mer flexibel för förändringar
- **Resurser**: ETL kräver transform-server, ELT använder warehouse
- **Data**: ELT behåller rådata, ETL kan förlora original

### När använda vad:
- **ETL**: Äldre system, säkerhetskritiskt, begränsad storage
- **ELT**: Moderna cloud-lösningar, stora volymer, flexibla behov

### Framtiden:
- ELT blir mer dominant tack vare cloud computing
- Hybrid-lösningar för olika use cases
- Real-time streaming blir vanligare
- DataOps kräver kodbaserade transformationer (ELT-vänligt)

**Bottom line:** Välj ETL för kontrolle och säkerhet, ELT för hastighet och flexibilitet. I moderna cloud-miljöer är ELT oftast det bättre valet!
