import os
import csv
from datetime import datetime
import smtplib, ssl
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3
import csv
import io


def lambda_handler(event, context):
    # Function to be executed by AWS Lambda
    s3_client = boto3.client("s3")
    S3_BUCKET = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]
    file_content = (
        s3_client.get_object(Bucket=S3_BUCKET, Key=object_key)["Body"]
        .read()
        .decode("utf-8")
    )
    csv_reader = csv.DictReader(io.StringIO(file_content))
    transactions = [row for row in csv_reader]
    process_transactions_and_send_email(transactions)


def read_transactions(filename: str) -> list[dict]:
    """
    Reads transactions from a CSV file.

    Args:
        filename: The name of the CSV file to read from.

    Returns:

    """
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        transactions = [row for row in reader]
    return transactions


def process_transactions_and_send_email(transactions: list[dict]) -> None:
    """
    Processes transactions and sends email to customers.

    Args:

    """
    total_balance = 0
    transactions_by_month = defaultdict(int)
    credit_by_month = defaultdict(float)
    debit_by_month = defaultdict(float)
    total_credit = 0
    total_debit = 0

    for transaction in transactions:
        date = datetime.strptime(transaction["Date"], "%m/%d")

        transaction_amount = float(transaction["Transaction"])
        total_balance += transaction_amount

        transactions_by_month[date.strftime("%B")] += 1

        if transaction_amount > 0:
            credit_by_month[date.strftime("%B")] += transaction_amount
            total_credit += transaction_amount
        else:
            debit_by_month[date.strftime("%B")] += transaction_amount
            total_debit += transaction_amount

    avg_credit_amount = total_credit / len(credit_by_month)
    avg_debit_amount = total_debit / len(debit_by_month)

    avg_credit_by_month = {
        month: credit / transactions_by_month[month]
        for month, credit in credit_by_month.items()
    }
    avg_debit_by_month = {
        month: debit / transactions_by_month[month]
        for month, debit in debit_by_month.items()
    }

    port = 465  # For SSL
    email = os.environ.get("EMAIL", None)
    if email is None:
        raise ValueError("Email not found in environment variables")
    password = os.environ.get("APP_PASSWORD", None)
    if password is None:
        raise ValueError("App password not found in environment variables")
    user, domain = email.split("@")
    customer_email = f"{user}+customer@{domain}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Your monthly report"
    message["From"] = email
    message["To"] = customer_email

    transactions_by_month = dict(transactions_by_month)
    credit_by_month = dict(credit_by_month)
    debit_by_month = dict(debit_by_month)
    avg_credit_by_month = dict(avg_credit_by_month)
    avg_debit_by_month = dict(avg_debit_by_month)

    text = f"Total balance: {total_balance:.2f}\n\n"

    for month, num_transactions in transactions_by_month.items():
        text += f"Number of transactions in {month}: {num_transactions}\n"
        text += f"Average credit in {month}: {avg_credit_by_month[month]:.2f}\n"
        text += f"Average debit in {month}: {avg_debit_by_month[month]:.2f}\n\n"

    text += f"Total credit: {total_credit:.2f}\n"
    text += f"Total debit: {total_debit:.2f}\n\n"
    text += f"Average credit: {avg_credit_amount:.2f}\n"
    text += f"Average debit: {avg_debit_amount:.2f}\n"

    html = f"""
    <html>
        <body>
            <p>Total balance: {total_balance:.2f}</p>
    """

    for month, num_transactions in transactions_by_month.items():
        html += f"<p>Number of transactions in {month}: {num_transactions}</p>"
        html += f"<p>Average credit in {month}: {avg_credit_by_month[month]:.2f}</p>"
        html += f"<p>Average debit in {month}: {avg_debit_by_month[month]:.2f}</p>"

    html += f"<p>Total credit: {total_credit:.2f}</p>"
    html += f"<p>Total debit: {total_debit:.2f}</p>"
    html += f"<p>Average credit: {avg_credit_amount:.2f}</p>"
    html += f"<p>Average debit: {avg_debit_amount:.2f}</p>"

    html += """
        <img src="https://blog.storicard.com/wp-content/uploads/2019/07/Stori-horizontal-11.jpg" alt="Stori" style="width: 300px; height: 100px;">
        </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, customer_email, message.as_string())
        print("Email sent!")


if __name__ == "__main__":
    csv_filename = "txns.csv"
    transactions = read_transactions(csv_filename)
    process_transactions_and_send_email(transactions)
