Mac Miller Lyric Analysis ETL Pipeline

This project is an end-to-end data engineering pipeline that extracts, processes, and analyzes song lyrics from Mac Miller's albums. The pipeline leverages a modern data stack to ingest data from public APIs, transform it in the cloud using AWS, and load it into a Snowflake data warehouse for analytics.

🏛️ Cloud Architecture
The pipeline is designed with a clear separation of concerns, moving data through distinct zones in a cloud data lake environment. The complete workflow diagram can be found in the architecture/ directory.
Architecture Breakdown
Data Extraction (Local): A Python script is run locally to connect to the Spotify API (for track/album metadata) and the Genius API (for lyrics URLs). It then scrapes the raw lyrics text.
S3 Data Lake (Landing Zone): The raw, unstructured data from the script is uploaded as .jsonl files to a raw zone (/raw) in an AWS S3 bucket. This serves as the permanent, immutable source of truth.
Schema Discovery (Glue Data Catalog): An AWS Glue Crawler automatically scans the raw data in S3. It infers the schema and creates a metadata table in the AWS Glue Data Catalog, making the data queryable.
ETL Transformation (AWS Glue): An AWS Glue ETL job, written in PySpark, reads the raw data from the catalog. It performs a series of cleaning transformations (e.g., removing headers, punctuation, and extra whitespace) on the raw lyrics.
S3 Data Lake (Processed Zone): The Glue job writes the clean, structured data to a processed zone (/processed) in the S3 bucket. The data is saved in the columnar Parquet format, which is highly optimized for analytics.
Data Warehousing (Snowflake): The clean Parquet data is efficiently loaded from the S3 processed zone into a final analytics table in Snowflake using the COPY command, making it available for high-performance SQL queries.
🛠️ Tech Stack
Category
Technology
Data Ingestion
Python, requests, BeautifulSoup4
Cloud Provider
AWS (Amazon Web Services)
Data Lake
AWS S3
ETL & Catalog
AWS Glue (Crawlers, PySpark ETL Jobs)
Data Warehouse
Snowflake
BI (Future)
Amazon Quicksight, Tableau

📁 Project Structure
/
├── architecture/
│   └── lyrics_etl.png              # Workflow diagram of the pipeline
├── data/
│   └── ...                         # Directory for raw output data (.jsonl files)
├── docs/
│   ├── glue_crawler_setup.md       # Instructions for setting up the Glue Crawler
│   ├── iam_roles_setup.md          # Guide for configuring necessary IAM permissions
│   └── snowflake_s3_integration.md # Steps for integrating Snowflake with S3
├── glue_jobs/
│   └── clean_lyrics.py             # PySpark script for the AWS Glue cleaning job
├── scripts/
│   └── 1_fetch_lyrics.py           # Local Python script to fetch and scrape raw lyrics
├── snowflake/
│   ├── 1_setup_integration.sql     # SQL for creating the S3 Stage and Integration
│   └── 2_load_data.sql             # SQL for creating the final table and loading data
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


🚀 Setup and Usage
1. Prerequisites
Python 3.8+
An AWS account with appropriate IAM permissions for S3 and Glue.
A Snowflake account.
API credentials from Spotify for Developers and Genius API.
2. Local Setup
Clone the repository and install the required Python packages.
git clone <your-repository-url>
cd music-sentiment-pipeline
pip install -r requirements.txt


3. Configure Environment Variables
Create a .env file in the project root by copying the template, then add your API keys:
cp .env.example .env


Now, edit the .env file with your secret credentials.
4. Running the Pipeline
Run Local Script: Execute scripts/1_fetch_lyrics.py to generate the raw .jsonl files.
Upload to S3: Upload the contents of the data/ folder to your S3 raw zone.
Run Glue Crawler: Run your Glue Crawler to catalog the raw data.
Run Glue ETL Job: Execute the Glue job using the script from glue_jobs/clean_lyrics.py.
Load into Snowflake: Run the SQL scripts in the snowflake/ directory in order (1_setup_integration.sql then 2_load_data.sql) to load the data.
📄 Detailed Documentation
For detailed setup instructions on the cloud components, please refer to the documents in the docs/ directory:
iam_roles_setup.md: A guide for configuring the necessary IAM roles and permissions.
glue_crawler_setup.md: Instructions for setting up the AWS Glue Crawler.
snowflake_s3_integration.md: Steps for securely integrating Snowflake with your S3 bucket.
🔮 Future Work
Emotion Analysis: Implement a second Glue job to perform emotion classification on the cleaned lyrics.
Orchestration: Automate the entire pipeline using AWS Step Functions or Apache Airflow.
Visualization: Connect a BI tool like Amazon Quicksight to the Snowflake table to build interactive dashboards.
