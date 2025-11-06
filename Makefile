.PHONY: dev backend frontend build run test lint install-backend install-frontend dev-backend dev-frontend

BACKEND_DIR=backend
FRONTEND_DIR=frontend

install-backend:
	pip install -r $(BACKEND_DIR)/requirements.txt

install-frontend:
	cd $(FRONTEND_DIR) && npm install

dev-backend:
	uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd $(FRONTEND_DIR) && npm run dev -- --host

dev:
	@echo "Run backend and frontend dev servers separately"

build:
	docker compose build

run:
	docker compose up --build

test:
	cd $(BACKEND_DIR) && pytest

lint:
	cd $(BACKEND_DIR) && ruff check . && black --check .
	cd $(FRONTEND_DIR) && npm run lint
