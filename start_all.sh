#!/bin/bash
echo "Starting Backend..."
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Waiting for services to start..."
sleep 5

echo "Starting Simulation..."
python3 main.py

echo "Simulation finished. Backend and Frontend are still running."
echo "Press [ENTER] to stop the services..."
read

# Cleanup
echo "Stopping services..."
kill $BACKEND_PID
kill $FRONTEND_PID
echo "Done."
