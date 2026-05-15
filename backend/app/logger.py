"""Logging configuration"""

import logging
import logging.handlers
import os
from datetime import datetime

# Create logs directory
if not os.path.exists("logs"):
    os.makedirs("logs")

# Setup logger
logger = logging.getLogger("nft_trading_bot")
logger.setLevel(logging.DEBUG)

# File handler with rotation
file_handler = logging.handlers.RotatingFileHandler(
    "logs/app.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger():
    """Get logger instance"""
    return logger
