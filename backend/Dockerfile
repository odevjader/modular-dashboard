# backend/Dockerfile

# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# --- ADDED: Install System Dependencies (Builder Stage) ---
# Install poppler, Tesseract OCR engine, Portuguese language pack, and libmagic
# Needed for PDF processing and OCR capabilities potentially during pip install or later
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libmagic1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# --- END Added System Dependencies ---

# Create and activate venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies (AFTER system deps are installed)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into /app/app in the builder stage
COPY ./app /app/app

# --- Stage 2: Runtime ---
FROM python:3.12-slim as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set WORKDIR to the final application directory
WORKDIR /app/app

# --- ADDED: Install System Dependencies (Runtime Stage) ---
# Install runtime libraries needed by the application and installed packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libmagic1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# --- END Added Runtime System Dependencies ---

# Copy venv from builder stage
COPY --from=builder /opt/venv /opt/venv
# Copy app code from builder stage
COPY --from=builder /app/app /app/app

# Set path to use venv python
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Run Uvicorn relative to the WORKDIR (/app/app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]