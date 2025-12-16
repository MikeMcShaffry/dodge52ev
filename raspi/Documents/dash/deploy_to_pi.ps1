# deploy_to_pi.ps1 - PowerShell deployment script for Windows

param(
    [string]$PiHost = "raspberrypi.local",
    [string]$PiUser = "pi",
    [string]$PiPath = "/home/pi/Documents/dash",
    [switch]$UseRsync = $false,
    [switch]$StartGame = $false
)

Write-Host "Deploying Dash Game to Raspberry Pi..." -ForegroundColor Green

# Check if we have Git
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue

if ($gitAvailable -and -not $UseRsync) {
    Write-Host "Using Git deployment..." -ForegroundColor Yellow
    
    # Check if there are changes to commit
    $status = git status --porcelain
    if ($status) {
        # Add and commit changes
        git add .
        $commitMsg = Read-Host "Enter commit message"
        git commit -m $commitMsg
    }
    
    # Push to repository
    Write-Host "Pushing changes to repository..."
    git push origin main
    
    # Deploy on Pi via SSH (requires SSH key setup or password)
    Write-Host "Pulling changes on Raspberry Pi..."
    $sshCommand = "cd $PiPath && git pull origin main && source bin/activate && pip install -r requirements.txt"
    ssh "$PiUser@$PiHost" $sshCommand
    
    Write-Host "Git deployment complete!" -ForegroundColor Green
    
    if ($StartGame) {
        Write-Host "Starting game on Raspberry Pi..."
        $startCommand = "cd $PiPath && source bin/activate && python main.py"
        ssh "$PiUser@$PiHost" $startCommand
    }
}
elseif (Get-Command rsync -ErrorAction SilentlyContinue) {
    Write-Host "Using rsync deployment..." -ForegroundColor Yellow
    
    # Use rsync for deployment
    $excludes = @(
        "--exclude=.git",
        "--exclude=venv",
        "--exclude=__pycache__",
        "--exclude=*.pyc",
        "--exclude=.pytest_cache"
    )
    
    $source = "./"
    $destination = "$PiUser@$PiHost`:$PiPath/"
    
    & rsync -avz --delete $excludes $source $destination
    
    Write-Host "Rsync deployment complete!" -ForegroundColor Green
}
else {
    Write-Host "Neither Git nor rsync available. Please install one of them." -ForegroundColor Red
    Write-Host "For Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "For rsync: Install WSL or use Cygwin" -ForegroundColor Yellow
    exit 1
}

Write-Host "Deployment finished!" -ForegroundColor Green
