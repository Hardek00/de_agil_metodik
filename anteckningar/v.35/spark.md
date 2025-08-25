# Apache Spark - Praktisk Introduktion

## Vad är Apache Spark?

Apache Spark är ett **distribuerat beräkningsramverk** som låter dig bearbeta stora datamängder snabbt genom att sprida arbetet över flera CPU-kärnor eller maskiner.

### Enkelt förklarat:
```
Pandas: 1 CPU-kärna bearbetar data sekventiellt
Spark: Alla CPU-kärnor bearbetar data parallellt

Din laptop: 8 CPU-kärnor
Pandas: Använder 1 kärna → 100% av 1 kärna = 12.5% total användning
Spark: Använder 8 kärnor → 100% av 8 kärnor = 100% total användning
```

**Resultat**: 5-10x snabbare bearbetning på samma maskin!

---

## Varför Spark vs Era Befintliga Verktyg?

### Pandas vs Spark - Praktisk Jämförelse

```python
# Pandas (sekventiell)
import pandas as pd
df = pd.read_csv('large_file.csv')  # 2GB → 5 minuter, använder 1 CPU
result = df.groupby('category').sum()  # Långsamt

# PySpark (parallell)
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("MyApp").getOrCreate()
df = spark.read.csv('large_file.csv')  # 2GB → 1 minut, använder alla CPUs
result = df.groupBy('category').sum()  # Mycket snabbare
```

### Prestandajämförelse (typiska siffror):
```
Datafil: 5GB CSV

Pandas:
- Laddning: 15 minuter
- Bearbetning: 25 minuter  
- Total: 40 minuter
- Minne: Kraschar ofta (behöver >8GB RAM)

PySpark:
- Laddning: 3 minuter
- Bearbetning: 5 minuter
- Total: 8 minuter  
- Minne: Fungerar med 4GB RAM (strömmande processing)
```

---

## Spark i Era Projekt - Konkreta Användningsfall

### 1. E-handelsanalys (stora dataset)
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Starta Spark
spark = SparkSession.builder \
    .appName("ECommerceAnalysis") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# Läs stora e-handelsfiler
orders = spark.read.csv('orders_2023.csv', header=True, inferSchema=True)
customers = spark.read.csv('customers.csv', header=True, inferSchema=True)

# Snabb analys på stora data
customer_metrics = orders.join(customers, 'customer_id') \
    .groupBy('customer_id', 'customer_name') \
    .agg(
        sum('total_amount').alias('lifetime_value'),
        count('order_id').alias('total_orders'),
        avg('total_amount').alias('avg_order_value')
    )

# Skriv resultat till BigQuery
customer_metrics.write \
    .format("bigquery") \
    .option("table", "myproject.mydataset.customer_analysis") \
    .mode("overwrite") \
    .save()
```

### 2. Log-analys (många filer)
```python
# Läs alla log-filer på en gång (tusentals filer)
logs = spark.read.text('logs/2023/*/access.log')

# Parsa och analysera
parsed_logs = logs.select(
    regexp_extract('value', r'^(\S+)', 1).alias('ip'),
    regexp_extract('value', r'"\w+ (\S+)', 1).alias('url'),
    regexp_extract('value', r'" (\d{3})', 1).cast('int').alias('status')
)

# Hitta populäraste sidor
popular_pages = parsed_logs \
    .filter(col('status') == 200) \
    .groupBy('url') \
    .count() \
    .orderBy(desc('count')) \
    .limit(10)

popular_pages.show()
```

### 3. Sensor-data aggregering
```python
# IoT sensor data - miljontals readings
sensor_data = spark.read.json('sensor_readings/*.json')

# Aggregera per timme och sensor
hourly_stats = sensor_data \
    .withColumn('hour', date_trunc('hour', 'timestamp')) \
    .groupBy('sensor_id', 'hour') \
    .agg(
        avg('temperature').alias('avg_temp'),
        max('temperature').alias('max_temp'),
        min('temperature').alias('min_temp'),
        count('*').alias('reading_count')
    )

# Filtrera anomalier
anomalies = hourly_stats.filter(
    (col('max_temp') > 50) | (col('min_temp') < -10)
)

