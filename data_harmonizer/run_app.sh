#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure we are in the script's directory (project root)
cd "$(dirname "$0")"

echo "=========================================="
echo "🚀 Starting Data Harmonizer Setup"
echo "=========================================="

# 1. Check/Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment (venv)..."
    python3 -m venv venv
else
    echo "✅ Virtual environment found."
fi

# 2. Activate Virtual Environment
source venv/bin/activate
echo "✅ Virtual environment activated."

# 3. Install/Update Dependencies
echo "⬇️  Installing/Updating dependencies from requirements.txt..."
pip install -r requirements.txt | grep -v 'already satisfied' || true

# 4. Clean Streamlit Cache (Optional)
# Removing default cache directory if exists to ensure fresh run
if [ -d "$HOME/.streamlit/cache" ]; then
    echo "🧹 Clearing Streamlit cache..."
    rm -rf "$HOME/.streamlit/cache"
fi

# 5. Run Application
echo "=========================================="
echo "▶️  Launching Data Harmonizer..."
echo "=========================================="
streamlit run app.py
