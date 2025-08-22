# config.py
from datetime import datetime

# Mock credentials (in real world, these would be from environment variables or secure storage)
CREDENTIALS = {
    "gmail": {
        "email": "your-email@gmail.com",
        "password": "your-password"
    },
    "outlook": {
        "email": "your-email@outlook.com",
        "password": "your-password"
    }
}

# Provider URLs
URLS = {
    "gmail": "https://mail.google.com",
    "outlook": "https://outlook.live.com"
}

# Default settings
DEFAULT_TIMEOUT = 30000  # 30 seconds