import logging

from config.settings import APP_NAME, APP_ENV
from config.logging_config import setup_logging


def main():

    setup_logging()

    logger = logging.getLogger(__name__)

    logger.info("=" * 50)
    logger.info("%s starting...", APP_NAME)
    logger.info("Environment: %s", APP_ENV)
    logger.info("Application initialized successfully")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
