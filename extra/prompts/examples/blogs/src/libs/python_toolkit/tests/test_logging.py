import logging

from python_toolkit.logging import get_logger


def test_get_logger_with_name():
    """Test that get_logger returns a logger with the specified name."""
    logger = get_logger("test_logger")
    assert logger.name == "test_logger"
    assert isinstance(logger, logging.Logger)


def test_get_logger_without_name():
    """Test that get_logger returns a logger with the module's name when no name is provided."""
    logger = get_logger()
    assert logger.name == __name__
    assert isinstance(logger, logging.Logger)


def test_logger_can_log():
    """Test that the logger can actually log messages."""
    logger = get_logger("test_logging")

    # This shouldn't raise any exceptions
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
