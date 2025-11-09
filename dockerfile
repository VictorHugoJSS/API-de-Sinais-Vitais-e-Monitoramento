FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y vim git

COPY api/requirements.txt .

RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt

COPY api/ .

ENV FLASK_APP=Api.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["python", "Api.py"]
