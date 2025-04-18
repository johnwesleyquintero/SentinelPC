"""SentinelPC Main Entry Point

This module serves as the main entry point for the SentinelPC application.
It initializes core components, sets up the GUI, and handles application lifecycle.
"""

import sys
import logging
import platform
import tkinter as tk
import argparse

# Conditional import for Windows DPI awareness
try:
    from ctypes import windll
except ImportError:
    windll = None  # Not on Windows or ctypes not available

from src.core.sentinel_core import SentinelCore
from src.gui.sentinel_gui import SentinelGUI
from src.cli.sentinel_cli import SentinelCLI


# --- Logging Configuration ---
def setup_logging(debug=False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("logs/SentinelPC.log"), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.debug("Logging initialized")
    return logger


# --- Platform Specific Enhancements ---
def set_dpi_awareness():
    """Sets DPI awareness on Windows for better scaling."""
    if platform.system() == "Windows" and windll:
        try:
            # Query DPI Awareness (Windows 10 and later)
            # awareness = windll.shcore.GetProcessDpiAwareness(0)
            # Set DPI Awareness (requires Windows 8.1 or later)
            # PROCESS_PER_MONITOR_DPI_AWARE = 2
            windll.shcore.SetProcessDpiAwareness(2)
            logging.info("Process DPI awareness set to Per Monitor DPI Aware.")
        except AttributeError:
            # Fallback for older Windows versions (Vista and later)
            try:
                windll.user32.SetProcessDPIAware()
                logging.info("Process DPI awareness set using SetProcessDPIAware().")
            except AttributeError:
                logging.warning(
                    "Could not set DPI awareness. GUI scaling might be suboptimal on high-DPI displays."
                )
        except Exception as e:
            logging.error(f"Error setting DPI awareness: {e}")


# --- Main Application Logic ---
def main():
    args = parse_args()
    # Setup logging based on debug flag
    logger = setup_logging(args.debug)

    try:
        # Launch GUI mode if specified
        if args.gui:
            logger.info("Starting GUI mode")
            core = SentinelCore()
            app = SentinelGUI(core)
            app.mainloop()
        # Launch CLI mode if specified
        elif args.cli:
            logger.info("Starting CLI mode")
            cli = SentinelCLI()
            cli.run()
        else:
            logger.info("No mode specified, defaulting to GUI")
            core = SentinelCore()
            app = SentinelGUI(core)
            app.mainloop()
    except Exception as e:
        logger.error(f"Critical error occurred: {str(e)}")
        raise


def parse_args():
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="SentinelPC - System Performance Optimization Tool"
    )
    parser.add_argument("--gui", action="store_true", help="Run in GUI mode")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


if __name__ == "__main__":
    main()
