# src/utils/logger.py


import logging
import sys
import json
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

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
    Adds both console and file handlers (info and error logs), rotating daily.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = JsonFormatter()

        # Ensure logs/app and logs/error directories exist
        os.makedirs("logs/app", exist_ok=True)
        os.makedirs("logs/error", exist_ok=True)

        # Console handler
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # Use date-based log file naming for daily log separation
        from datetime import datetime
        today_str = datetime.now().strftime('%Y-%m-%d')
        app_log_path = f"logs/app/app_{today_str}.log"
        error_log_path = f"logs/error/error_{today_str}.log"

        # File handler for all logs (INFO and above)
        file_handler = logging.FileHandler(app_log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # File handler for errors only
        error_file_handler = logging.FileHandler(error_log_path, encoding="utf-8")
        error_file_handler.setFormatter(formatter)
        error_file_handler.setLevel(logging.ERROR)
        logger.addHandler(error_file_handler)

    return logger

# Example of a generic logger instance you can import elsewhere
log = get_logger(__name__)