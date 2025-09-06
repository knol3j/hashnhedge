"""Logging configuration."""
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

def get_logger(name):
    """Get configured logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        handler = RotatingFileHandler(
            log_dir / "image_agent.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
