## Description

The transactions.py file reads and processes files from a csv file called "txns.cvs" and sends an email with information regarding those transactions to the customer.
For terms of this challenge the customer's email is created from the given emailer for testing.

You would also need to setup an app password to use gmail to be able to authenticate and send the email from python.

## Setup

Get an app password from gmail:
https://support.google.com/mail/answer/185833?hl=en

The repo already contains a csv file of transactions to process

### Docker

Build the image:
```bash
$ docker build . -t tnxs-processor-emailer
```

### Running script with docker

To run the script once and input env variables:
```bash
$ docker run -e EMAIL=your-emailer-account -e APP_PASSWORD=your-email-app-password txns
```

### AWS Lambda

-Create an S3 Bucket to upload csv file into and update the "upload_txns_csv_lambda.sh" file with it's name

-Create an AWS Lambda function and setup to receive file upload events from previous S3 Buckets

-Install and configure AWS CLI with your credentials 

-Setup environment variables:
```bash
aws lambda update-function-configuration --function-name txns_processor_and_emailer --environment "Variables={EMAIL=YOUR_EMAIL,APP_PASSWORD=YOUR_APP_PASSWORD}"
```

-Package and deploy running file:
```bash
package_and_deploy.sh
```

### Running script with AWS Lambda

Run the script by uploading the txns.csv file to lambda running the script:
```bash
upload_txns_csv_lambda.sh
```