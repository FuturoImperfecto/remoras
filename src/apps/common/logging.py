"""Logging utilities."""

import logging
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance."""
    return logging.getLogger(name)


class StructuredLogger:
    """Logger with structured data support."""

    def __init__(self, name: str):
        self.logger = get_logger(name)

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        """Log with structured data."""
        extra = {"data": kwargs}
        getattr(self.logger, level)(message, extra=extra)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info level."""
        self.log("info", message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning level."""
        self.log("warning", message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error level."""
        self.log("error", message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug level."""
        self.log("debug", message, **kwargs)
