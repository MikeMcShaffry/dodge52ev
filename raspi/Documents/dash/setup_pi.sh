#!/bin/bash
# Setup script for Raspberry Pi

echo "Setting up Dash Game on Raspberry Pi..."

# Create virtual environment
python3 -m venv .
source bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Setup complete! To run the game:"
echo "source bin/activate"
echo "python main.py"
