FROM python:3.10

WORKDIR /app

COPY . /app

ENV EMAIL=""

ENV APP_PASSWORD=""

CMD ["python", "transactions.py"]
