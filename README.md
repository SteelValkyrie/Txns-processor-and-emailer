### Description

The transactions.py file reads and processes files from a csv file called "txns.cvs" and sends an email with information regarding those transactions to the customer.
For terms of this challenge the customer's email is created from the given emailer for testing.

You would also need to setup an app password to use gmail to be able to authenticate and send the email from python.

### Setup

Get an app password from gmail:
https://support.google.com/mail/answer/185833?hl=en

The repo already contains a csv file of transactions to process

Build the image:
```bash
$ docker build . -t tnxs-processor-emailer
```

### Running script

To run the script once and input env variables:
```bash
$ docker run -e EMAIL=your-emailer-account -e APP_PASSWORD=your-email-app-password txns
```