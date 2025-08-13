USE music_analysis_db.public;

-- Step 1: Create the final analytics table
CREATE OR REPLACE TABLE lyrics_data (
    artist_name VARCHAR,
    album_name VARCHAR,
    track_title VARCHAR,
    genius_url VARCHAR,
    lyrics VARCHAR
);

-- Step 2: Load the data from the S3 stage into the table
COPY INTO lyrics_data
  FROM @my_s3_processed_stage
  MATCH_BY_COLUMN_NAME = 'CASE_INSENSITIVE';

-- Step 3: Verify the data was loaded successfully
SELECT * FROM lyrics_data LIMIT 10;

-- Optional: Check the row count to ensure all data was loaded
SELECT COUNT(*) FROM lyrics_data;
