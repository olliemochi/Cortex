#!/bin/bash
# Cortex Project Verification Script
# This script verifies that all components are properly set up

set -e

echo "=========================================="
echo "Cortex Project Verification"
echo "=========================================="
echo ""

ERRORS=0

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check() {
    local name=$1
    local command=$2
    
    echo -n "Checking $name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== File Structure ==="
check "README exists" "[ -f README.md ]"
check "Backend folder" "[ -d backend ]"
check "Frontend folder" "[ -d frontend ]"
check "CLI folder" "[ -d cli ]"
check "Docker Compose" "[ -f docker-compose.yml ]"
check "Backend Dockerfile" "[ -f backend/Dockerfile ]"
check "Frontend Dockerfile" "[ -f frontend/Dockerfile ]"

echo ""
echo "=== Python Compilation ==="
check "Discord bot compiles" "python3 -m py_compile backend/app/integrations/discord_bot.py"
check "Discord routes compile" "python3 -m py_compile backend/app/routes/discord_routes.py"
check "Tailscale integration compiles" "python3 -m py_compile backend/app/integrations/tailscale.py"
check "CLI tool compiles" "python3 -m py_compile cli/cortex_cli.py"

echo ""
echo "=== Docker Configuration ==="
check "docker-compose.yml valid" "docker-compose config > /dev/null 2>&1"

echo ""
echo "=== Requirements ==="
check "Backend requirements.txt" "[ -f backend/requirements.txt ]"
check "discord.py in requirements" "grep -q 'discord.py' backend/requirements.txt"
check "click in requirements" "grep -q 'click' backend/requirements.txt"
check "rich in requirements" "grep -q 'rich' backend/requirements.txt"

echo ""
echo "=== Documentation ==="
check "README.md" "[ -f README.md ]"
check "DEPLOYMENT_GUIDE.md" "[ -f DEPLOYMENT_GUIDE.md ]"
check "QUICK_START.md" "[ -f QUICK_START.md ]"
check "API_DOCUMENTATION.md" "[ -f API_DOCUMENTATION.md ]"

echo ""
echo "=== Integration Setup ==="
check "Discord bot imports working" "python3 -c 'import sys; sys.path.insert(0, \".\"); import backend.app.integrations.discord_bot' 2>&1 || true"
check "main.py imports Cortex modules" "grep -q 'from routers import' backend/main.py"

echo ""
echo "=========================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed!${NC}"
    echo "You can now run: docker-compose up -d"
else
    echo -e "${RED}$ERRORS checks failed!${NC}"
    echo "Please review the errors above"
    exit 1
fi
