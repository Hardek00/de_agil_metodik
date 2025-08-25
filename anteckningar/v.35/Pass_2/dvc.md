# Data Version Control (DVC)

## Vad är Data Version Control?

Data Version Control är konceptet att **versionshantera data** på samma sätt som vi versionshantera kod med Git. DVC (Data Version Control) är ett verktyg som gör detta möjligt.

### Problemet
```bash
# Så här ser det ofta ut i projekt:
data/
├── dataset_v1.csv           # 2GB
├── dataset_v2.csv           # 2GB  
├── dataset_final.csv        # 2GB
├── dataset_final_final.csv  # 2GB
├── model_20240115.pkl       # 500MB
├── model_20240116.pkl       # 500MB
└── model_best.pkl           # 500MB
```

**Problem:**
- Stora filer som inte kan versionshanteras i Git
- Oklart vilken version som är aktuell
- Svårt att reproducera tidigare resultat
- Storage-problem - samma data sparas flera gånger

### Lösningen med DVC
```bash
# Med DVC ser det ut så här:
data/
├── dataset.csv.dvc     # 100 bytes - pekare till data
└── model.pkl.dvc       # 100 bytes - pekare till modell

# Faktisk data lagras i remote storage (S3, GCS, etc.)
```

---

## Varför behöver vi Data Version Control?

### 1. Stora Filer
Git är designat för kod (text), inte data:
- **Git problem**: Långsam med filer > 100MB
- **DVC lösning**: Lagrar bara "pekare" i Git, data i molnet

### 2. Reproducerbarhet
```python
# Utan DVC - oklart vilken data som användes
model = train_model('data/dataset_final_v3.csv')

# Med DVC - exakt version spåras
model = train_model('data/dataset.csv')  # DVC vet vilken version
```

### 3. Collaboration
- **Problem**: Skicka stora datafiler via email/Slack
- **Lösning**: Alla hämtar samma data-version automatiskt

### 4. Experimenthantering
- Spåra vilken data som gav bäst resultat
- Jämföra modeller tränade på olika dataset
- Rollback till tidigare versioner

---

## Grundläggande DVC-koncept

### 1. DVC Files (.dvc)
**Vad det är:** Små textfiler som pekar på stora datafiler

**Exempel `dataset.csv.dvc`:**
```yaml
outs:
- md5: a1b2c3d4e5f6...
  size: 2147483648
  path: dataset.csv
```

**I Git sparas:** `dataset.csv.dvc` (100 bytes)  
**I remote storage:** `dataset.csv` (2GB)

### 2. Remote Storage
DVC kan använda många storage-lösningar:
- **Cloud**: AWS S3, Google Cloud Storage, Azure Blob
- **Lokal**: Annan disk/server
- **SSH**: Remote server via SSH

### 3. Pipelines
DVC kan också hantera hela ML-pipelines:
```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python prepare_data.py
    deps: [raw_data.csv]
    outs: [clean_data.csv]
  
  train:
    cmd: python train.py
    deps: [clean_data.csv]
    outs: [model.pkl]
```

---

## Praktiskt Exempel: ML-projekt

### Setup
```bash
# Initiera DVC i ditt Git-repo
git init
dvc init

# Lägg till remote storage (Google Cloud Storage)
dvc remote add -d myremote gs://my-bucket/dvc-storage

# Eller lokal storage för test
dvc remote add -d myremote /tmp/dvc-storage
```

### Scenario: Bildklassificering
Du bygger en modell för att klassificera hundraser med en dataset på 5GB.

#### Steg 1: Lägg till data
```bash
# Ladda ner stora bilddataset
wget https://example.com/dog-dataset.zip
unzip dog-dataset.zip  # 5GB bilder

# Lägg till i DVC (inte Git!)
dvc add images/
git add images.dvc .gitignore
git commit -m "Add dog images dataset v1"

# Pusha data till remote storage
dvc push
```

**Vad händer:**
- `images.dvc` skapas (småfil som pekar på data)
- `images/` läggs till i `.gitignore`
- Faktiska bilder laddas upp till molnet
- Git trackar bara pekaren

#### Steg 2: Teamwork
Kollega klona ditt repo:
```bash
git clone https://github.com/yourrepo/dog-classifier
cd dog-classifier

# Hämta data automatiskt
dvc pull
```

Nu har kollegan exakt samma data som du hade!

#### Steg 3: Datauppdatering
Du får fler bilder och vill uppdatera dataset:
```bash
# Lägg till nya bilder
cp new_images/* images/

# Uppdatera DVC
dvc add images/
git add images.dvc
git commit -m "Add 500 new dog images - dataset v2"
dvc push
```

#### Steg 4: Experimentering
```bash
# Träna modell med v1 av data
git checkout HEAD~1  # Gå tillbaka till v1
dvc checkout         # Hämta v1-data
python train.py      # Träna modell

# Jämför med v2
git checkout main    # Tillbaka till v2
dvc checkout         # Hämta v2-data  
python train.py      # Träna på nya data
```

