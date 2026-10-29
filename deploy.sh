#!/bin/bash
# ==============================================================================
# ShopRaven AI Co-Founder — 1-Command AWS EC2 Automated Deployment Script
# Target Store: https://nnstore.shop
# ==============================================================================
set -e

echo "=========================================================="
echo "🦅 ShopRaven AI Co-Founder — Deploying on AWS EC2"
echo "=========================================================="

# 1. Determine sudo requirements for Docker
SUDO_PREFIX=""
if [ "$EUID" -ne 0 ]; then
    if ! docker info &> /dev/null 2>&1; then
        SUDO_PREFIX="sudo "
    fi
fi

# 2. Detect and Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "📦 Docker not found. Installing official Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker "$USER" || true
    rm -f get-docker.sh
    echo "✅ Docker installed successfully."
fi

# 3. Check for docker compose or docker-compose
DOCKER_COMPOSE_CMD=""
if docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="${SUDO_PREFIX}docker compose"
elif sudo docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="sudo docker compose"
elif command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="${SUDO_PREFIX}docker-compose"
else
    echo "📦 Installing Docker Compose plugin..."
    sudo apt-get update && sudo apt-get install -y docker-compose-plugin docker-compose || true
    DOCKER_COMPOSE_CMD="sudo docker compose"
fi

# 4. Verify .env file exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "⚠️  No .env file found. Creating from .env.example..."
        cp .env.example .env
        echo "⚠️  ACTION REQUIRED: Edit your credentials in .env (e.g. nano .env)"
        echo "   Then re-run: ./deploy.sh"
        exit 1
    else
        echo "❌ Error: Neither .env nor .env.example found."
        exit 1
    fi
fi

# 5. Clean up dangling cache to reclaim disk space on small instances
echo "🧹 Reclaiming disk space from previous build caches..."
${SUDO_PREFIX}docker builder prune -af || true
${SUDO_PREFIX}docker system prune -f || true

# 6. Stop existing containers & rebuild with latest lightweight images
echo "🚀 Building and starting ShopRaven containers..."
$DOCKER_COMPOSE_CMD down || true
$DOCKER_COMPOSE_CMD up -d --build

# 7. Fetch Public IP
PUBLIC_IP=$(curl -s -m 5 https://ifconfig.me || curl -s -m 5 https://api.ipify.org || echo "YOUR-SERVER-IP")

echo ""
echo "=========================================================="
echo "🎉 ShopRaven is LIVE and running 24/7 on AWS EC2!"
echo "=========================================================="
echo "📊 Control Room Dashboard:  http://${PUBLIC_IP}"
echo "                          http://${PUBLIC_IP}:4000"
echo "🏥 Health Endpoint:         http://${PUBLIC_IP}/health"
echo "📱 WhatsApp Webhook URL:    http://${PUBLIC_IP}/api/whatsapp/webhook"
echo ""
echo "👉 Next Step: Paste the WhatsApp Webhook URL into Wasender"
echo "👉 Test Command: Send 'STATUS' from WhatsApp (+923114618934)"
echo "=========================================================="
