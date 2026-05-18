FROM python:3.12-slim

LABEL description="Container armazenamento persistente via volume"
LABEL version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DADOS_DIR=/app/dados

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY app.py .

VOLUME ["/app/dados"]

CMD ["python", "app.py"]