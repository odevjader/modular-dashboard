# backend/Dockerfile

# --- Build Stage ---
# Use Python 3.12 to match your development environment
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# Create and activate venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# This copies the *contents* of the local 'backend/app' directory
# into '/app/app' inside the container image.
COPY ./app/ /app/app/

# --- Runtime Stage ---
# Use Python 3.12 for the runtime stage as well
FROM python:3.12-slim as runtime

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

# Copy venv and app code from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app/app/ /app/app/

# Set path to use venv python
ENV PATH="/opt/venv/bin:$PATH"

# Expose port 8000 (default for Uvicorn)
EXPOSE 8000

# Run the application using Uvicorn
# Looks for 'app' instance in '/app/app/main.py' relative to WORKDIR (/app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]