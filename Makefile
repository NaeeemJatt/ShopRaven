.PHONY: help setup dev migrate scan-now test test-backend test-orchestrator clean

help:
	@echo "ShopRaven Automation & Deployment Commands:"
	@echo "  make setup        - Install backend and orchestrator dependencies"
	@echo "  make dev          - Start all containers via docker-compose"
	@echo "  make migrate      - Run Alembic database migrations"
	@echo "  make scan-now     - Trigger manual Pakistani market research scan"
	@echo "  make test         - Run full pytest and Jest test suites"
	@echo "  make clean        - Remove temporary cache and test artifacts"

setup:
	@echo "Setting up Python virtualenv and installing dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing Node.js orchestrator dependencies..."
	cd orchestrator && npm install

dev:
	@echo "Starting ShopRaven stack with Docker Compose..."
	docker compose up -d --build

stop:
	@echo "Stopping ShopRaven stack..."
	docker compose down

migrate:
	@echo "Running Alembic migrations on backend..."
	cd backend && alembic upgrade head

scan-now:
	@echo "Triggering immediate market research scan..."
	curl -X POST http://localhost:8000/api/v1/research/scan

test: test-backend test-orchestrator

test-backend:
	@echo "Running Python pytest test suite..."
	cd backend && pytest -v tests/

test-orchestrator:
	@echo "Running Node.js Jest test suite..."
	cd orchestrator && npm test

clean:
	@echo "Cleaning up build artifacts and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
