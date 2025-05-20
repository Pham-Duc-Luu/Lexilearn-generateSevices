import logging.handlers
import os

import logstash

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DIR = "logs"
LOG_FILENAME = "app.logs"
LOG_FILEPATH = os.path.join(LOG_DIR, LOG_FILENAME)

LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "localhost")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", "5000"))

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("generate-server")
logger.setLevel(logging.DEBUG)

if os.getenv("ENV", "prod") == "dev":
    if not logger.hasHandlers():
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILEPATH, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        # Logstash handler
        logstash_handler = logstash.TCPLogstashHandler(
            LOGSTASH_HOST, LOGSTASH_PORT, version=1
        )
        logstash_handler.setLevel(logging.DEBUG)
        logger.addHandler(logstash_handler)

        logger.info(f"Logging to rotating file: {LOG_FILEPATH}")
