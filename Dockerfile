FROM python:3.13.3-alpine3.20
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    cargo \
    rust \
    openssl-dev \
    build-base
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app/
RUN apk add --no-cache postgresql-client
RUN dos2unix /app/scripts/entrypoint_backend.sh
RUN chmod +x /app/scripts/entrypoint_backend.sh
COPY --chmod=0644 .env /app/