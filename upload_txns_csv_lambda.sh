#!/bin/bash

# Variables
S3_BUCKET="your-s3-bucket-name"
LOCAL_FILE_PATH="txns.csv"
S3_KEY="txns.csv"

# Upload to S3
aws s3 cp "${LOCAL_FILE_PATH}" "s3://${S3_BUCKET}/${S3_KEY}"
