# config.py
from datetime import datetime

# Mock credentials (in real world, these would be from environment variables or secure storage)
CREDENTIALS = {
    "gmail": {
        "email": "testemail@gmail.com",
        "password": "Chan@2024"
    },
    "outlook": {
        "email": "testemail@gmail.com",
        "password": "Chan@2024"
    }
}

# Provider URLs
URLS = {
    "gmail": "https://mail.google.com",
    "outlook": "https://outlook.live.com"
}

# Default settings
DEFAULT_TIMEOUT = 30000  # 30 seconds


# Test with headless mode first (no browser UI)

# Test with visible browser