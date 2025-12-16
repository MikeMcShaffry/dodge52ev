"""
Platform-specific utilities for handling differences between Windows and Raspberry Pi
"""

import platform
import sys
from typing import Optional, Dict, Any

# Platform detection
IS_RASPBERRY_PI = platform.machine() in ["armv7l", "aarch64"]
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Try to import platform-specific modules
GPIO_AVAILABLE = False
MCP3XXX_AVAILABLE = False

if IS_RASPBERRY_PI:
    try:
        import RPi.GPIO as GPIO
        GPIO_AVAILABLE = True
    except ImportError:
        print("Warning: RPi.GPIO not available")
        
    try:
        import board
        import busio
        import digitalio
        from adafruit_mcp3xxx import mcp3008
        from adafruit_mcp3xxx.analog_in import AnalogIn
        MCP3XXX_AVAILABLE = True
    except ImportError:
        print("Warning: Adafruit CircuitPython libraries not available")


class PlatformManager:
    """Manages platform-specific functionality"""
    
    def __init__(self):
        self.gpio_initialized = False
        self.spi = None
        self.mcp = None
        
    def initialize_gpio(self, gpio_config: Optional[Dict[str, Any]] = None):
        """Initialize GPIO if on Raspberry Pi"""
        if not GPIO_AVAILABLE or not IS_RASPBERRY_PI:
            print("GPIO not available or not on Raspberry Pi")
            return False
            
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            if gpio_config:
                # Setup pins based on configuration
                for pin_name, pin_number in gpio_config.get('gpio_pins', {}).items():
                    if 'button' in pin_name:
                        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    elif 'led' in pin_name:
                        GPIO.setup(pin_number, GPIO.OUT)
                        
            self.gpio_initialized = True
            print("GPIO initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing GPIO: {e}")
            return False
            
    def initialize_spi(self, spi_config: Optional[Dict[str, Any]] = None):
        """Initialize SPI devices like MCP3008"""
        if not MCP3XXX_AVAILABLE or not IS_RASPBERRY_PI:
            print("SPI/MCP3XXX not available or not on Raspberry Pi")
            return False
            
        try:
            # Create the SPI bus
            self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            
            # Create the CS (chip select)
            cs = digitalio.DigitalInOut(board.CE0)
            
            # Create the MCP object
            self.mcp = mcp3008.MCP3008(self.spi, cs)
            
            print("SPI/MCP3008 initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing SPI: {e}")
            return False
            
    def read_button(self, pin: int) -> bool:
        """Read button state (returns True when pressed)"""
        if not self.gpio_initialized or not GPIO_AVAILABLE:
            return False
            
        try:
            # Button is pressed when pin reads LOW (due to pull-up resistor)
            return not GPIO.input(pin)
        except Exception as e:
            print(f"Error reading button on pin {pin}: {e}")
            return False
            
    def set_led(self, pin: int, state: bool):
        """Set LED state"""
        if not self.gpio_initialized or not GPIO_AVAILABLE:
            return
            
        try:
            GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
        except Exception as e:
            print(f"Error setting LED on pin {pin}: {e}")
            
    def read_analog(self, channel: int) -> float:
        """Read analog value from MCP3008 (returns 0.0 to 1.0)"""
        if not self.mcp:
            return 0.0
            
        try:
            analog_channel = AnalogIn(self.mcp, getattr(self.mcp, f'P{channel}'))
            return analog_channel.value / 65535.0  # Convert to 0.0-1.0 range
        except Exception as e:
            print(f"Error reading analog channel {channel}: {e}")
            return 0.0
            
    def cleanup(self):
        """Clean up platform resources"""
        if self.gpio_initialized and GPIO_AVAILABLE:
            GPIO.cleanup()
            self.gpio_initialized = False
            print("GPIO cleaned up")
            
        if self.spi:
            self.spi.deinit()
            self.spi = None
            print("SPI cleaned up")


# Global platform manager instance
platform_manager = PlatformManager()
