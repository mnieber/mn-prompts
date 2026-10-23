import logging

logger = logging.getLogger(__name__)


def strip_prefix(text: str, prefix: str) -> str:
    """
    Strip a prefix from the beginning of text if it exists.

    Args:
        text: The text to process
        prefix: The prefix to remove from the beginning of text

    Returns:
        The text with the prefix removed if it was present, otherwise the original text
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
