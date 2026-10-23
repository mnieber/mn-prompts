import logging

from bookie.chapters.utils.strip_prefix import strip_prefix

logger = logging.getLogger(__name__)


def is_bad_word(word: str) -> bool:
    """
    Determine if a word is a bad word.

    A bad word is defined as any word that - after stripping the prefix of "aaa" -
    contains the letter 'a' or 'b'.
    """
    stripped_word = strip_prefix(word.lower(), "aaa")
    return "a" in stripped_word or "b" in stripped_word
