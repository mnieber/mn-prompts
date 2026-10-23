import logging
import os

log_level = os.getenv("LOG_LEVEL", "WARNING")
logging.basicConfig(level=logging.getLevelName(log_level))


def get_logger(name=None):
    if name is None:
        # Get the calling module's name automatically
        import inspect

        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "unknown")

    return logging.getLogger(name)
