# backend/Dockerfile

# --- Build Stage ---
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# WORKDIR for build stage remains /app
WORKDIR /app

# Create and activate venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into /app/app
COPY ./app /app/app

# --- Runtime Stage ---
FROM python:3.12-slim as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set WORKDIR to the directory containing main.py
WORKDIR /app/app

# Copy venv from builder stage to /opt/venv
COPY --from=builder /opt/venv /opt/venv
# Copy app code from builder stage's /app/app into the final WORKDIR (/app/app)
COPY --from=builder /app/app /app/app

# Set path to use venv python
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 8000
EXPOSE 8000

# Run Uvicorn relative to the new WORKDIR (/app/app)
# It will look for 'main.py' in the current WORKDIR
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]