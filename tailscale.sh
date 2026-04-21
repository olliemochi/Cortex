#!/bin/bash
# Tailscale setup for Cortex - PLACEHOLDER
# To be implemented in Phase 6

echo "Setting up Tailscale for Cortex..."

# Check if tailscale is installed
if ! command -v tailscale &> /dev/null; then
    echo "ERROR: Tailscale is not installed. See https://tailscale.com/download"
    exit 1
fi

# Check if tailscale is running
if ! tailscale status &> /dev/null; then
    echo "Starting Tailscale..."
    sudo tailscaled &
    sleep 2
fi

# Authenticate with Tailscale
if ! tailscale status | grep -q "logged in"; then
    echo "Authenticating with Tailscale..."
    sudo tailscale login
fi

# Get hostname
HOSTNAME=$(tailscale status --json | grep '"DNSName"' | head -1 | cut -d'"' -f4)

echo "Tailscale authenticated: $HOSTNAME"
echo ""
echo "To expose Cortex via Tailscale Serve:"
echo "  tailscale serve --bg https / http://localhost:8080"
echo ""
echo "Your Cortex URL will be: https://$HOSTNAME"
