AWS Glue Crawler Setup
This guide explains how to create the Glue Crawler to catalog your raw data in S3.

Navigate to AWS Glue: In the AWS Management Console, go to the AWS Glue service.

Create a Crawler:

On the left menu, select Crawlers and click Create crawler.

Give your crawler a name, like music-lyrics-crawler.

Specify Data Source:

For the data source, choose S3.

For the S3 path, provide the path to your "raw" data folder (e.g., s3://your-bucket-name/raw/).

Configure IAM Role:

Choose the IAM role you created in the iam_roles_setup.md guide.

Set the Output Database:

Choose a database for your catalog table. If you don't have one, click Add database and create one (e.g., music_data_db).

Review and Create: Review your settings and click Create crawler.

Run Crawler: Once created, select your crawler from the list and click Run crawler. When it finishes, a new table will appear in your data catalog.