---

## DVC Pipelines - Automatisera ML-flödet

### Pipeline Definition (dvc.yaml)
```yaml
stages:
  # Steg 1: Datapreparering
  prepare:
    cmd: python scripts/prepare_data.py
    deps:
      - scripts/prepare_data.py
      - data/raw_images/
    outs:
      - data/processed_images/
    params:
      - prepare.image_size
      - prepare.augmentation

  # Steg 2: Feature extraction
  features:
    cmd: python scripts/extract_features.py
    deps:
      - scripts/extract_features.py
      - data/processed_images/
    outs:
      - data/features.npy
    params:
      - features.model_name

  # Steg 3: Träning
  train:
    cmd: python scripts/train.py
    deps:
      - scripts/train.py
      - data/features.npy
    outs:
      - models/classifier.pkl
    metrics:
      - metrics.json
    params:
      - train.learning_rate
      - train.epochs

  # Steg 4: Evaluering
  evaluate:
    cmd: python scripts/evaluate.py
    deps:
      - scripts/evaluate.py
      - models/classifier.pkl
      - data/test_features.npy
    metrics:
      - evaluation.json
```

### Parameter-fil (params.yaml)
```yaml
prepare:
  image_size: 224
  augmentation: true

features:
  model_name: "resnet50"

train:
  learning_rate: 0.001
  epochs: 50
  batch_size: 32
```

### Köra Pipeline
```bash
# Kör hela pipelinen
dvc repro

# Kör bara vissa steg
dvc repro train

# Kör om parameterändring upptäcks
# (DVC upptäcker automatiskt beroenden)
```

### Experimentjämförelse
```bash
# Ändra parametrar
# params.yaml: learning_rate: 0.01

# Kör experiment
dvc repro

# Jämför resultat
dvc metrics diff

# Visa alla experiment
dvc exp show
```

---

## Praktiska Kommandon

### Grundläggande Workflow
```bash
# Initiera DVC
dvc init

# Lägg till remote storage
dvc remote add -d storage s3://my-bucket/dvc

# Lägg till data
dvc add large_dataset.csv
git add large_dataset.csv.dvc .gitignore
git commit -m "Add dataset"

# Pusha data
dvc push

# Andra utvecklare: hämta data
dvc pull

# Uppdatera data
# (ändra filen)
dvc add large_dataset.csv
git add large_dataset.csv.dvc
git commit -m "Update dataset"
dvc push
```

### Branches och Experiment
```bash
# Skapa experiment-branch
git checkout -b experiment-new-features
dvc checkout

# Ändra data för experiment
cp experimental_data.csv dataset.csv
dvc add dataset.csv
git add dataset.csv.dvc
git commit -m "Experiment with new features"

# Tillbaka till main
git checkout main
dvc checkout  # Hämtar original-data automatiskt
```

### Status och Info
```bash
# Se DVC-status
dvc status

# Se info om fil
dvc list storage://remote/path

# Se pipeline-status
dvc dag  # Visa dependency graph

# Se metrics från experiment
dvc metrics show
dvc plots show
```

---

## Integration med Git och Remote Storage

### Git + DVC Workflow
```bash
# Normal Git workflow
git add script.py
git commit -m "Update training script"

# DVC workflow för data
dvc add new_data.csv
git add new_data.csv.dvc
git commit -m "Add new training data"

# Pusha både kod och data
git push       # Kod till GitHub
dvc push       # Data till cloud storage
```

### Team Workflow
```bash
# Developer A: Lägg till ny data
dvc add dataset.csv
git add dataset.csv.dvc
git commit -m "Add Q4 data"
git push
dvc push

# Developer B: Hämta uppdateringar
git pull
dvc pull  # Hämtar automatiskt ny data
```

---

## Storage-alternativ

### 1. Google Cloud Storage
```bash
# Setup
dvc remote add -d storage gs://my-bucket/data
dvc remote modify storage credentialpath /path/to/credentials.json

# Eller använd gcloud auth
gcloud auth application-default login
```

### 2. AWS S3
```bash
# Setup
dvc remote add -d storage s3://my-bucket/data
dvc remote modify storage profile my-aws-profile

# Eller environment variables
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

### 3. Lokal/SSH Storage
```bash
# Lokal disk
dvc remote add -d storage /mnt/shared/dvc-data

