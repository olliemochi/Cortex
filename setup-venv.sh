#!/usr/bin/env bash

##############################################################################
# Cortex Python Virtual Environment Setup
#
# Purpose: Quick setup of Python virtual environment for Cortex
# Organization: AetherAssembly  
# License: MIT
#
# Usage: bash setup-venv.sh [VENV_PATH]
# Default VENV_PATH: .venv
#
##############################################################################

set -e

VENV_PATH="${1:-.venv}"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Cortex Virtual Environment Setup${NC}\n"

# Find Python 3
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo -e "${GREEN}✓${NC} Found Python 3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+')
    echo -e "${GREEN}✓${NC} Found Python $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

# Check if venv already exists
if [ -d "$VENV_PATH" ]; then
    echo -e "${BLUE}ℹ${NC} Virtual environment already exists at $VENV_PATH"
    read -p "Activate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        source "$VENV_PATH/bin/activate"
        echo -e "${GREEN}✓${NC} Environment activated"
        exit 0
    else
        exit 0
    fi
fi

# Create virtual environment
echo -e "${BLUE}→${NC} Creating virtual environment at $VENV_PATH..."
$PYTHON_CMD -m venv "$VENV_PATH"
echo -e "${GREEN}✓${NC} Virtual environment created"

# Activate
source "$VENV_PATH/bin/activate"
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Upgrade pip
echo -e "${BLUE}→${NC} Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip upgraded"

# Install backend dependencies if in backend directory
if [ -f "requirements.txt" ]; then
    echo -e "${BLUE}→${NC} Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
fi

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo "To activate this environment in the future:"
echo -e "  ${BLUE}source $VENV_PATH/bin/activate${NC}"
echo ""
echo "To deactivate:"
echo -e "  ${BLUE}deactivate${NC}"
echo ""
