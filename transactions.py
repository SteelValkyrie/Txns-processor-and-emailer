import csv
from datetime import datetime
import smtplib, ssl
from collections import defaultdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

    avg_credit_by_month = {
        month: credit / transactions_by_month[month]
        for month, credit in credit_by_month.items()
    }
    avg_debit_by_month = {
        month: debit / transactions_by_month[month]
        for month, debit in debit_by_month.items()
    }

    port = 465  # For SSL
    email = input("Type your email and press enter: ")
    password = input("Type your password and press enter: ")
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

    text = """
    Your total balance is {}.

    Transactions by month:
    {}

    Credits by month:
    {}

    Debits by month:
    {}

    Average credit by month:
    {}

    Average debit by month:
    {}

    Your total credit is {}.
    Your total debit is {}.
    """.format(
        total_balance,
        "\n".join(
            [
                f"{month}: {count} transactions"
                for month, count in transactions_by_month.items()
            ]
        ),
        "\n".join(
            [f"{month}: ${credit:.2f}" for month, credit in credit_by_month.items()]
        ),
        "\n".join(
            [f"{month}: ${debit:.2f}" for month, debit in debit_by_month.items()]
        ),
        "\n".join(
            [f"{month}: ${avg:.2f}" for month, avg in avg_credit_by_month.items()]
        ),
        "\n".join(
            [f"{month}: ${avg:.2f}" for month, avg in avg_debit_by_month.items()]
        ),
        total_credit,
        total_debit,
    )

    html = """
    <html>
        <body>
            <p>Your total balance is {}.</p>
            
            <p>Transactions by month:</p>
            <ul>
                {}
            </ul>

            <p>Credits by month:</p>
            <ul>
                {}
            </ul>

            <p>Debits by month:</p>
            <ul>
                {}
            </ul>

            <p>Average credit by month:</p>
            <ul>
                {}
            </ul>

            <p>Average debit by month:</p>
            <ul>
                {}
            </ul>

            <p>Your total credit is ${:.2f}.</p>
            <p>Your total debit is ${:.2f}.</p>

            <img src="https://blog.storicard.com/wp-content/uploads/2019/07/Stori-horizontal-11.jpg" alt="Stori" style="width: 300px; height: 100px;">

        </body>
    </html>
    """.format(
        total_balance,
        "".join(
            [
                f"<li>{month}: {count} transactions</li>"
                for month, count in transactions_by_month.items()
            ]
        ),
        "".join(
            [
                f"<li>{month}: ${credit:.2f}</li>"
                for month, credit in credit_by_month.items()
            ]
        ),
        "".join(
            [
                f"<li>{month}: ${debit:.2f}</li>"
                for month, debit in debit_by_month.items()
            ]
        ),
        "".join(
            [
                f"<li>{month}: ${avg:.2f}</li>"
                for month, avg in avg_credit_by_month.items()
            ]
        ),
        "".join(
            [
                f"<li>{month}: ${avg:.2f}</li>"
                for month, avg in avg_debit_by_month.items()
            ]
        ),
        total_credit,
        total_debit,
    )

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