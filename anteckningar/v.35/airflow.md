# Apache Airflow - Grundläggande Koncept

## Vad är Apache Airflow?

Apache Airflow är en **workflow orchestration platform** - ett verktyg för att schemalägga, övervaka och hantera komplexa dataprocesser som består av flera steg.

### Enkelt förklarat:
Tänk dig att du har en kedja av uppgifter som måste köras i rätt ordning:
1. Ladda ner data från API
2. Rensa och validera datan
3. Ladda upp till databas
4. Skicka rapport via email

**Airflow** hjälper dig att:
- Definiera denna kedja som kod
- Schemalägga när den ska köras
- Hantera fel och omstart
- Övervaka framsteg visuellt

---

## Grundläggande Koncept

### 1. DAG (Directed Acyclic Graph)
**Vad det är:** En samling uppgifter med definierade beroenden mellan dem.

**Enkelt exempel:**
```
Hämta data → Rensa data → Spara data → Skicka rapport
     ↓           ↓           ↓           ↓
   Task A     Task B     Task C     Task D
```

**Kod-exempel:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Definiera DAG
dag = DAG(
    'enkel_data_pipeline',
    description='En enkel data pipeline',
    schedule_interval='@daily',  # Kör en gång per dag
    start_date=datetime(2024, 1, 1),
    catchup=False
)

def hamta_data():
    """Hämta data från API"""
    print("Hämtar data från API...")
    # Här skulle du ha din API-kod
    return "Data hämtad!"

def rensa_data():
    """Rensa och validera data"""
    print("Rensar data...")
    # Här skulle du ha din data-cleaning kod
    return "Data rensad!"

def spara_data():
    """Spara data till databas"""
    print("Sparar data...")
    # Här skulle du ha din databas-kod
    return "Data sparad!"

# Skapa tasks
hamta_task = PythonOperator(
    task_id='hamta_data',
    python_callable=hamta_data,
    dag=dag
)

rensa_task = PythonOperator(
    task_id='rensa_data', 
    python_callable=rensa_data,
    dag=dag
)

spara_task = PythonOperator(
    task_id='spara_data',
    python_callable=spara_data,
    dag=dag
)

# Definiera beroenden
hamta_task >> rensa_task >> spara_task
```

### 2. Tasks (Uppgifter)
**Vad det är:** Individuella steg i din pipeline.

**Olika typer av operators:**
```python
# Python-kod
PythonOperator(
    task_id='run_python_function',
    python_callable=min_funktion
)

# Bash-kommando
BashOperator(
    task_id='run_bash_command',
    bash_command='echo "Hello World"'
)

# SQL-query
SqlOperator(
    task_id='run_sql',
    sql='SELECT COUNT(*) FROM min_tabell'
)

# Email
EmailOperator(
    task_id='send_email',
    to=['team@company.com'],
    subject='Pipeline klar!',
    html_content='Data är processad.'
)
```

### 3. Schemaläggning
**Schedule Intervals:**
```python
# Varje dag kl 02:00
schedule_interval='0 2 * * *'

# Varje måndag
schedule_interval='0 0 * * 1'

# Varje timme
schedule_interval='@hourly'

# Fördefinierade alternativ
schedule_interval='@daily'
schedule_interval='@weekly'
schedule_interval='@monthly'

