# backend/Dockerfile

# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# Install System Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libmagic1 \
    libpq5 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and activate venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir # Considere remover --no-cache-dir se o build ainda estiver lento

# Copy application code into /app/app relative to WORKDIR /app
COPY ./app /app/app

# --- Stage 2: Runtime ---
FROM python:3.12-slim as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# --- WORKDIR MODIFICADO ---
WORKDIR /app # Define /app como diretório base

# Install Runtime System Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libmagic1 \
    libpq5 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy venv from builder stage
COPY --from=builder /opt/venv /opt/venv
# Copy app code from builder stage (source /app/app, dest /app/app)
# O código da aplicação reside em /app/app
COPY --from=builder /app/app /app/app

# Set path to use venv python
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

# --- CMD MODIFICADO ---
# Uvicorn agora executa a partir de /app e procura 'main:app' dentro do diretório 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]