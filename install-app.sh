#!/usr/bin/env bash

################################################################################
# Cortex System Installation Script
# 
# Organization: AetherAssembly
# License: MIT
# 
# This script installs Cortex as a system-wide Linux application.
# Requires root (sudo) to install to system directories.
#
# Usage: sudo bash install-app.sh
#
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}✓${NC} $*"
}

log_error() {
    echo -e "${RED}✗${NC} $*"
}

log_section() {
    echo -e "\n${BLUE}→${NC} $*"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Error: This script must be run as root (use: sudo bash install-app.sh)${NC}"
    exit 1
fi

log_section "Cortex System Installation"
echo "Organization: AetherAssembly"
echo "License: MIT"
echo ""

# Configuration
INSTALL_PATH="/opt/cortex"
BIN_PATH="/usr/local/bin"
SHARE_PATH="/usr/local/share/applications"
ICON_PATH="/usr/local/share/icons/hicolor/256x256/apps"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_section "Copying files to $INSTALL_PATH..."
mkdir -p "$INSTALL_PATH"

# Copy entire project
cp -r "$CURRENT_DIR"/{backend,frontend} "$INSTALL_PATH/" 2>/dev/null || true
cp "$CURRENT_DIR"/{package.json,README.md,LICENSE} "$INSTALL_PATH"/ 2>/dev/null || true

if [ -d "$CURRENT_DIR/Cortex-Wiki" ]; then
    cp -r "$CURRENT_DIR/Cortex-Wiki" "$INSTALL_PATH/"
fi

log_info "Files copied to $INSTALL_PATH"

# Install launcher script
log_section "Installing launcher script..."
cp "$CURRENT_DIR/cortex-launcher" "$BIN_PATH/cortex-launcher"
chmod +x "$BIN_PATH/cortex-launcher"
log_info "Launcher installed to $BIN_PATH/cortex-launcher"

# Install shell completions
log_section "Installing shell completions..."
COMPLETION_PATH="$INSTALL_PATH/cli/completions"

# Bash completion
if [ -f "$COMPLETION_PATH/cortex_completion.bash" ]; then
    mkdir -p /etc/bash_completion.d
    cp "$COMPLETION_PATH/cortex_completion.bash" /etc/bash_completion.d/cortex
    chmod 644 /etc/bash_completion.d/cortex
    log_info "Bash completion installed"
fi

# Zsh completion
if [ -f "$COMPLETION_PATH/cortex_completion.zsh" ]; then
    mkdir -p /usr/share/zsh/site-functions
    cp "$COMPLETION_PATH/cortex_completion.zsh" /usr/share/zsh/site-functions/_cortex
    chmod 644 /usr/share/zsh/site-functions/_cortex
    log_info "Zsh completion installed"
fi

# Fish completion
if [ -f "$COMPLETION_PATH/cortex_completion.fish" ]; then
    mkdir -p /usr/share/fish/vendor_completions.d
    cp "$COMPLETION_PATH/cortex_completion.fish" /usr/share/fish/vendor_completions.d/cortex.fish
    chmod 644 /usr/share/fish/vendor_completions.d/cortex.fish
    log_info "Fish completion installed"
fi

# Desktop entry
log_section "Installing desktop entry..."
mkdir -p "$SHARE_PATH"
cp "$CURRENT_DIR/cortex.desktop" "$SHARE_PATH/"
chmod 644 "$SHARE_PATH/cortex.desktop"
log_info "Desktop entry installed to $SHARE_PATH"

# Create and install icon
log_section "Creating and installing application icon..."
mkdir -p "$ICON_PATH"

# Create a simple SVG icon
cat > "$ICON_PATH/cortex.svg" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg version="1.1" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="256" height="256" fill="#1f2937" rx="32"/>
  
  <!-- Outer circle -->
  <circle cx="128" cy="128" r="100" fill="none" stroke="#60a5fa" stroke-width="8"/>
  
  <!-- Inner circles (nodes) -->
  <circle cx="128" cy="50" r="12" fill="#60a5fa"/>
  <circle cx="180" cy="90" r="12" fill="#60a5fa"/>
  <circle cx="200" cy="150" r="12" fill="#60a5fa"/>
  <circle cx="165" cy="195" r="12" fill="#60a5fa"/>
  <circle cx="90" cy="205" r="12" fill="#60a5fa"/>
  <circle cx="35" cy="160" r="12" fill="#60a5fa"/>
  <circle cx="28" cy="95" r="12" fill="#60a5fa"/>
  <circle cx="75" cy="50" r="12" fill="#60a5fa"/>
  <circle cx="128" cy="128" r="14" fill="#60a5fa"/>
  
  <!-- Connecting lines -->
  <line x1="128" y1="50" x2="180" y2="90" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="180" y1="90" x2="200" y2="150" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="200" y1="150" x2="165" y2="195" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="165" y1="195" x2="90" y2="205" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="90" y1="205" x2="35" y2="160" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="35" y1="160" x2="28" y2="95" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="28" y1="95" x2="75" y2="50" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  <line x1="75" y1="50" x2="128" y2="50" stroke="#60a5fa" stroke-width="2" opacity="0.5"/>
  
  <!-- Center glow -->
  <circle cx="128" cy="128" r="20" fill="none" stroke="#93c5fd" stroke-width="1" opacity="0.3"/>
</svg>
EOF

chmod 644 "$ICON_PATH/cortex.svg"
log_info "Icon created at $ICON_PATH/cortex.svg"

# Update desktop database (if available)
if command -v update-desktop-database &> /dev/null; then
    log_section "Updating desktop database..."
    update-desktop-database /usr/local/share/applications/
    log_info "Desktop database updated"
fi

# Update icon cache (if available)
if command -v gtk-update-icon-cache &> /dev/null; then
    log_section "Updating icon cache..."
    gtk-update-icon-cache /usr/local/share/icons/hicolor/ || true
    log_info "Icon cache updated"
fi

# Set permissions
chmod -R 755 "$INSTALL_PATH"

# Create uninstall script
log_section "Creating uninstall script..."
cat > "$BIN_PATH/cortex-uninstall" << 'UNINSTALL'
#!/bin/bash
if [ "$EUID" -ne 0 ]; then 
    echo "Error: This script must be run as root"
    exit 1
fi
echo "Uninstalling Cortex..."
rm -rf /opt/cortex
rm -f /usr/local/bin/cortex-launcher
rm -f /usr/local/bin/cortex-uninstall
rm -f /usr/local/share/applications/cortex.desktop
rm -f /usr/local/share/icons/hicolor/256x256/apps/cortex.svg
rm -f /etc/bash_completion.d/cortex
rm -f /usr/share/zsh/site-functions/_cortex
rm -f /usr/share/fish/vendor_completions.d/cortex.fish
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/local/share/applications/
fi
echo "Cortex has been uninstalled"
UNINSTALL
chmod +x "$BIN_PATH/cortex-uninstall"
log_info "Uninstall script created at $BIN_PATH/cortex-uninstall"

# Summary
log_section "Installation Complete!"
echo ""
echo -e "${GREEN}Cortex has been installed successfully!${NC}"
echo ""
echo "You can now launch Cortex by:"
echo -e "  1. ${YELLOW}Command line:${NC} cortex-launcher"
echo -e "  2. ${YELLOW}Application menu:${NC} Search for 'Cortex' in your application launcher"
echo -e "  3. ${YELLOW}Desktop:${NC} Look for Cortex in your applications"
echo ""
echo "Installation details:"
echo -e "  Application files: ${BLUE}$INSTALL_PATH${NC}"
echo -e "  Launcher script:   ${BLUE}$BIN_PATH/cortex-launcher${NC}"
echo -e "  Desktop file:      ${BLUE}$SHARE_PATH/cortex.desktop${NC}"
echo -e "  Icon:              ${BLUE}$ICON_PATH/cortex.svg${NC}"
echo -e "  Shell completions: ${BLUE}Bash, Zsh, Fish${NC}"
echo ""
echo "Shell Completion:"
echo -e "  After installation, completions should work immediately."
echo -e "  If not, restart your shell or run: ${YELLOW}source /etc/bash_completion.d/cortex${NC}"
echo ""
echo "To uninstall:"
echo -e "  ${YELLOW}sudo cortex-uninstall${NC}"
echo ""
echo "Support: support@aetherassembly.org"
echo "Website: https://cortex.aetherassembly.org"
echo "GitHub:  https://github.com/aetherassembly/Cortex"
echo ""
