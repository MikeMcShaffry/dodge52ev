"""
Test cases for the dash game
"""

import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import GameConfig
from platform_utils import PlatformManager, IS_RASPBERRY_PI, IS_WINDOWS


class TestGameConfig(unittest.TestCase):
    """Test game configuration"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = GameConfig()
        
        self.assertEqual(config.get('display.width'), 800)
        self.assertEqual(config.get('display.height'), 480)
        self.assertEqual(config.get('display.fps'), 60)
        self.assertFalse(config.get('display.fullscreen'))
        
    def test_config_get_with_default(self):
        """Test getting config with default value"""
        config = GameConfig()
        
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')
        self.assertIsNone(config.get('nonexistent.key'))


class TestPlatformUtils(unittest.TestCase):
    """Test platform utilities"""
    
    def test_platform_detection(self):
        """Test platform detection"""
        self.assertIsInstance(IS_RASPBERRY_PI, bool)
        self.assertIsInstance(IS_WINDOWS, bool)
        
    def test_platform_manager_creation(self):
        """Test platform manager can be created"""
        pm = PlatformManager()
        self.assertFalse(pm.gpio_initialized)
        self.assertIsNone(pm.spi)
        self.assertIsNone(pm.mcp)


if __name__ == '__main__':
    unittest.main()
