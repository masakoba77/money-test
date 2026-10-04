#!/bin/bash

set -e

echo "================================"
echo "Stock Trading Simulator Server"
echo "================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

echo "✅ Dependencies installed"
echo ""

echo "🚀 Starting server on http://0.0.0.0:8000"
echo "📱 Access from this machine: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
