#!/usr/bin/env bash

##############################################################################
# Cortex Universal Linux Installer
# 
# Purpose: Automated setup for Cortex AI Agent Platform on any Linux distro
# Organization: AetherAssembly
# License: MIT
# 
# Usage: bash install.sh [OPTIONS]
# Options:
#   --help              Show this help message
#   --python-only       Only install Python packages (skip system deps)
#   --backend-only      Only install backend
#   --frontend-only     Only install frontend
#   --dev               Development mode (install dev dependencies)
#   --venv-path PATH    Custom path for virtual environment (default: ./venv)
#
##############################################################################

set -e

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_PATH="${VENV_PATH:-.venv}"
INSTALL_SYSTEM_DEPS=true
INSTALL_BACKEND=true
INSTALL_FRONTEND=true
DEV_MODE=false

# Functions
print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}  $1"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
}

print_info() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help)
            cat << 'EOF'
Cortex Universal Linux Installer

Usage: bash install.sh [OPTIONS]

Options:
  --help              Show this help message
  --python-only       Only install Python packages (skip system deps)
  --backend-only      Only install backend
  --frontend-only     Only install frontend
  --dev               Development mode (install dev dependencies)
  --venv-path PATH    Custom path for virtual environment (default: ./venv)

Examples:
  bash install.sh                    # Full installation
  bash install.sh --python-only      # Skip system dependencies
  bash install.sh --dev              # Development setup
  bash install.sh --venv-path /opt/cortex-env

EOF
            exit 0
            ;;
        --python-only)
            INSTALL_SYSTEM_DEPS=false
            shift
            ;;
        --backend-only)
            INSTALL_FRONTEND=false
            shift
            ;;
        --frontend-only)
            INSTALL_BACKEND=false
            shift
            ;;
        --dev)
            DEV_MODE=true
            shift
            ;;
        --venv-path)
            VENV_PATH="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Run 'bash install.sh --help' for usage information"
            exit 1
            ;;
    esac
done

print_header "Cortex AI Agent Platform - Universal Linux Installer"

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        echo "$DISTRIB_ID" | tr '[:upper:]' '[:lower:]'
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
print_info "Detected Linux distribution: $DISTRO"

# Check if running as root for system package installation
if [[ $INSTALL_SYSTEM_DEPS == true ]]; then
    if [[ $EUID -ne 0 && $DISTRO != "unknown" ]]; then
        print_warning "System package installation requires root. Attempting with sudo..."
        if ! command -v sudo &> /dev/null; then
            print_error "sudo not found. Please run with sudo: sudo bash install.sh"
            exit 1
        fi
    fi
fi

# Install system dependencies
install_system_deps() {
    if [[ $INSTALL_SYSTEM_DEPS == false ]]; then
        print_info "Skipping system dependency installation (--python-only)"
        return 0
    fi

    print_header "Installing System Dependencies"

    case $DISTRO in
        ubuntu|debian)
            print_info "Installing dependencies for Ubuntu/Debian..."
            if command -v sudo &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y \
                    python3.11 python3.11-venv python3-pip \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis-server \
                    git curl wget \
                    build-essential libssl-dev libffi-dev python3-dev
            else
                apt-get update
                apt-get install -y \
                    python3.11 python3.11-venv python3-pip \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis-server \
                    git curl wget \
                    build-essential libssl-dev libffi-dev python3-dev
            fi
            ;;
        fedora|rhel|centos)
            print_info "Installing dependencies for Fedora/RHEL/CentOS..."
            if command -v sudo &> /dev/null; then
                sudo dnf install -y \
                    python3.11 python3.11-devel \
                    postgresql-server postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    gcc openssl-devel libffi-devel
            else
                dnf install -y \
                    python3.11 python3.11-devel \
                    postgresql-server postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    gcc openssl-devel libffi-devel
            fi
            ;;
        arch|manjaro)
            print_info "Installing dependencies for Arch/Manjaro..."
            if command -v sudo &> /dev/null; then
                sudo pacman -S --noconfirm \
                    python python-pip \
                    postgresql \
                    nodejs npm \
                    redis \
                    git curl wget \
                    base-devel
            else
                pacman -S --noconfirm \
                    python python-pip \
                    postgresql \
                    nodejs npm \
                    redis \
                    git curl wget \
                    base-devel
            fi
            ;;
        alpine)
            print_info "Installing dependencies for Alpine..."
            if command -v sudo &> /dev/null; then
                sudo apk add --no-cache \
                    python3 py3-pip python3-dev \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    build-base openssl-dev libffi-dev
            else
                apk add --no-cache \
                    python3 py3-pip python3-dev \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    build-base openssl-dev libffi-dev
            fi
            ;;
        opensuse*|suse)
            print_info "Installing dependencies for openSUSE..."
            if command -v sudo &> /dev/null; then
                sudo zypper install -y \
                    python3.11 python3.11-devel \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    gcc openssl-devel libffi-devel
            else
                zypper install -y \
                    python3.11 python3.11-devel \
                    postgresql postgresql-contrib \
                    nodejs npm \
                    redis \
                    git curl wget \
                    gcc openssl-devel libffi-devel
            fi
            ;;
        *)
            print_warning "Unknown or unsupported distribution: $DISTRO"
            print_warning "Please install the following manually:"
            echo "  - Python 3.11+"
            echo "  - PostgreSQL 13+"
            echo "  - Node.js 18+"
            echo "  - Redis (optional)"
            echo "  - Git"
            ;;
    esac

    print_info "System dependencies installed"
}

