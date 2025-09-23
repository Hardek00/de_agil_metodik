# PySpark Exercise: From Local to Cloud with GCP Dataproc

## Overview
In this exercise, you'll learn the basics of PySpark by running it locally on your machine, then scaling it to the cloud using Google Cloud Dataproc. You'll process a dataset of your choice (e.g., a small CSV from Kaggle like Iris flowers or e-commerce sales).

**Prerequisites**:
- Python 3.8+ installed.
- A Google Cloud Platform (GCP) account (free tier available with $300 credits).
- Basic terminal/command line knowledge.

**Objectives**:
- Install and run PySpark locally.
- Submit a Spark job to a Dataproc cluster in GCP.
- Understand the difference between local and distributed processing.

---

## Part 1: Run PySpark Locally
You'll install PySpark, create a simple script to process a small dataset, and run it on your machine.

### Step 1.1: Install PySpark
1. **Install Java** (required for Spark; skip if already installed—check with `java -version` in terminal; it should show Java 8 or 11).
   - **Windows**: Download JDK 8 or 11 from [Oracle](https://www.oracle.com/java/technologies/downloads/) or use OpenJDK. Install and add to PATH (e.g., set `JAVA_HOME` environment variable).
   - **macOS**: Use Homebrew: `brew install openjdk@11`. Add to PATH: `export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"`.
   - **Linux**: `sudo apt update && sudo apt install openjdk-11-jdk` (Ubuntu) or `sudo yum install java-11-openjdk-devel` (CentOS).
   - Verify: Run `java -version`. If it's not 8 or 11, uninstall and reinstall the correct version.

2. Open your terminal (e.g., Command Prompt on Windows, Terminal on macOS/Linux).
3. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv spark-venv
   source spark-venv/bin/activate  # On Windows: spark-venv\Scripts\activate
   ```
4. Install PySpark:
   ```
   pip install pyspark
   ```
5. Verify installation:
   ```
   python -c "import pyspark; print(pyspark.__version__)"
   ```
   - Expected: A version like "3.5.0".

### Step 1.2: Prepare a Small Dataset
- Choose and download a small CSV dataset (e.g., Iris from https://archive.ics.uci.edu/dataset/53/iris as `iris.csv`).
- Place it in a working directory (e.g., `~/spark-exercise/`).

### Step 1.3: Create and Run a Local PySpark Script
1. Create a file named `local_spark.py` with this code (adapt for your dataset):
   ```python
   from pyspark.sql import SparkSession
   from pyspark.sql import functions as F

   if __name__ == "__main__":
       # Create local SparkSession
       spark = SparkSession.builder \
           .appName("LocalSparkExercise") \
           .master("local[*]") \
           .getOrCreate()

       # Load your CSV (update path)
       csv_path = "iris.csv"  # Replace with your file path
       df = spark.read.csv(csv_path, header=True, inferSchema=True)

       # Basic operations: Show summary
       df.show(5)
       df.printSchema()

       # Aggregate: Example for Iris - average sepal length by class
       agg_df = df.groupBy("class").agg(F.avg("sepal_length").alias("Avg_Sepal_Length"))
       agg_df.show()

       spark.stop()
   ```

2. Run it locally:
   ```
   spark-submit local_spark.py
   ```
   - Output: Shows data summary and aggregates in the terminal.

### Step 1.4: Questions to Answer
- What is the purpose of `master("local[*]")`?
- How long did the script take to run? Try a larger dataset—what happens?

---

## Part 2: Run a Spark Job on GCP Dataproc
Now, scale to the cloud: Upload data/script to GCS, create a Dataproc cluster, and submit a job.

### Step 2.1: Set Up GCP
1. Log into GCP Console (console.cloud.google.com).
2. Enable Dataproc API (search for "Dataproc" > Enable if not already).
3. Create a GCS bucket (Storage > Create Bucket) for your data/script (e.g., "my-spark-bucket").
4. Upload your CSV to the bucket (e.g., via Console or `gsutil cp iris.csv gs://my-spark-bucket/iris.csv`—install gsutil if needed via gcloud SDK).

### Step 2.2: Create a Dataproc Cluster
1. In Console: Dataproc > Clusters > Create Cluster.
2. Name: "my-spark-cluster".
3. Region: Choose one (e.g., us-central1 for low cost).
4. Type: Standard (1 master + 2 workers, n2-standard-2 machines for cheap/small).
5. Enable preemptible workers for savings.
6. Create—it takes ~5 minutes.

### Step 2.3: Adapt and Submit a Job
1. Create `cloud_spark.py` (adapt from local script; update paths):
   ```python
   from pyspark.sql import SparkSession
   from pyspark.sql import functions as F

   if __name__ == "__main__":
       spark = SparkSession.builder \
           .appName("CloudSparkExercise") \
           .getOrCreate()  # No master—Dataproc handles it

       csv_path = "gs://my-spark-bucket/iris.csv"  # Your GCS path
       df = spark.read.csv(csv_path, header=True, inferSchema=True)

       agg_df = df.groupBy("class").agg(F.avg("sepal_length").alias("Avg_Sepal_Length"))
       agg_df.show()

       # Save output to GCS
       agg_df.write.csv("gs://my-spark-bucket/output")

       spark.stop()
   ```

2. Upload script to GCS: `gsutil cp cloud_spark.py gs://my-spark-bucket/cloud_spark.py`.
3. Submit job (via terminal with gcloud installed/authenticated):
   ```
   gcloud dataproc jobs submit pyspark \
       --cluster=my-spark-cluster \
       --region=us-central1 \
       gs://my-spark-bucket/cloud_spark.py
   ```
4. Monitor in Console (Dataproc > Jobs). Check output in GCS bucket.

### Step 2.4: Clean Up
- Delete the cluster after (Dataproc > Clusters > Delete) to avoid costs.

### Step 2.5: Questions to Answer
- How was the runtime different from local?
- What costs did you incur (check Billing)?
- Try a larger dataset—what changes?
