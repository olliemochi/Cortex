#!/bin/bash
# Build Cortex for production

set -e

echo "Building Cortex..."

echo "Building frontend..."
cd frontend
npm run build
cd ..

echo "Building backend..."
cd backend
# Python doesn't need compilation, just install dependencies
pip install -r requirements.txt
cd ..

echo "✓ Build complete"
