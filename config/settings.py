import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


# Application settings
APP_NAME = os.getenv("APP_NAME", "Ecommerce Price Monitor")

APP_ENV = os.getenv("APP_ENV", "development")

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# Database settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/ecommerce.db"
)


# Scraping settings
SCRAPE_INTERVAL_HOURS = int(
    os.getenv("SCRAPE_INTERVAL_HOURS", "6")
)

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "30")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)


# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOG_FILE = BASE_DIR / os.getenv(
    "LOG_FILE",
    "data/app.log"
)
