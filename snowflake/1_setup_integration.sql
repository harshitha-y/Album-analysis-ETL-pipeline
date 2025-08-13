-- Step 1: Create a database and warehouse if they don't exist
CREATE WAREHOUSE IF NOT EXISTS my_wh;
CREATE DATABASE IF NOT EXISTS music_analysis_db;
USE music_analysis_db.public;

-- Step 2: Create a Storage Integration to securely connect to your AWS account
-- Replace 'YOUR_IAM_ROLE_ARN' and 'your-bucket-name' with your actual values
CREATE OR REPLACE STORAGE INTEGRATION s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = S3
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::ACCOUNT_ID:role/YOUR_IAM_ROLE_NAME' --<-- UPDATE THIS
  STORAGE_ALLOWED_LOCATIONS = ('s3://your-bucket-name/processed/'); --<-- UPDATE THIS

-- Step 3: IMPORTANT - Retrieve Snowflake's credentials to grant access in AWS
-- Run this command and follow the instructions in 'docs/snowflake_s3_integration.md'
DESC INTEGRATION s3_integration;

-- Step 4: Create a File Format for Parquet files
CREATE OR REPLACE FILE FORMAT my_parquet_format
  TYPE = PARQUET;

-- Step 5: Create an External Stage that points to your processed data
CREATE OR REPLACE STAGE my_s3_processed_stage
  STORAGE_INTEGRATION = s3_integration
  URL = 's3://your-bucket-name/processed/' --<-- UPDATE THIS
  FILE_FORMAT = my_parquet_format;
