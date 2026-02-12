"""
Logging configuration for NetOpsForge
"""

import sys
import logging
import structlog
from pathlib import Path
from typing import Optional
from .config import Config


def setup_logging(log_level: Optional[str] = None, log_file: Optional[Path] = None):
    """
    Configure structured logging for NetOpsForge

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
    """
    # Ensure logs directory exists
    Config.ensure_directories()

    # Use config defaults if not provided
    log_level = log_level or Config.LOG_LEVEL
    log_file = log_file or Config.LOG_FILE

    # Map log level string to logging constant
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    numeric_level = level_map.get(log_level.upper(), logging.INFO)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=False,
    )

    return structlog.get_logger()


def get_logger(name: str = "netopsforge"):
    """
    Get a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return structlog.get_logger(name)

