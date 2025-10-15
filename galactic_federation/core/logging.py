from __future__ import annotations
import logging
from pythonjsonlogger import jsonlogger

_DEF_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'


def configure_logging(level: int = logging.INFO) -> None:
    """Configure JSON logging for the application.

    Parameters:
        level:
            Logging level (e.g., logging.INFO).
    """
    handler = logging.StreamHandler()
    fmt = jsonlogger.JsonFormatter(_DEF_FORMAT)
    handler.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)
