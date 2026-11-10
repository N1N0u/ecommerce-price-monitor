import logging

from config.settings import LOG_FILE, LOG_LEVEL


def setup_logging():

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),

        format=(
            "%(asctime)s - "
            "%(name)s - "
            "%(levelname)s - "
            "%(message)s"
        ),

        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