# Manuell trigger endast
schedule_interval=None
```

---

## Varför Airflow?

### Problem utan Airflow:
```bash
# Cron job - svårt att hantera beroenden och fel
0 2 * * * /path/to/script1.sh
5 2 * * * /path/to/script2.sh  # Hoppas script1 är klar...
10 2 * * * /path/to/script3.sh # Hoppas script2 är klar...
```

### Lösning med Airflow:
- **Visuell översikt** över hela processen
- **Automatisk felhantering** och retry-logik
- **Beroende-hantering** - script2 väntar på script1
- **Logging och monitoring** - se vad som gick fel
- **Skalbarhet** - kör på flera servrar

---

## Praktiskt Exempel: Data Pipeline

### Scenario: E-handelsdashboard
Varje natt ska vi:
1. Hämta försäljningsdata från API
2. Hämta kunddata från databas
3. Kombinera och analysera data
4. Generera rapport
5. Skicka till business team

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta
import pandas as pd
import requests

# DAG konfiguration
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ehandel_dashboard',
    default_args=default_args,
    description='Daglig e-handelsdashboard',
    schedule_interval='0 3 * * *',  # Kl 03:00 varje dag
    catchup=False
)

def hamta_forsaljningsdata():
    """Hämta försäljningsdata från API"""
    # Simulerad API-call
    data = {
        'datum': ['2024-01-01', '2024-01-02'],
        'forsaljning': [1000, 1200],
        'antal_ordrar': [50, 60]
    }
    df = pd.DataFrame(data)
    df.to_csv('/tmp/forsaljning.csv', index=False)
    return f"Hämtade {len(df)} försäljningsrader"

def hamta_kunddata():
    """Hämta kunddata från intern databas"""
    # Simulerad databas-query
    data = {
        'kund_id': [1, 2, 3],
        'namn': ['Anna', 'Bert', 'Cora'],
        'registrerad': ['2023-01-01', '2023-02-01', '2023-03-01']
    }
    df = pd.DataFrame(data)
    df.to_csv('/tmp/kunder.csv', index=False)
    return f"Hämtade {len(df)} kunder"

def analysera_data():
    """Kombinera och analysera data"""
    # Läs in data
    forsaljning = pd.read_csv('/tmp/forsaljning.csv')
    kunder = pd.read_csv('/tmp/kunder.csv')
    
    # Enkel analys
    total_forsaljning = forsaljning['forsaljning'].sum()
    total_ordrar = forsaljning['antal_ordrar'].sum()
    
    # Skapa rapport
    rapport = f"""
    Daglig E-handelsrapport
    ======================
    Total försäljning: {total_forsaljning} kr
    Antal ordrar: {total_ordrar}
    Genomsnitt per order: {total_forsaljning/total_ordrar:.2f} kr
    Antal aktiva kunder: {len(kunder)}
    """
    
    with open('/tmp/rapport.txt', 'w') as f:
        f.write(rapport)
    
    return "Analys klar!"

# Skapa tasks
hamta_forsaljning = PythonOperator(
    task_id='hamta_forsaljningsdata',
    python_callable=hamta_forsaljningsdata,
    dag=dag
)

hamta_kunder = PythonOperator(
    task_id='hamta_kunddata',
    python_callable=hamta_kunddata,
    dag=dag
)

analysera = PythonOperator(
    task_id='analysera_data',
    python_callable=analysera_data,
    dag=dag
)

skicka_rapport = EmailOperator(
    task_id='skicka_rapport',
    to=['business@company.com'],
    subject='Daglig E-handelsrapport',
    html_content='<p>Se bifogad rapport.</p>',
    files=['/tmp/rapport.txt'],
    dag=dag
)

# Definiera beroenden - parallell hämtning, sedan analys, sedan email
[hamta_forsaljning, hamta_kunder] >> analysera >> skicka_rapport
```

### Visuell representation:
```
hamta_forsaljningsdata ↘
                        ↘
                         analysera_data → skicka_rapport
                        ↗
hamta_kunddata        ↗
```

---

## Airflow UI och Monitoring

### Graph View
Airflow ger dig en visuell representation av din DAG:
- **Gröna boxar** = Framgångsrika tasks
- **Röda boxar** = Misslyckade tasks  
- **Gula boxar** = Pågående tasks
- **Grå boxar** = Väntande tasks

### Logs
Varje task har detaljerade loggar:
```
[2024-01-15 03:00:01] INFO - Hämtar data från API...
[2024-01-15 03:00:05] INFO - Data hämtad: 1000 rader
[2024-01-15 03:00:06] INFO - Task completed successfully
```

