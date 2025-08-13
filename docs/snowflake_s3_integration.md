Snowflake S3 Integration Setup
This guide explains how to update your IAM role's Trust Policy to allow Snowflake to securely access your S3 bucket.

1. Get Credentials from Snowflake
First, run the 1_setup_integration.sql script in Snowflake. The most important command is:

DESC INTEGRATION s3_integration;

From the output of this command, copy two values:

STORAGE_AWS_IAM_USER_ARN

STORAGE_AWS_EXTERNAL_ID

2. Edit the IAM Role's Trust Policy
In the AWS IAM console, navigate to Roles and select your Glue role.

Click the Trust relationships tab and then Edit trust policy.

Replace the entire JSON with the following template. This policy trusts both the AWS Glue service and the Snowflake user.

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "glue.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "PASTE_YOUR_STORAGE_AWS_IAM_USER_ARN_HERE"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "PASTE_YOUR_STORAGE_AWS_EXTERNAL_ID_HERE"
        }
      }
    }
  ]
}

Paste the STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID values you copied from Snowflake into the appropriate placeholders.

Click Update policy.

After waiting about a minute, your Snowflake stage will be able to securely connect to your S3 bucket.