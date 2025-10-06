FROM python:3.12-alpine
LABEL authors="benfict1@gmail.com"

ENV PYTHONNBUFFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
