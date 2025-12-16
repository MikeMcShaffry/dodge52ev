#!/usr/bin/env python3
"""
Main entry point for the Dash Game
Supports both Raspberry Pi and Windows development environments
"""

import sys
import platform
import argparse
from src.game import DashGame


def main():
    parser = argparse.ArgumentParser(description="Dash Game")
    parser.add_argument('--dev-check', action='store_true', 
                       help='Run development environment check')
    parser.add_argument('--config', type=str, 
                       help='Path to configuration file')
    args = parser.parse_args()
    
    print(f"Starting Dash Game on {platform.system()}")
    print(f"Python version: {sys.version}")
    
    # Development environment check
    if args.dev_check:
        from src.dev_utils import DevUtils
        print(DevUtils.create_deployment_summary())
        return
    
    try:
        game = DashGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