anomalies.show()
```

---

## Installation och Setup

### Lokalt på Era Maskiner

#### Via pip (enklaste):
```bash
pip install pyspark

# Med BigQuery-support
pip install pyspark[sql]
pip install google-cloud-bigquery-storage
```

#### Test-installation:
```python
from pyspark.sql import SparkSession

# Skapa Spark session
spark = SparkSession.builder \
    .appName("TestApp") \
    .master("local[*]") \
    .getOrCreate()

# Test med enkel data
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
columns = ["name", "age"]

df = spark.createDataFrame(data, columns)
df.show()

# Stäng Spark
spark.stop()
```

### Docker Setup för Era Projekt

#### Dockerfile:
```dockerfile
FROM python:3.9-slim

# Installera Java (krävs för Spark)
RUN apt-get update && apt-get install -y openjdk-11-jre-headless

# Installera Python-paket
COPY requirements.txt .
RUN pip install -r requirements.txt

# Kopiera kod
COPY . /app
WORKDIR /app

# Sätt miljövariabler
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV SPARK_HOME=/usr/local/lib/python3.9/site-packages/pyspark

CMD ["python", "spark_pipeline.py"]
```

#### docker-compose.yml:
```yaml
version: '3.8'

services:
  spark-app:
    build: .
    environment:
      - SPARK_MASTER=local[*]
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
    volumes:
      - ./data:/app/data
      - ./service-account.json:/app/service-account.json:ro
    ports:
      - "4040:4040"  # Spark Web UI
```

---

## PySpark API - Grunderna

### DataFrames (som pandas, men distribuerat)

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

spark = SparkSession.builder.appName("Learning").getOrCreate()

# Skapa DataFrame från data
data = [
    ("Alice", 25, "Engineer", 75000),
    ("Bob", 30, "Manager", 85000),
    ("Charlie", 35, "Engineer", 70000),
    ("Diana", 28, "Analyst", 65000)
]
columns = ["name", "age", "job", "salary"]
df = spark.createDataFrame(data, columns)

# Basic operations (som pandas)
df.show()                           # Visa data
df.printSchema()                    # Schema info
df.describe().show()                # Statistik

# Filtering (som pandas)
engineers = df.filter(col("job") == "Engineer")
high_earners = df.filter(col("salary") > 70000)

# Grouping (som pandas)
avg_salary_by_job = df.groupBy("job").avg("salary")
avg_salary_by_job.show()

# Sorting
df.orderBy(desc("salary")).show()

# Ny kolumn
df_with_bonus = df.withColumn("bonus", col("salary") * 0.1)
df_with_bonus.show()
```

### Läsa Olika Filformat

```python
# CSV
df_csv = spark.read.csv('data.csv', header=True, inferSchema=True)

# JSON
df_json = spark.read.json('data.json')

# Parquet (mest effektiv)
df_parquet = spark.read.parquet('data.parquet')

# Flera filer samtidigt
df_multiple = spark.read.csv('data/2023/*/sales.csv', header=True)

# Med schema (snabbare än inferSchema)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True)
])

df_with_schema = spark.read.csv('data.csv', header=True, schema=schema)
```

---

## Integration med BigQuery

### Läsa från BigQuery
```python
# Konfigurera BigQuery
spark.conf.set("viewsEnabled", "true")
spark.conf.set("materializationDataset", "temp_dataset")

# Läs direkt från BigQuery
df = spark.read \
    .format("bigquery") \
    .option("table", "myproject.mydataset.mytable") \
    .load()

# Eller med SQL
df = spark.read \
    .format("bigquery") \
    .option("query", """
        SELECT customer_id, SUM(amount) as total
        FROM `myproject.mydataset.orders` 
        WHERE order_date >= '2023-01-01'
        GROUP BY customer_id
    """) \
    .load()
```

### Skriva till BigQuery
```python
# Skriv resultat tillbaka
result_df.write \
    .format("bigquery") \
    .option("table", "myproject.mydataset.results") \
    .option("writeMethod", "direct") \
    .mode("overwrite") \
    .save()

# Append mode för att lägga till data
daily_summary.write \
    .format("bigquery") \
    .option("table", "myproject.mydataset.daily_stats") \
    .mode("append") \
    .save()
```

---

