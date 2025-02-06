#!/bin/bash
export PYTHONWARNINGS=ignore::SyntaxWarning:DrissionPage

echo "Creating virtual environment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment!"
        exit 1
    fi
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run build script
echo "Starting build process..."
python build.py

# Complete
echo "Build completed!"