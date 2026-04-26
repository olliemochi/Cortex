.PHONY: help install install-dev install-backend install-frontend install-python dev venv build clean docker-build docker-up docker-down lint format install-app launch uninstall-app

help:
	@echo "Cortex AI Agent Platform - AetherAssembly"
	@echo ""
	@echo "Installation targets:"
	@echo "  install              Full installation (system deps + backend + frontend)"
	@echo "  install-dev          Full installation with development dependencies"
	@echo "  install-backend      Backend only"
	@echo "  install-frontend     Frontend only"
	@echo "  install-python       Skip system dependencies (Python only)"
	@echo ""
	@echo "Desktop Application targets:"
	@echo "  install-app          Install Cortex as a system desktop application"
	@echo "  launch               Launch Cortex desktop application"
	@echo "  uninstall-app        Uninstall system desktop application"
	@echo ""
	@echo "Development targets:"
	@echo "  dev                  Start development servers (frontend + backend)"
	@echo "  venv                 Setup Python virtual environment"
	@echo "  build                Build production bundle"
	@echo "  clean                Clean build artifacts"
	@echo ""
	@echo "Docker targets:"
	@echo "  docker-build         Build Docker images"
	@echo "  docker-up            Start containers with docker-compose"
	@echo "  docker-down          Stop containers"
	@echo ""
	@echo "Code quality targets:"
	@echo "  lint                 Run linters"
	@echo "  format               Format code"
	@echo ""
	@echo "Website: https://cortex.aetherassembly.org"
	@echo "GitHub: https://github.com/aetherassembly/Cortex"
	@echo "Support: support@aetherassembly.org"

install:
	@echo "Running full installation..."
	bash install.sh

install-dev:
	@echo "Running installation with development dependencies..."
	bash install.sh --dev

install-backend:
	@echo "Installing backend only..."
	bash install.sh --backend-only

install-frontend:
	@echo "Installing frontend only..."
	bash install.sh --frontend-only

install-python:
	@echo "Installing Python dependencies only (skipping system packages)..."
	bash install.sh --python-only

venv:
	@echo "Setting up Python virtual environment..."
	bash setup-venv.sh

install-app:
	@echo "Installing Cortex as a system desktop application..."
	@echo "This requires root (sudo) access..."
	sudo bash install-app.sh

launch:
	@echo "Launching Cortex..."
	cortex-launcher

uninstall-app:
	@echo "Uninstalling Cortex desktop application..."
	sudo cortex-uninstall

dev:
	@echo "Starting development servers..."
	bash run-dev.sh

build:
	@echo "Building for production..."
	cd frontend && npm run build
	cd backend && pip install -r requirements.txt

clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/build frontend/dist frontend/.svelte-kit
	rm -rf backend/__pycache__ backend/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting containers..."
	docker-compose up -d
	@echo "Cortex is running at http://localhost:8000 (API) and http://localhost:5173 (Frontend)"

docker-down:
	@echo "Stopping containers..."
	docker-compose down

lint:
	@echo "Running linters..."
	cd frontend && npm run lint || true
	cd backend && pylint . --ignore=.venv,migrations || true

format:
	@echo "Formatting code..."
	cd frontend && npm run format || true
	cd backend && ruff format . --exclude venv || true

.DEFAULT_GOAL := help
