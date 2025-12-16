# Development Workflow Guide

## Recommended Development Workflow

### Setup (One-time)

1. **Set up SSH keys for passwordless access:**
   ```powershell
   # On Windows
   ssh-keygen -t rsa -b 4096
   ssh-copy-id pi@raspberrypi.local
   ```

2. **Initialize Git repository:**
   ```powershell
   git init
   git remote add origin https://github.com/MikeMcShaffry/dodge52ev.git
   git add .
   git commit -m "Initial dash game structure"
   git push -u origin main
   ```

### Daily Development Workflow

#### Option 1: Git-Based (Recommended)
```powershell
# 1. Develop on Windows
venv\Scripts\Activate.ps1
python main.py  # Test locally

# 2. Deploy to Pi
.\deploy_to_pi.ps1

# 3. If you made changes on Pi, sync back
.\sync_from_pi.ps1
```

#### Option 2: Direct Rsync (Faster for testing)
```powershell
# Quick deployment without git commits
.\deploy_to_pi.ps1 -UseRsync
```

### Workflow Commands

| Action | Windows Command | Description |
|--------|----------------|-------------|
| Deploy | `.\deploy_to_pi.ps1` | Git-based deployment |
| Quick Deploy | `.\deploy_to_pi.ps1 -UseRsync` | Fast rsync deployment |
| Deploy & Start | `.\deploy_to_pi.ps1 -StartGame` | Deploy and start game |
| Sync Back | `.\sync_from_pi.ps1` | Pull Pi changes to Windows |
| Test Locally | `python main.py` | Test on Windows |

### File Synchronization Strategy

**Always Synced:**
- Source code (`src/`)
- Assets (`assets/`)
- Configuration (`config/`)
- Main scripts (`main.py`, `requirements.txt`)

**Platform-Specific (Not Synced):**
- Virtual environments (`venv/` on Windows, `bin/lib/` on Pi)
- Platform-specific cache files
- Log files

### Best Practices

1. **Commit Often:** Small, frequent commits make debugging easier
2. **Test Locally First:** Always test on Windows before deploying
3. **Use Branches:** Create feature branches for major changes
4. **Document Changes:** Use clear commit messages
5. **Backup:** Regularly push to your Git repository

### Troubleshooting

**SSH Connection Issues:**
```powershell
# Test SSH connection
ssh pi@raspberrypi.local "echo 'Connection successful'"

# If hostname doesn't work, use IP
ssh pi@192.168.1.100
```

**Git Issues:**
```powershell
# Check repository status
git status
git remote -v

# Reset if needed
git reset --hard HEAD
git pull origin main
```

**Permission Issues:**
```bash
# On Raspberry Pi
chmod +x *.sh
```
