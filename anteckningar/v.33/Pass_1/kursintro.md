# Kursintroduktion: Data Engineering & Agil Metodik

## 🎯 Välkommen till kursen!

Denna kurs kombinerar praktisk **Data Engineering** med **Agil Metodik** för att ge dig verktyg och arbetsmetoder som används i moderna tech-företag.

---

## 📊 Vad är Data Engineering?

Data Engineering är konsten att **samla in**, **bearbeta** och **tillgängliggöra** data för analys och beslutsfattande.

### Vad gör en Data Engineer?
- **Bygger datapipelines** som automatiskt hämtar data från olika källor
- **Transformerar rådata** till struktur som är användbar för analytiker
- **Säkerställer datakvalitet** och övervakar system för fel
- **Designar databaser** och datalagringslösningar
- **Automatiserar processer** så data flödar smidigt utan manuell inblandning

### Exempel på vardagliga uppgifter:
```
🏪 E-handel → Samla försäljningsdata från webshop + CRM + lager
🏥 Sjukvård → Integrera patientdata från olika system säkert
📱 Sociala medier → Bearbeta miljontals posts för sentiment-analys
🚗 Transport → Analysera GPS-data för optimering av rutter
```

**Enkelt uttryckt:** Data Engineers bygger "vattenkranen" som levererar ren, användbar data till analytiker och beslutsfattare.

---

## 🗓️ Kursupplägg

### **Format:**
- **9 veckor** total kurstid (12 aug – 12 okt)
- **2 pass per vecka** (09:00-15:00)
- **Praktisk hands-on approach** - vi bygger riktiga system
- **Agila arbetsmetoder** genomsyrar hela kursen
- **Grupprojekt** som röd tråd genom kursen

### **Lärandemiljö:**
- **Blandad undervisning:** Teori + praktik i samma session
- **Code-alongs:** Vi kodar tillsammans steg för steg
- **Labbmiljöer:** Hands-on workshops varje pass
- **Grupparbete:** Simulerar riktiga utvecklingsteam
- **Projektworkshops:** Dedicated tid för projektarbete

---

## 📚 Kursinnehåll: Vad kommer vi lära oss?

### **🔧 Tekniska Verktyg & Plattformar:**
- **WSL & Ubuntu** → Linux-miljö på Windows
- **Bash/Linux** → Kommandorad och serverhantering
- **Git/GitHub** → Versionshantering och samarbete
- **Docker** → Containerisering och deployment
- **GitHub Actions** → CI/CD och automatisering
- **Google Cloud Platform (GCP)** → Molnplattform (Compute, Storage, IAM)
- **BigQuery** → Data warehouse och SQL-transformationer
- **Cloud Dataflow/dbt** → Batch-processing av data
- **Apache Airflow** → Orkestreringsverktyg för datapipelines
- **Apache Spark** → Distribuerad databehandling (möjligen)
- **Python** → Automatisering och databehandling
- **API:er** → Datakällor och integrationer

### **⚡ Agila Metoder:**
- **Agila värden & principer** → Grunden för agilt arbetssätt
- **Scrum** → Roller, ceremonier och artefakter
- **Kanban** → Visuell processhantering och jämförelse med Scrum
- **Backlog & Sprint Planning** → Prioritering och planering
- **Retrospektiv** → Kontinuerlig förbättring av teamprocesser

### **🏗️ Grupprojekt (Röd Tråd):**
- **End-to-end datapipeline** som grupparbete
- **Agil projektmetodik** med riktiga sprints
- **CI/CD implementation** med GitHub Actions
- **Molndeploy** på Google Cloud Platform
- **Teamsamarbete** via Git workflows och PR-processer
- **Presentations** och teknisk reflektion

---

## 📖 Undervisningsformat

### **🎤 Presentationer**
- **Konceptuell fördjupning** av teorier och best practices
- **Live demos** av verktyg och plattformar
- **Interaktiva Q&A** sessioner

### **📝 Anteckningar på GitHub**
Alla kursmaterial finns på GitHub för enkel åtkomst:
```
📁 anteckningar/
  ├── v.33/ (Vecka 33)
  │   ├── Pass_1/
  │   │   ├── kursintro.md
  │   │   ├── bash-grundkurs.md
  │   │   └── wsl-installationsguide.md
  │   └── Pass_2/
  │       ├── git-github-ssh.md
  │       └── docker-anteckningar.md
  ├── v.34/ (Vecka 34)
  └── v.35/ (Vecka 35)
```

**Fördelar:**
- ✅ **Alltid uppdaterat** material
- ✅ **Sökbar** innehåll
- ✅ **Historik** av ändringar
- ✅ **Mobilvänligt** - läs var som helst