### Retry och Error Handling
```python
default_args = {
    'retries': 3,                    # Försök 3 gånger
    'retry_delay': timedelta(minutes=5),  # Vänta 5 min mellan försök
    'email_on_failure': True,       # Skicka email vid fel
    'sla': timedelta(hours=2)        # Service Level Agreement
}
```

---

## Jämförelse med Andra Verktyg

### Cron (traditionellt)
```bash
# Cron - enkelt men begränsat
0 3 * * * /path/to/daily_script.sh
```
**Begränsningar:**
- Ingen visuell överblick
- Svår felhantering
- Ingen beroende-hantering
- Begränsad logging

### Airflow
```python
# Airflow - kraftfullt och flexibelt
schedule_interval='0 3 * * *'
```
**Fördelar:**
- Visuell DAG-editor
- Avancerad felhantering
- Komplex beroende-hantering
- Rik logging och monitoring
- Skalbart över flera servrar

### Kubernetes CronJobs
```yaml
# Kubernetes - bra för containeriserade miljöer
apiVersion: batch/v1
kind: CronJob
spec:
  schedule: "0 3 * * *"
```
**Skillnader:**
- Kubernetes fokuserar på container-orchestration
- Airflow fokuserar på workflow-orchestration
- Kan användas tillsammans!

---

## När ska man använda Airflow?

### ✅ Bra användningsfall:
- **Komplexa data pipelines** med många steg
- **Beroenden mellan tasks** - A måste köras före B
- **Schemalagda jobb** som behöver övervakning
- **ETL-processer** (Extract, Transform, Load)
- **ML-pipelines** - träna modeller, evaluera, deploy
- **Datavalidering** och kvalitetskontroller

### ❌ Overkill för:
- **Enkla scripts** utan beroenden
- **Realtidsprocesser** (Airflow är batch-orienterat)
- **Mycket höga prestanda-krav** (streaming)
- **Enkla cron-jobb** som redan fungerar bra

### Exempel på perfekta Airflow-användningar:
```
1. Nattlig datasynkronisering:
   API → Validering → Transformering → Databas → Rapport

2. ML-pipeline:
   Data → Feature Engineering → Träning → Evaluering → Deploy

3. Rapportgenerering:
   Flera datakällor → Sammanslagning → Analys → PDF → Email
```

---

## Installation och Setup (Snabb översikt)

### Docker (Enklaste för test)
```bash
# Ladda ner Airflow Docker Compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'

# Starta Airflow
docker-compose up -d

# Öppna browser: http://localhost:8080
# Användarnamn: airflow
# Lösenord: airflow
```

### Pip installation
```bash
# Installera Airflow
pip install apache-airflow

# Initiera databas
airflow db init

# Skapa användare
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Starta web server
airflow webserver --port 8080

# Starta scheduler (i annat terminal)
airflow scheduler
```

---

## Sammanfattning

### Vad är Airflow?
- **Workflow orchestration** - kör komplexa dataprocesser
- **Kod-baserad** - definiera pipelines som Python-kod
- **Visuell** - se dina processer grafiskt
- **Robust** - felhantering, retry, monitoring

### Huvudkoncept:
- **DAG** = Hela processen (Directed Acyclic Graph)
- **Task** = Individuella steg
- **Operator** = Typ av steg (Python, Bash, SQL, etc.)
- **Schedule** = När processen ska köras

### Varför använda det?
- Ersätter komplexa cron-jobb
- Bättre överblick och kontroll
- Professionell felhantering
- Skalbart för stora organisationer

### Alternativ:
- **Cron** - för enkla schemalagda jobb
- **Kubernetes CronJobs** - för containeriserade miljöer  
- **Cloud-lösningar** - AWS Step Functions, GCP Cloud Workflows
- **Andra verktyg** - Prefect, Dagster, Luigi

**Bottom line:** Airflow är ett kraftfullt verktyg för komplexa dataprocesser, men använd det bara när du verkligen behöver dess funktioner. För enkla saker räcker cron gott och väl!
