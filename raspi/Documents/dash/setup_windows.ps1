# Setup script for Windows development

Write-Host "Setting up Dash Game for Windows development..."

# Create virtual environment
python -m venv venv
& "venv\Scripts\Activate.ps1"

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

Write-Host "Setup complete! To run the game:"
Write-Host "venv\Scripts\Activate.ps1"
Write-Host "python main.py"
