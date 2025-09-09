--warehouse and DB creation
CREATE WAREHOUSE IF NOT EXISTS my_wh;
CREATE DATABASE IF NOT EXISTS music_analysis_db;
USE music_analysis_db.public;

--Creating a Storage Integration to securely connect to AWS account

CREATE OR REPLACE STORAGE INTEGRATION s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::ACCOUNT_ID:role/YOUR_IAM_ROLE_NAME' --<-- UPDATE THIS
  STORAGE_ALLOWED_LOCATIONS = ('s3://your-bucket-name/processed/'); --<-- UPDATE THIS

-- Retrieve Snowflake's credentials to grant access in AWS
-- Run this command and get the ARN, add it to IAM trust policy
--Snowflake won’t have permission to read your bucket without this
DESC INTEGRATION s3_integration;

-- Creating a File Format for Parquet files
CREATE OR REPLACE FILE FORMAT my_parquet_format
  TYPE = PARQUET;

--Creating an External Stage that points to processed data
CREATE OR REPLACE STAGE my_s3_processed_stage
  STORAGE_INTEGRATION = s3_integration
  URL = 's3://your-bucket-name/processed/' --<-- UPDATE THIS
  FILE_FORMAT = my_parquet_format;
