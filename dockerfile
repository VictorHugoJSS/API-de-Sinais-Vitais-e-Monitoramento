FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y vim git

COPY requirements.txt ./

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt