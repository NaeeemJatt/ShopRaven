# ==============================================================================
# Hugging Face Spaces Unified Dockerfile for ShopRaven AI Co-Founder
# Bundles: Python 3.11 Backend (FastAPI), Celery Beat, Redis, and Node.js Orchestrator
# Port: 7860 (Hugging Face default)
# ==============================================================================

FROM python:3.11-slim

# Prevent prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies: Redis, Supervisor, Node.js 20, and Pillow/Playwright build libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    redis-server \
    supervisor \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces runs with user ID 1000
RUN useradd -m -u 1000 user

# Setup App directory
WORKDIR /app

# Copy dependency definitions first for optimal Docker layer caching
COPY backend/requirements.txt /app/backend/requirements.txt
COPY orchestrator/package*.json /app/orchestrator/

# Install Python backend dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Install Playwright browser dependencies and chromium
RUN playwright install --with-deps chromium || true

# Install Node.js orchestrator dependencies
RUN cd /app/orchestrator && npm install --omit=dev --no-audit

# Copy full application codebase
COPY --chown=user:user . /app

# Ensure directories for SQLite, logs, and supervisor exist with proper permissions
RUN mkdir -p /app/data /tmp/supervisor /var/run/redis && \
    chown -R user:user /app /tmp/supervisor /var/run/redis && \
    chmod +x /app/entrypoint.sh

# Switch to non-root user (Hugging Face default)
USER user

# Set environment variables for Hugging Face
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONPATH=/app/backend \
    PORT=7860 \
    ORCHESTRATOR_PORT=7860 \
    DATABASE_URL=sqlite:////app/data/shopraven.db \
    REDIS_URL=redis://127.0.0.1:6379/0 \
    PYTHON_BACKEND_URL=http://127.0.0.1:8000

# Hugging Face Spaces port
EXPOSE 7860

# Entrypoint script starts redis, backend, celery, and orchestrator via supervisor
ENTRYPOINT ["/app/entrypoint.sh"]
