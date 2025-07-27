# src/utils/logger.py

import logging
import sys
import json
from pathlib import Path

# Define a custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)

# Configure the logger

def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a logger with a specified name.
    Adds both console and file handlers (info and error logs).
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = JsonFormatter()

        # Console handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File handler for all logs
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # File handler for errors only
        error_file_handler = logging.FileHandler("error.log", encoding="utf-8")
        error_file_handler.setFormatter(formatter)
        error_file_handler.setLevel(logging.ERROR)
        logger.addHandler(error_file_handler)

    return logger

# Example of a generic logger instance you can import elsewhere
log = get_logger(__name__)