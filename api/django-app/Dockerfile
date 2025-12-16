FROM python:3.13.9-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    ffmpeg \
    libffi-dev \
    openssl-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["./entrypoint.sh", "gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120", "--worker-class", "gevent", "--workers", "3"]
