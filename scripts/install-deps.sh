#!/bin/bash
# Install Cortex dependencies

set -e

echo "Installing Cortex dependencies..."

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "✓ All dependencies installed"
