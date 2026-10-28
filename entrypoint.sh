#!/usr/bin/env bash
set -e

# 1. Detect Hugging Face Native Persistent Storage (/data) or fallback to /app/data
if [ -d "/data" ] && [ -w "/data" ]; then
    DATA_DIR="/data"
    echo "💾 [Hugging Face Storage] Native Persistent Storage (/data) detected and active!"
else
    DATA_DIR="/app/data"
    echo "💾 [Hugging Face Storage] Using local container data directory (/app/data)."
fi

mkdir -p "$DATA_DIR" /tmp/supervisor

# 2. If HF_DATASET_BACKUP is specified, auto-restore database from private Hugging Face Dataset (100% Free)
if [ -n "$HF_DATASET_BACKUP" ] && [ -n "$HF_TOKEN" ]; then
    echo "🔄 [Hugging Face Dataset] Checking for remote database backup in: $HF_DATASET_BACKUP..."
    python3 -c "
import os
from huggingface_hub import hf_hub_download
try:
    path = hf_hub_download(
        repo_id='$HF_DATASET_BACKUP',
        filename='shopraven.db',
        repo_type='dataset',
        token='$HF_TOKEN',
        local_dir='$DATA_DIR'
    )
    print(f'✅ [Hugging Face Dataset] Restored database successfully from {path}')
except Exception as e:
    print(f'ℹ️ [Hugging Face Dataset] First run or no remote backup found yet ({e}). Starting fresh database.')
" || true
fi

# 3. Dynamic Database and Orchestrator URL configuration
if [ -z "$DATABASE_URL" ] || [ "$DATABASE_URL" = "sqlite:////app/data/shopraven.db" ]; then
    export DATABASE_URL="sqlite:///${DATA_DIR}/shopraven.db"
fi

export ORCHESTRATOR_URL="http://127.0.0.1:${PORT:-7860}"

echo "=========================================================="
echo "🦅 ShopRaven AI Co-Founder — Launching on Hugging Face Spaces"
echo "Port: ${PORT:-7860} | Database: ${DATABASE_URL}"
echo "Storage Location: ${DATA_DIR} | Orchestrator: ${ORCHESTRATOR_URL}"
echo "=========================================================="

# 4. Launch Supervisord to manage Redis, Python FastAPI, Celery, and Node Orchestrator
exec /usr/bin/supervisord -c /app/supervisord.conf
