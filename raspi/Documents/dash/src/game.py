"""
Main Game Class
"""

import pygame
import platform
import sys
from typing import Optional

try:
    # Raspberry Pi specific imports
    if platform.machine() in ["armv7l", "aarch64"]:
        import RPi.GPIO as GPIO
        GPIO_AVAILABLE = True
    else:
        GPIO_AVAILABLE = False
except ImportError:
    GPIO_AVAILABLE = False


class DashGame:
    """Main game class for the Dash Game"""
    
    def __init__(self, width: int = 800, height: int = 480):
        """
        Initialize the game
        
        Args:
            width: Screen width (default 800 for development, 800 for Pi touchscreen)
            height: Screen height (default 480 for Pi touchscreen)
        """
        self.width = width
        self.height = height
        self.running = False
        self.clock: Optional[pygame.time.Clock] = None
        self.screen: Optional[pygame.Surface] = None
        
        # Platform detection
        self.is_raspberry_pi = platform.machine() in ["armv7l", "aarch64"]
        print(f"Running on Raspberry Pi: {self.is_raspberry_pi}")
        print(f"GPIO Available: {GPIO_AVAILABLE}")
        
    def initialize_pygame(self):
        """Initialize pygame"""
        pygame.init()
        
        if self.is_raspberry_pi:
            # Raspberry Pi specific display setup
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            # Windows development setup
            self.screen = pygame.display.set_mode((self.width, self.height))
            
        pygame.display.set_caption("Dash Game")
        self.clock = pygame.time.Clock()
        
    def initialize_gpio(self):
        """Initialize GPIO pins if on Raspberry Pi"""
        if GPIO_AVAILABLE and self.is_raspberry_pi:
            GPIO.setmode(GPIO.BCM)
            # Add your GPIO pin setups here
            print("GPIO initialized")
        
    def cleanup_gpio(self):
        """Clean up GPIO on exit"""
        if GPIO_AVAILABLE and self.is_raspberry_pi:
            GPIO.cleanup()
            print("GPIO cleaned up")
            
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def update(self):
        """Update game logic"""
        pass
        
    def draw(self):
        """Draw the game"""
        if self.screen:
            # Clear screen
            self.screen.fill((0, 0, 0))
            
            # Draw game elements here
            font = pygame.font.Font(None, 36)
            text = font.render("Dash Game Running!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)
            
            # Platform info
            platform_text = font.render(f"Platform: {platform.system()}", True, (255, 255, 255))
            self.screen.blit(platform_text, (10, 10))
            
            pygame.display.flip()
            
    def run(self):
        """Main game loop"""
        print("Initializing game...")
        
        try:
            self.initialize_pygame()
            self.initialize_gpio()
            
            self.running = True
            print("Game loop starting...")
            
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                
                if self.clock:
                    self.clock.tick(60)  # 60 FPS
                    
        except Exception as e:
            print(f"Error in game loop: {e}")
            raise
        finally:
            self.cleanup_gpio()
            pygame.quit()
            print("Game shut down cleanly")
