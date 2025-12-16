# sync_from_pi.ps1 - Pull changes from Raspberry Pi back to Windows

param(
    [string]$PiHost = "raspberrypi.local",
    [string]$PiUser = "pi",
    [string]$PiPath = "/home/pi/Documents/dash"
)

Write-Host "Syncing changes from Raspberry Pi to Windows..." -ForegroundColor Green

# Check if we have Git
$gitAvailable = Get-Command git -ErrorAction SilentlyContinue

if ($gitAvailable) {
    Write-Host "Using Git to sync..." -ForegroundColor Yellow
    
    # First, tell Pi to commit and push any changes
    Write-Host "Committing any changes on Pi..."
    $commitCommand = @"
cd $PiPath
if [ -n "`$(git status --porcelain)" ]; then
    git add .
    git commit -m "Pi changes - `$(date)"
    git push origin main
else
    echo "No changes to commit on Pi"
fi
"@
    
    ssh "$PiUser@$PiHost" $commitCommand
    
    # Pull changes to Windows
    Write-Host "Pulling changes to Windows..."
    git pull origin main
    
    Write-Host "Git sync complete!" -ForegroundColor Green
}
else {
    Write-Host "Git not available. Install Git for Windows." -ForegroundColor Red
    exit 1
}

Write-Host "Sync finished!" -ForegroundColor Green
