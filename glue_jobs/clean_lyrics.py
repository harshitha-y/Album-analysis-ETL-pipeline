import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, lower, regexp_replace, trim, substring, instr

# --- Boilerplate Glue Code ---
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# --- ETL Logic ---

# 1. Load your raw data from the Glue Data Catalog
#    Replace database and table_name with your actual values
input_dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database="music_data_db",
    table_name="raw_lyrics_data"
)

input_df = input_dynamic_frame.toDF()

# 2. Perform robust cleaning transformations
cleaned_df = input_df \
    .filter(col("lyrics").isNotNull()) \
    .withColumn("start_position",
        instr(col("lyrics"), "[")
    ) \
    .filter(col("start_position") > 0) \
    .withColumn("lyrics_body",
        substring(col("lyrics"), col("start_position"), 100000)
    ) \
    .withColumn("cleaned_lyrics",
        lower(col("lyrics_body"))
    ) \
    .withColumn("cleaned_lyrics",
        regexp_replace(col("cleaned_lyrics"), r'\[[\s\S]*?\]', '')
    ) \
    .withColumn("cleaned_lyrics",
        regexp_replace(col("cleaned_lyrics"), r"[^\w\s']", '')
    ) \
    .withColumn("cleaned_lyrics",
        regexp_replace(col("cleaned_lyrics"), r'\s+', ' ')
    ) \
    .withColumn("cleaned_lyrics",
        trim(col("cleaned_lyrics"))
    )

# 3. Select the final columns for your output
final_df = cleaned_df.select(
    col("artist").alias("artist_name"),
    col("album").alias("album_name"),
    col("track_title"),
    col("genius_url"),
    col("cleaned_lyrics").alias("lyrics")
)

# 4. Write the clean DataFrame to your "processed" S3 zone in Parquet format
#    Replace with your actual S3 bucket path
output_path = "s3://your-bucket-name/processed/"
final_df.repartition(1).write.mode("overwrite").parquet(output_path)