## Spark Web UI - Monitoring

När ni kör Spark lokalt kan ni övervaka prestanda:

```
Öppna browser: http://localhost:4040

Flikar att kolla:
- Jobs: Se vilka operationer som körs
- Stages: Detaljerat för varje bearbetningssteg  
- Storage: Cachade DataFrames
- Executors: CPU och minne-användning
```

### Exempel på vad ni ser:
```
Jobs Tab:
┌────────┬─────────────────┬──────────┬──────────┐
│ Job ID │ Description     │ Duration │ Status   │
├────────┼─────────────────┼──────────┼──────────┤
│ 0      │ csv read        │ 2.3s     │ Success  │
│ 1      │ groupBy         │ 1.8s     │ Running  │
│ 2      │ write to BQ     │ -        │ Pending  │
└────────┴─────────────────┴──────────┴──────────┘
```

---

## Optimering och Best Practices

### 1. Caching för Återanvändning
```python
# Om ni använder samma DataFrame flera gånger
large_df = spark.read.csv('huge_file.csv')

# Cache i minnet för snabbare access
large_df.cache()

# Nu är alla operationer snabbare
result1 = large_df.filter(col('amount') > 1000).count()
result2 = large_df.groupBy('category').sum('amount')  # Använder cachad data
result3 = large_df.select('customer_id').distinct()   # Också snabbare
```

### 2. Partitionering för Prestanda
```python
# Partitionera data för parallell processing
df.write \
    .partitionBy('year', 'month') \
    .parquet('output/partitioned_data')

# När ni läser tillbaka - mycket snabbare för datum-queries
df = spark.read.parquet('output/partitioned_data')
jan_data = df.filter((col('year') == 2023) & (col('month') == 1))
```

### 3. Rätt Antal Partitioner
```python
# Kolla nuvarande partitioner
print(f"Partitions: {df.rdd.getNumPartitions()}")

# Optimera för er maskin (vanligtvis 2-4 per CPU-kärna)
df_optimized = df.repartition(16)  # För 8-kärnig maskin

# Eller baserat på kolumn
df_by_category = df.repartition('category')
```

---

## Vanliga Fel och Lösningar

### 1. Minnes-problem
```python
# Problem: "Java heap space" error
# Lösning: Öka minne
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()
```

### 2. Långsamma Joins
```python
# Problem: Långsam join
large_df.join(small_df, 'key')  # Långsam

# Lösning: Broadcast join för små tables
from pyspark.sql.functions import broadcast
large_df.join(broadcast(small_df), 'key')  # Mycket snabbare
```

### 3. För många små filer
```python
# Problem: Tusentals små filer = långsam
df.write.csv('output/')  # Skapar många små filer

# Lösning: Coalesce före skrivning
df.coalesce(10).write.csv('output/')  # 10 filer istället
```

---

## Praktiska Projekt för Era Studenter

### Projekt 1: E-handelsanalys
```python
"""
Mål: Analysera försäljningsdata för att hitta trends

Data: orders.csv (1-5GB), customers.csv, products.csv
Uppgifter:
1. Läs in alla filer med Spark
2. Skapa customer lifetime value
3. Hitta populäraste produkter per månad
4. Identifiera säsongseffekter
5. Exportera resultat till BigQuery
"""

def ecommerce_analysis():
    # Era implementationer här
    orders = spark.read.csv('orders.csv', header=True, inferSchema=True)
    # ... fortsätt analysen
```

### Projekt 2: Log-analys
```python
"""
Mål: Analysera webbserver-loggar för att förstå användarbeteende

Data: access.log filer (många GB)
Uppgifter:
1. Parsa log-format med regex
2. Hitta populäraste sidor
3. Identifiera fel-mönster (404, 500)
4. Analysera trafik per timme
5. Skapa dashboard-data
"""

def log_analysis():
    logs = spark.read.text('logs/*.log')
    # Era parsing och analys här
```

### Projekt 3: IoT sensor-data
```python
"""
Mål: Bearbeta sensor-data för anomali-detektion

Data: JSON-filer från sensorer (många små filer)
Uppgifter:
1. Läs tusentals JSON-filer effektivt
2. Aggregera data per timme/dag
3. Hitta temperatur-anomalier
4. Beräkna rullande medelvärden
5. Spara aggregerad data för dashboard
"""

def sensor_analysis():
    sensor_data = spark.read.json('sensors/*/*.json')
    # Era analytics här
```