# Create virtual environment
create_venv() {
    print_header "Setting Up Python Virtual Environment"

    if [ -d "$VENV_PATH" ]; then
        print_warning "Virtual environment already exists at $VENV_PATH"
        read -p "Recreate it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_PATH"
        else
            print_info "Using existing virtual environment"
            return 0
        fi
    fi

    # Use python3.11 if available, otherwise python3
    PYTHON_CMD="python3"
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.9 or higher."
        exit 1
    fi

    print_info "Creating virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv "$VENV_PATH"
    print_info "Virtual environment created at $VENV_PATH"
}

# Activate virtual environment
activate_venv() {
    if [ -f "$VENV_PATH/bin/activate" ]; then
        source "$VENV_PATH/bin/activate"
        print_info "Virtual environment activated"
    else
        print_error "Virtual environment activation failed"
        exit 1
    fi
}

# Install backend dependencies
install_backend_deps() {
    if [[ $INSTALL_BACKEND == false ]]; then
        print_info "Skipping backend installation (--frontend-only)"
        return 0
    fi

    print_header "Installing Backend Dependencies"

    if [ ! -d "backend" ]; then
        print_error "backend/ directory not found. Are you in the cortex root directory?"
        exit 1
    fi

    cd backend

    if [ -f "requirements.txt" ]; then
        print_info "Installing Python packages from requirements.txt..."
        pip install --upgrade pip setuptools wheel
        pip install -r requirements.txt
        
        if [[ $DEV_MODE == true ]] && [ -f "requirements-dev.txt" ]; then
            print_info "Installing development dependencies..."
            pip install -r requirements-dev.txt
        fi
        
        print_info "Backend dependencies installed"
    else
        print_warning "requirements.txt not found in backend/"
    fi

    cd ..
}

# Install frontend dependencies
install_frontend_deps() {
    if [[ $INSTALL_FRONTEND == false ]]; then
        print_info "Skipping frontend installation (--backend-only)"
        return 0
    fi

    print_header "Installing Frontend Dependencies"

    if [ ! -d "frontend" ]; then
        print_error "frontend/ directory not found. Are you in the cortex root directory?"
        exit 1
    fi

    if ! command -v npm &> /dev/null; then
        print_error "npm not found. Please install Node.js and npm."
        exit 1
    fi

    cd frontend

    if [ -f "package.json" ]; then
        print_info "Installing npm packages..."
        npm install
        
        if [[ $DEV_MODE == true ]]; then
            print_info "Installing development dependencies..."
            npm install --save-dev
        fi
        
        print_info "Frontend dependencies installed"
    else
        print_warning "package.json not found in frontend/"
    fi

    cd ..
}

# Create setup scripts
create_setup_scripts() {
    print_header "Creating Helper Scripts"

    # Activation script
    cat > "activate-cortex.sh" << 'SCRIPT'
#!/bin/bash
# Activate Cortex environment

VENV_PATH=".venv"

if [ ! -f "$VENV_PATH/bin/activate" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Run: bash install.sh"
    exit 1
fi

source "$VENV_PATH/bin/activate"
echo "✓ Cortex environment activated"
echo "  Run 'cortex --help' for CLI commands"
echo "  Backend: http://localhost:8000"
echo "  Frontend: http://localhost:5173"
SCRIPT
    chmod +x activate-cortex.sh
    print_info "Created activate-cortex.sh"

    # Development run script
    cat > "run-dev.sh" << 'SCRIPT'
#!/bin/bash
# Run Cortex in development mode

source .venv/bin/activate 2>/dev/null || true

echo "Starting Cortex in development mode..."
echo ""

# Start backend if requested
if [[ "${1}" != "--frontend-only" ]]; then
    echo "Starting backend (http://localhost:8000)..."
    cd backend
    uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
    cd ..
fi

# Start frontend if requested
if [[ "${1}" != "--backend-only" ]]; then
    echo "Starting frontend (http://localhost:5173)..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
fi

echo ""
echo "Services starting... Press Ctrl+C to stop"
wait
SCRIPT
    chmod +x run-dev.sh
    print_info "Created run-dev.sh"

    # Environment setup script
    cat > ".env.local" << 'SCRIPT'
# Local Development Configuration
# Copy to backend/ and frontend/ .env.local as needed

# Backend
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (development)
DATABASE_URL=postgresql://cortex:cortex@localhost:5432/cortex_dev

# Frontend
VITE_API_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000/ws
SCRIPT
    print_info "Created .env.local"
}

# Print final instructions
print_instructions() {
    print_header "Installation Complete!"
    
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Activate the environment:"
    echo -e "   ${YELLOW}source ./activate-cortex.sh${NC}"
    echo ""
    echo "2. Run in development mode:"
    echo -e "   ${YELLOW}bash ./run-dev.sh${NC}"
    echo ""
    echo "3. Access the application:"
    echo -e "   Backend API: ${BLUE}http://localhost:8000${NC}"
    echo -e "   API Docs:    ${BLUE}http://localhost:8000/docs${NC}"
    echo -e "   Frontend:    ${BLUE}http://localhost:5173${NC}"
    echo ""
    echo "Documentation:"
    echo "  - Quick Start: https://cortex.aetherassembly.org/getting-started/"
    echo "  - GitHub: https://github.com/aetherassembly/Cortex"
    echo "  - Issues: https://github.com/aetherassembly/Cortex/issues"
    echo ""
    echo "Support:"
    echo "  - Email: support@aetherassembly.org"
    echo "  - Contact: contact@aetherassembly.org"
    echo ""
}

# Main execution
main() {
    print_info "User: $(whoami)"
    print_info "Current directory: $(pwd)"
    print_info "Virtual environment path: $VENV_PATH"
    echo ""

    install_system_deps
    create_venv
    activate_venv
    install_backend_deps
    install_frontend_deps
    create_setup_scripts
    print_instructions
}

# Run main
main
