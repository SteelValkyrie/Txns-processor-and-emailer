FROM python:3.10

WORKDIR /app

COPY . /app

ENV EMAIL=""

ENV APP_PASSWORD=""

RUN pip install boto3

CMD ["python", "transactions.py"]
