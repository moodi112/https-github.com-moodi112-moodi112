# Multi-stage Dockerfile for Oman Wikipedia Generator
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY .flake8 .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.wiki_generator; print('OK')" || exit 1

# Default command (can be overridden)
CMD ["python", "-m", "src.cli", "--help"]

# Production stage
FROM base as production
LABEL maintainer="moodi112"
LABEL description="Oman Wikipedia Generator - AI-powered article generation"
LABEL version="1.0.0"

# Web interface stage (for future FastAPI app)
FROM base as web
EXPOSE 8000
CMD ["uvicorn", "src.web:app", "--host", "0.0.0.0", "--port", "8000"]
