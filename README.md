🎶Album Lyrics Analysis ETL Pipeline

This project is an **end-to-end data engineering pipeline** that extracts, processes, and analyzes song lyrics from **Mac Miller’s albums**.

The pipeline leverages a **modern data stack** to:

* Ingest lyrics from public APIs
* Transform them in the cloud with **AWS Glue & PySpark**
* Load into **Snowflake** for analytics and future visualization

---

## 🏛️ Cloud Architecture

The pipeline is built with **layered zones** in an AWS data lake and integrates with Snowflake for scalable analytics.

📌 A full architecture diagram is available in [`architecture/lyrics_etl.png`](architecture/lyrics_etl.png).

Workflow Overview:

1. **Data Extraction (Local)** – Python script fetches track metadata (Spotify API) & lyrics (Genius API).
2. **Landing Zone (S3 Raw)** – Raw JSONL files uploaded to AWS S3 `/raw`.
3. **Schema Discovery (Glue Crawler)** – Infers schema & catalogs data.
4. **ETL Transformation (AWS Glue)** – PySpark cleaning: remove headers, punctuation, extra whitespace.
5. **Processed Zone (S3)** – Outputs structured **Parquet files** to `/processed`.
6. **Data Warehouse (Snowflake)** – Loads Parquet into analytics tables for **SQL queries**.

---

## 🛠️ Tech Stack

* Data Ingestion → Python, Requests, BeautifulSoup4
* Cloud → AWS (S3, Glue, IAM)
* ETL & Catalog → AWS Glue Crawlers + PySpark ETL Jobs
* Data Warehouse → Snowflake
* BI (Future) → Amazon QuickSight, Tableau

---

## 📁 Project Structure

```bash
/
├── architecture/               # Architecture diagram
│   └── lyrics_etl.png
├── data/                       # Raw & processed data (local)
├── docs/                       # Setup guides
│   ├── glue_crawler_setup.md
│   ├── iam_roles_setup.md
│   └── snowflake_s3_integration.md
├── glue_jobs/                  # PySpark ETL scripts
│   └── clean_lyrics.py
├── scripts/                    # Local ingestion scripts
│   └── 1_fetch_lyrics.py
├── snowflake/                  # SQL scripts for warehouse
│   ├── 1_setup_integration.sql
│   └── 2_load_data.sql
├── .env.example                # Env variable template
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🚀 Setup & Usage

### 1️⃣ Prerequisites

* Python **3.8+**
* AWS account with **S3 & Glue IAM permissions**
* Snowflake account
* API credentials: **Spotify Developer**, **Genius API**

### 2️⃣ Local Setup

```bash
git clone <your-repository-url>
cd music-sentiment-pipeline
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

```bash
cp .env.example .env
# Fill in your API keys and secrets
```

### 4️⃣ Run the Pipeline

1. Run local ingestion → `python scripts/1_fetch_lyrics.py`
2. Upload raw files → S3 `/raw` zone
3. Run Glue Crawler → catalog schema
4. Run Glue ETL job → `glue_jobs/clean_lyrics.py`
5. Load to Snowflake → run SQL scripts in `snowflake/`

---

## 📄 Documentation

* [`docs/iam_roles_setup.md`](docs/iam_roles_setup.md) → IAM roles & permissions
* [`docs/glue_crawler_setup.md`](docs/glue_crawler_setup.md) → AWS Glue setup
* [`docs/snowflake_s3_integration.md`](docs/snowflake_s3_integration.md) → Snowflake ↔ S3 integration

---

## 🔮 Future Work

* **Emotion Analysis** → emotion classification using NLP/LLMs
* **Orchestration** → Automate with AWS Step Functions / Apache Airflow
* **Visualization** → BI dashboards
