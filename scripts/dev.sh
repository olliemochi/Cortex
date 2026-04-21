#!/bin/bash
# Start Cortex development environment

set -e

echo "Starting Cortex development environment..."

# Check if required ports are free
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "ERROR: Port $1 is already in use"
        exit 1
    fi
}

check_port 3000
check_port 8080

# Start backend in background
echo "Starting backend..."
cd backend
python main.py &
BACKEND_PID=$!

# Start frontend in new terminal or same
echo "Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "Cortex is starting..."
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop all services"

wait
