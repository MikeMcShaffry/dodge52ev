"""
Configuration management for the game
"""

import json
import os
from typing import Dict, Any


class GameConfig:
    """Manages game configuration"""
    
    def __init__(self, config_file: str = "config/game_config.json"):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                print(f"Config file {self.config_file} not found, using defaults")
                self.config = self.get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            self.config = self.get_default_config()
            
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "display": {
                "width": 800,
                "height": 480,
                "fullscreen": False,
                "fps": 60
            },
            "game": {
                "difficulty": "medium",
                "sound_enabled": True,
                "debug_mode": False
            }
        }
        
    def get(self, key: str, default=None):
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def save_config(self):
        """Save current configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")


# Global config instance
config = GameConfig()
