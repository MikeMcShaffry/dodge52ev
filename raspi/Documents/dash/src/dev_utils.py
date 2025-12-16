"""
Development utilities for cross-platform testing and deployment
"""

import subprocess
import platform
import os
import json
from typing import Dict, List, Optional


class DevUtils:
    """Development utilities for the game project"""
    
    @staticmethod
    def get_git_status() -> Dict[str, any]:
        """Get current git status"""
        try:
            # Check if git is available
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                return {'available': False, 'error': 'Git not found'}
            
            # Get repository info
            branch = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            status = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            return {
                'available': True,
                'branch': branch.stdout.strip(),
                'has_changes': bool(status.stdout.strip()),
                'changes': status.stdout.strip().split('\n') if status.stdout.strip() else []
            }
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    @staticmethod
    def check_dependencies() -> Dict[str, bool]:
        """Check if required dependencies are installed"""
        dependencies = {
            'pygame': False,
            'numpy': False,
            'git': False
        }
        
        # Check Python packages
        for package in ['pygame', 'numpy']:
            try:
                __import__(package)
                dependencies[package] = True
            except ImportError:
                dependencies[package] = False
        
        # Check git
        try:
            result = subprocess.run(['git', '--version'], 
                                  capture_output=True, text=True)
            dependencies['git'] = result.returncode == 0
        except:
            dependencies['git'] = False
            
        return dependencies
    
    @staticmethod
    def get_platform_info() -> Dict[str, str]:
        """Get detailed platform information"""
        return {
            'system': platform.system(),
            'machine': platform.machine(),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'is_raspberry_pi': platform.machine() in ["armv7l", "aarch64"],
            'is_windows': platform.system() == "Windows"
        }
    
    @staticmethod
    def validate_project_structure() -> Dict[str, bool]:
        """Validate that all required project files exist"""
        required_files = [
            'main.py',
            'requirements.txt',
            'src/__init__.py',
            'src/game.py',
            'src/config.py',
            'src/platform_utils.py',
            'config/game_config.json'
        ]
        
        required_dirs = [
            'src',
            'assets',
            'assets/images',
            'assets/sounds',
            'assets/fonts',
            'config',
            'tests'
        ]
        
        structure = {}
        
        for file_path in required_files:
            structure[f"file:{file_path}"] = os.path.exists(file_path)
            
        for dir_path in required_dirs:
            structure[f"dir:{dir_path}"] = os.path.isdir(dir_path)
            
        return structure
    
    @staticmethod
    def create_deployment_summary() -> str:
        """Create a summary for deployment"""
        git_info = DevUtils.get_git_status()
        platform_info = DevUtils.get_platform_info()
        dependencies = DevUtils.check_dependencies()
        structure = DevUtils.validate_project_structure()
        
        summary = f"""
=== DASH GAME DEPLOYMENT SUMMARY ===

Platform Information:
- System: {platform_info['system']}
- Machine: {platform_info['machine']}
- Python: {platform_info['python_version']}
- Is Raspberry Pi: {platform_info['is_raspberry_pi']}

Git Status:
- Available: {git_info.get('available', False)}
- Branch: {git_info.get('branch', 'Unknown')}
- Has Changes: {git_info.get('has_changes', False)}

Dependencies:
- Pygame: {'✓' if dependencies['pygame'] else '✗'}
- NumPy: {'✓' if dependencies['numpy'] else '✗'}
- Git: {'✓' if dependencies['git'] else '✗'}

Project Structure:
"""
        
        # Add structure validation
        for item, exists in structure.items():
            status = '✓' if exists else '✗'
            summary += f"- {item}: {status}\n"
        
        # Add recommendations
        summary += "\nRecommendations:\n"
        
        if not dependencies['git']:
            summary += "- Install Git for version control\n"
        
        if not dependencies['pygame']:
            summary += "- Install pygame: pip install pygame\n"
            
        missing_structure = [k for k, v in structure.items() if not v]
        if missing_structure:
            summary += f"- Fix missing files/directories: {', '.join(missing_structure)}\n"
        
        if git_info.get('has_changes', False):
            summary += "- Commit pending changes before deployment\n"
            
        return summary


if __name__ == "__main__":
    # Run development check
    print(DevUtils.create_deployment_summary())
