FROM python:3.9.7-slim

RUN apt-get update \
    && apt-get install -y gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

ENV FLASK_APP processReceipts.py

CMD ["flask", "run", "--host=0.0.0.0"]