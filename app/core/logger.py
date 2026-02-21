import logging
import sys

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logger = logging.getLogger("audio_analytics")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Avoid duplicate handlers
if not logger.hasHandlers():
    logger.addHandler(stream_handler)
else:
    logger.handlers.clear()
    logger.addHandler(stream_handler)

