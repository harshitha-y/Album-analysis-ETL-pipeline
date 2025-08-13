IAM Role and Permissions Setup
This guide outlines the necessary IAM role and policies for the AWS Glue job to access S3 and CloudWatch.

1. Create the IAM Role
In the AWS IAM console, go to Roles and click Create role.

For Trusted entity type, select AWS service.

For Use case, choose Glue and click Next.

The AWSGlueServiceRole policy will be pre-selected. Click Next.

Give the role a name (e.g., AWSGlueServiceRole-AlbumAnalysis) and click Create role.

2. Add S3 and CloudWatch Permissions
Find the role you just created and click on its name.

On the Permissions tab, click Add permissions > Create inline policy.

Select the JSON tab and paste the following policy. Remember to replace your-bucket-name.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3AccessForMusicETL",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/raw/*",
                "arn:aws:s3:::your-bucket-name/processed/*"
            ]
        },
        {
            "Sid": "S3ListBucket",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::your-bucket-name"
        },
        {
            "Sid": "CloudWatchLogsAccess",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws-glue/jobs/*"
        }
    ]
}

Review and create the policy.

3. Add PassRole Permission
While still on the role's page, create another inline policy.

Select the JSON tab and paste the following policy. Remember to replace the account ID and role name.

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/service-role/YOUR_GLUE_ROLE_NAME",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "glue.amazonaws.com"
                }
            }
        }
    ]
}

Review and create the policy.