# SSH server
dvc remote add -d storage ssh://user@server/path/to/data
dvc remote modify storage password mypassword
```

---

## Jämförelse med Andra Verktyg

### Git LFS vs DVC
**Git LFS:**
- Inbyggt i Git
- Enkelt för enstaka stora filer
- Begränsat för ML-pipelines

**DVC:**
- Mer flexibelt för ML-projekt
- Pipeline-hantering
- Experiment-tracking
- Fungerar med vilken cloud som helst

### MLflow vs DVC
**MLflow:**
- Fokus på experiment-tracking
- Model registry
- UI för jämförelser

**DVC:**
- Fokus på data och pipeline-versioning
- Git-baserat workflow
- Mer kod-centrerat

### Kaggle/Colab vs DVC
**Kaggle/Colab:**
- Bra för prototyping
- Begränsat för produktion
- Svårt att versionshantera

**DVC:**
- Professionellt workflow
- Reproducerbarhet
- Team collaboration

---

## Fördelar och Nackdelar

### ✅ Fördelar
- **Reproducerbarhet**: Exakt samma data och kod
- **Collaboration**: Enkelt att dela stora datasets
- **Experiment-tracking**: Spåra alla försök
- **Pipeline-automation**: Automatisera ML-flöden
- **Git-integration**: Familjärt för utvecklare
- **Storage-flexibilitet**: Fungerar med alla cloud-providers

### ❌ Nackdelar
- **Inlärningskurva**: Nytt verktyg att lära sig
- **Complexity**: Kan vara overkill för små projekt
- **Storage-kostnader**: Molnlagring kostar
- **Network-dependency**: Behöver internet för data
- **Setup-tid**: Kräver initial konfiguration

---

## När ska man använda DVC?

### ✅ Perfekt för:
- **ML-projekt** med stora datasets (>100MB)
- **Team-projekt** med flera utvecklare
- **Experiment-tunga** projekt
- **Produktions-ML** som behöver reproducerbarhet
- **Forskningsprojekt** med dataversionering

### ❌ Overkill för:
- **Små projekt** med lite data (<10MB)
- **Enkel dataanalys** utan ML
- **Prototyping** i Jupyter notebooks
- **Statisk data** som aldrig ändras

### Exempel på perfekta användningsfall:
```
1. Bildklassificering med 10GB bilder
2. NLP-modell med flera text-corpus
3. Tidsserie-analys med historisk data
4. Computer vision med annoterad data
5. Rekommendationssystem med user-behavior data
```

---

## Installation och Setup

### Installation
```bash
# Via pip
pip install dvc

# Med cloud support
pip install dvc[gs]  # Google Cloud
pip install dvc[s3]  # AWS S3
pip install dvc[all] # Alla providers

# Via conda
conda install -c conda-forge dvc
```

### Snabb Start
```bash
# 1. Initiera DVC i Git repo
git init
dvc init
git add .dvc/
git commit -m "Initialize DVC"

# 2. Lägg till remote storage
dvc remote add -d myremote gs://my-bucket/dvc

# 3. Lägg till data
dvc add data/large_file.csv
git add data/large_file.csv.dvc .gitignore
git commit -m "Add data"

# 4. Pusha
dvc push
git push
```

---

## Best Practices

### 1. Struktur
```
project/
├── data/
│   ├── raw/           # Original data
│   ├── processed/     # Cleaned data  
│   └── features/      # Feature files
├── models/            # Trained models
├── scripts/           # Processing scripts
├── dvc.yaml          # Pipeline definition
├── params.yaml       # Parameters
└── .dvc/             # DVC config
```

### 2. Namngivning
```bash
# Bra: Beskrivande namn
data/customer_reviews_2024.csv
models/sentiment_classifier_v2.pkl

# Dåligt: Generiska namn
data/data.csv
models/model.pkl
```

### 3. Remote Storage
```bash
# Separera olika typer av data
gs://company-bucket/
├── raw-data/         # Original datasets
├── processed-data/   # Cleaned data
├── models/          # Trained models
└── experiments/     # Temporary experiment data
```

### 4. .gitignore
DVC skapar automatiskt `.gitignore`-entries:
```gitignore
# DVC-tracked files
/data/dataset.csv
/models/classifier.pkl

# DVC cache
/.dvc/cache
```

---

## Sammanfattning

### Vad är DVC?
- **Git för data** - versionshantera stora filer
- **Pipeline-verktyg** - automatisera ML-workflows  
- **Experiment-tracker** - spåra och jämföra försök
- **Collaboration-tool** - dela data i team

### Huvudkoncept:
- **`.dvc` filer** = Pekare till stora filer
- **Remote storage** = Molnlagring för faktisk data
- **Pipelines** = Automatiserade ML-flöden
- **Experiments** = Spårade försök med parametrar

### Varför använda?
- Reproducerbara ML-experiment
- Effektiv team-collaboration
- Professionellt data-workflow
- Integration med befintliga Git-processer

### Alternativ:
- **Git LFS** - enklare för basic behov
- **MLflow** - fokus på experiment-tracking
- **Weights & Biases** - cloud-baserat alternativ
- **Kubeflow** - Kubernetes-baserat

**Bottom line:** DVC är perfekt för seriösa ML-projekt där reproducerbarhet och team-collaboration är viktigt. För enkla experiment räcker vanlig Git, men för produktions-ML är DVC nästan ett måste!
