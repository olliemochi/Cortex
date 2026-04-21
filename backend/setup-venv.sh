#!/usr/bin/env bash

##############################################################################
# Cortex Backend Virtual Environment Setup
#
# Purpose: Quick setup of Python virtual environment for Cortex backend only
# Organization: AetherAssembly
# License: MIT
#
# Usage: bash setup-backend-venv.sh
#
##############################################################################

set -e

cd "$(dirname "$0")" || exit 1

# Check if we're in the cortex directory
if [ ! -d "backend" ]; then
    echo "Error: backend/ directory not found"
    echo "Please run this script from the cortex root directory"
    exit 1
fi

VENV_PATH="../.venv"
BACKEND_DIR="backend"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  Cortex Backend Virtual Environment Setup"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Find Python 3
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo -e "${GREEN}✓${NC} Found Python 3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | grep -oP '\d+\.\d+')
    echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

# Check if venv already exists
if [ -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}!${NC} Virtual environment already exists"
    read -p "   Use existing environment? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Create virtual environment
    echo -e "${BLUE}→${NC} Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_PATH"
    echo -e "${GREEN}✓${NC} Virtual environment created at $VENV_PATH"
fi

# Activate
source "$VENV_PATH/bin/activate"
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Upgrade pip
echo -e "${BLUE}→${NC} Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Upgraded"

# Enter backend directory
cd "$BACKEND_DIR"

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}→${NC} Installing backend dependencies..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Backend dependencies installed"
else
    echo -e "${YELLOW}!${NC} requirements.txt not found in $BACKEND_DIR/"
fi

# Check for dev requirements
if [ -f "requirements-dev.txt" ]; then
    read -p "Install development dependencies? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}→${NC} Installing development dependencies..."
        pip install -r requirements-dev.txt > /dev/null 2>&1
        echo -e "${GREEN}✓${NC} Dev dependencies installed"
    fi
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    cat > ".env.local" << 'EOF'
# Cortex Backend - Local Development Configuration
# Copy from .env.example and customize as needed

# Python
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Debug
DEBUG=True
LOG_LEVEL=DEBUG

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database (PostgreSQL)
# Adjust credentials as needed
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_dev

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Add other configuration as needed from .env.example
EOF
    echo -e "${GREEN}✓${NC} Created .env.local"
else
    echo -e "${BLUE}ℹ${NC} .env.local already exists"
fi

cd ..

echo ""
echo -e "${GREEN}✓${NC} Backend environment setup complete!"
echo ""
echo "Quick start:"
echo -e "  1. Activate: ${BLUE}source $VENV_PATH/bin/activate${NC}"
echo -e "  2. Enter backend: ${BLUE}cd backend${NC}"
echo -e "  3. Run: ${BLUE}uvicorn main:app --reload${NC}"
echo ""
echo "Backend will be available at: ${BLUE}http://localhost:8000${NC}"
echo "API Documentation: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