### **💻 Kod & Exempel på GitHub**
```
📁 kod/
  ├── bq/ (BigQuery pipelines)
  │   ├── main.py
  │   ├── dockerfile
  │   └── dbt_project.yml
  ├── docker/ (Container demos)
  └── exercises/ (Övningsuppgifter)
```

**Exempel på vad du kommer bygga:**
- **API data extraction** → Hämta data från externa tjänster
- **ETL pipelines** → Extract, Transform, Load processer
- **Dockerized applications** → Containers för portabilitet
- **Cloud deployment** → Publika tjänster på GCP

### **👥 Code-Alongs**
- **Live kodning** där vi bygger tillsammans
- **Steg-för-steg genomgångar** av komplexa koncept
- **Felsökning i realtid** - lär dig av misstag
- **Individuell assistans** under sessions

**Format:**
1. **Demo** → Jag visar tekniken
2. **Code-Along** → Vi kodar tillsammans
3. **Egen tid** → Du experimenterar själv
4. **Q&A** → Vi löser problem tillsammans

---

## 🎓 Examination & Bedömning

### **Examinationsmoment:**

**[Detaljer fylls i här med specifika krav, deadlines och bedömningskriterier]**

- **Grupprojekt** med agil metodik (huvud-examination)
- **Gruppresentationer** (vecka 9)
- **Individuell teknisk reflektion/analys** 
- **Löpande deltagande** i workshops och labs
- **Code review** och peer assessment under projektarbete

---

## 🚀 Detaljerad Kursplan

| **Vecka** | **Datum** | **Pass 1 (09-15)** | **Pass 2 (09-15)** | **Övrigt** |
|-----------|-----------|---------------------|---------------------|-------------|
| **1** | 12 & 14 aug | **Kursintro**<br/>WSL & Ubuntu + Bash-övningar | **Verktyg & SSH-setup**<br/>Python/venv, Git/GitHub-CLI<br/>SSH-nycklar mot GitHub | |
| **2** | 18 & 21 aug | **Git & GitHub**<br/>Init, branching, PR-workflow<br/>Lab: team-övning med repo | **Docker-intro + CI/CD**<br/>Images, containers, Dockerfile<br/>GitHub Actions pipeline<br/>Introduktion data engineering & API:er | Projektintroduktion |
| **3** | 26 & 28 aug | **Molnöversikt & IAM**<br/>GCP-arkitektur, service accounts<br/>BigQuery intro | **Agila metoder (teori)**<br/>Agila värden, Scrum, Kanban<br/>Backlog & sprintplanering | **Distans** |
| **4** | 2 & 4 sept | **Compute & Storage**<br/>Compute Engine, Cloud Storage<br/>Lab: instans & data | **BigQuery (batch)**<br/>SQL-transforms "silver→gold"<br/>Lab: frågor & datahantering | |
| **5** | 9 & 11 sept | **Dataflow/dbt (batch)**<br/>Lab: GCS→BigQuery | **Airflow (lokalt)**<br/>Docker-Compose, DAG-syntax<br/>Lab: orkestrera jobb | |
| **6** | 16 & 18 sept | **Recap** | **Projektworkshop**<br/>Hands-on support, Q&A<br/>Spark? | |
| **7** | 23 & 25 sept | **Avancerad orkestrering**<br/>Schemaläggning med cron/Actions | **Kubernetes?**<br/>Feedback på förslag | |
| **8** | 30 sept & 2 okt | **Övervakning & felsökning**<br/>Monitorera Airflow, alerting | **Security och GDPR** | **Distans** |
| **9** | 7 & 9 okt | **Projektworkshop** | **Presentationer del 1**<br/>Gruppredovisningar + Q&A | **Presentationer del 2**<br/>Individuell teknikanalys |

---

## 💡 Tips för Framgång

### **🎯 Aktivt Deltagande:**
- **Ställ frågor** direkt när något är oklart
- **Experimentera** utanför lektionerna
- **Samarbeta** med kurskamrater
- **Dokumentera** din inlärningsresa

### **🔧 Teknisk Förberedelse:**
- Ha **WSL** installerat och fungerande
- **GitHub-konto** för versionshantering  
- **Google Cloud** konto (vi sätter upp tillsammans)
- **Nyfiken inställning** till nya verktyg

### **🤝 Agil Mindset:**
- **Iterativ förbättring** framför perfektion
- **Transparens** och öppen kommunikation
- **Anpassningsförmåga** när krav ändras
- **Teamwork** över individuella prestationer

---

## 🎉 Låt oss börja!

Välkommen till en spännande resa in i Data Engineering och Agil Metodik! 

**Nästa steg:** [WSL Installation Guide](./wsl-installationsguide.md) för att sätta upp din utvecklingsmiljö.

---

*"Data is the new oil, but like oil, it's not useful until it's refined."* - En Data Engineer någonstans 🛢️→💎