---

## Spark vs Andra Verktyg - När Använda Vad?

### Beslutsmatris:
```
Datasize < 1GB:
✅ Pandas: Snabbt, enkelt, lätt att debugga
❌ Spark: Overkill, overhead för setup

Datasize 1-10GB:
✅ Spark: Mycket snabbare än pandas
✅ BigQuery: Om data redan finns där
❌ Pandas: Risk för memory crash

Datasize > 10GB:
✅ Spark: Perfekt användningsområde
✅ Dataflow: För managed processing
❌ Pandas: Fungerar inte

Realtidsdata:
✅ Spark Streaming: Kontinuerlig processing
✅ Dataflow: Managed streaming
❌ Pandas: Inte designat för streaming

Team med SQL-fokus:
✅ BigQuery + dbt: SQL-baserat
✅ Spark SQL: SQL på stora data
❌ Pandas: Kräver Python-kunskap

Komplex ML:
✅ Spark MLlib: Distribuerad ML
✅ Vertex AI: Managed ML
❌ Pandas + scikit-learn: Begränsat av minne
```

---

## Installation Guide för Era Projekt

### Steg 1: Basic Setup
```bash
# Skapa projekt-miljö
python -m venv spark_env
source spark_env/bin/activate  # Linux/Mac
# eller
spark_env\Scripts\activate     # Windows

# Installera
pip install pyspark pandas google-cloud-bigquery-storage
```

### Steg 2: Test-körning
```python
# test_spark.py
from pyspark.sql import SparkSession
import time

start_time = time.time()

spark = SparkSession.builder \
    .appName("SparkTest") \
    .master("local[*]") \
    .getOrCreate()

# Skapa test-data
data = [(i, f"user_{i}", i * 10) for i in range(1000000)]
df = spark.createDataFrame(data, ["id", "name", "score"])

# Testoperationer
result = df.filter(df.score > 5000).groupBy("name").sum("score")
count = result.count()

print(f"Processed {count} records in {time.time() - start_time:.2f} seconds")
spark.stop()
```

### Steg 3: BigQuery Integration
```python
# bigquery_test.py
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BigQueryTest") \
    .config("spark.jars.packages", "com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.32.2") \
    .getOrCreate()

# Test läsning från BigQuery
df = spark.read \
    .format("bigquery") \
    .option("table", "bigquery-public-data.samples.shakespeare") \
    .load()

df.show(5)
spark.stop()
```

---

## Sammanfattning för Era 9 Veckor

### Vad är Spark?
- **Distribuerad beräkning** - använder alla CPU-kärnor parallellt
- **PySpark** - Python API som känns som pandas
- **Skalbar** - från lokal maskin till stora kluster
- **Snabb** - 5-10x snabbare än pandas för stora data

### Varför Relevant för Er?
- **Påtaglig förbättring** - ni ser direkt skillnad i prestanda
- **Praktiskt användbart** - kan faktiskt använda i era projekt
- **Industri-standard** - används överallt för big data
- **Bygger på Python** - använder befintlig kunskap

### Vad Ni Kan Göra:
1. **Installera och testa** - få det att fungera lokalt
2. **Konvertera pandas-kod** - samma logik, snabbare exekvering
3. **Integrera med BigQuery** - läsa/skriva stora dataset
4. **Använd i grupprojekt** - bearbeta större data tillsammans

### Realistic Timeline:
- **Vecka 1**: Installation och basic DataFrame-operationer
- **Vecka 2**: Läsa filer och enkla aggregeringar  
- **Vecka 3**: BigQuery-integration och första "riktiga" projekt
- **Resten**: Använda Spark för era data-pipelines

**Bottom line**: Spark är det verktyg som faktiskt kan förbättra era nuvarande projekt direkt. Det är som pandas fast snabbare - perfekt för att känna kraften i distribuerad beräkning utan att behöva lära sig helt nya koncept!

Nu kan ni faktiskt bearbeta de där 5GB CSV-filerna som pandas kraschar på! 🚀
