#!/bin/bash
# Startup script for FastAPI backend
# This script can be used by deployment platforms

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Start the FastAPI application
# PORT is set by the deployment platform
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-4000}

