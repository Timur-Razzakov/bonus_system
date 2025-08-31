FROM python:3.12.10-alpine3.21
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    libnsl \
    libaio \
    curl \
    unzip \
    git \
    openssl-dev \
    build-base

COPY . .

RUN pip install --no-cache-dir -r requirements/base.txt
RUN pip install --no-cache-dir -r requirements/local.txt
RUN pip install --no-cache-dir -r requirements/test.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
