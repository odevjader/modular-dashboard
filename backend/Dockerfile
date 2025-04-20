# backend/Dockerfile

# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# Install System Dependencies (including libpq5)
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

# Install Python dependencies ONLY from requirements file
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir # Using pip cache now

# REMOVED Explicit installs below - rely on requirements.txt
# RUN pip install alembic
# RUN pip install psycopg2-binary

# Copy application code
COPY ./app /app/app

# --- Stage 2: Runtime ---
FROM python:3.12-slim as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app/app

# Install Runtime System Dependencies (including libpq5)
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
# Copy app code from builder stage
COPY --from=builder /app/app /app/app

# Set path to use venv python
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Run Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]