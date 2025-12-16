#!/bin/bash
# deploy_to_pi.sh - Deploy from Windows development to Raspberry Pi

# Configuration
PI_USER="pi"
PI_HOST="raspberrypi.local"  # or use IP address like "192.168.1.100"
PI_PATH="/home/pi/Documents/dash"
LOCAL_PATH="."

echo "Deploying Dash Game to Raspberry Pi..."

# Option 1: Git-based deployment (recommended)
if command -v git &> /dev/null; then
    echo "Using Git deployment..."
    
    # Push to repository
    echo "Pushing changes to repository..."
    git add .
    read -p "Enter commit message: " commit_msg
    git commit -m "$commit_msg"
    git push origin main
    
    # Deploy on Pi via SSH
    echo "Pulling changes on Raspberry Pi..."
    ssh $PI_USER@$PI_HOST "cd $PI_PATH && git pull origin main && source bin/activate && pip install -r requirements.txt"
    
    echo "Deployment complete!"
    
    # Optional: Start the game remotely
    read -p "Start the game on Pi? (y/n): " start_game
    if [ "$start_game" = "y" ]; then
        ssh $PI_USER@$PI_HOST "cd $PI_PATH && source bin/activate && python main.py" &
    fi
    
else
    echo "Git not available, falling back to rsync..."
    
    # Option 2: rsync fallback
    rsync -avz --delete \
        --exclude='.git' \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        $LOCAL_PATH/ $PI_USER@$PI_HOST:$PI_PATH/
    
    echo "Rsync deployment complete!"
fi
