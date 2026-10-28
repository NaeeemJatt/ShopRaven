#!/usr/bin/env bash
set -e

# Ensure data directory and supervisor directories exist
mkdir -p /app/data /tmp/supervisor

echo "=========================================================="
echo "🦅 ShopRaven AI Co-Founder — Launching on Hugging Face Spaces"
echo "Port: ${PORT:-7860} | Environment: Production"
echo "=========================================================="

# Execute supervisord to manage Redis, Python Backend, Celery Beat, and Node Orchestrator
exec /usr/bin/supervisord -c /app/supervisord.conf
