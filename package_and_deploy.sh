#!/bin/bash

# Set your AWS Lambda function name and ZIP file name
FUNCTION_NAME="txns_processor_and_emailer"
ZIP_FILE="txns_processor_and_emailer.zip"

# Package your Python code and dependencies into a ZIP file
zip -r $ZIP_FILE transactions.py

# Upload the ZIP file to AWS Lambda
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb://$ZIP_FILE

# Clean up - remove the temporary ZIP file
rm $ZIP_FILE