# =============================================================================
# Dockerfile: Production Containerization for Library Reservation Gateway (LRG)
# Open-Source Containerized Deployment for SE Mini-Project
# =============================================================================

# Stage 1: Base Runtime Environment
FROM python:3.11-slim as base

# Set environment variables for optimized Python execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_ENV=production \
    PORT=5000

# Install system dependencies (curl for healthcheck probe)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first for caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application source code and seed files
COPY src/ /app/src/
COPY docs/ /app/docs/
COPY pytest.ini /app/

# Create a non-privileged user for security compliance (Principle of Least Privilege)
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose HTTP port
EXPOSE 5000

# Container Healthcheck probe (queries REST API /health endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Production WSGI entrypoint with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "--timeout", "60", "src.app:app"]
