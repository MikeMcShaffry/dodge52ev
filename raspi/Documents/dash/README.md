# Dash Game Project

A Python game project designed to run on Raspberry Pi, developed on Windows.

## Setup

### On Raspberry Pi:
```bash
cd /home/pi/Documents/dash
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

### On Windows (for development):
```powershell
cd D:\ProjectsPersonal\dodge52ev\raspi\Documents\dash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project Structure

- `src/` - Main source code
- `assets/` - Game assets (images, sounds, fonts)
- `config/` - Configuration files
- `tests/` - Unit tests
- `requirements.txt` - Python dependencies
- `requirements-dev.txt` - Development dependencies
- `main.py` - Entry point for the game

## Running

### On Raspberry Pi:
```bash
source bin/activate
python main.py
```

### On Windows:
```powershell
venv\Scripts\Activate.ps1
python main.py
```
