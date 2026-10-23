import logging
import lorem

from bookie import settings
from bookie.chapters.rules.is_bad_word import is_bad_word

logger = logging.getLogger(__name__)


def create_paragraph() -> str:
    """
    Create a paragraph with lorem ipsum text.

    The paragraph is filtered to ensure it contains no more than
    MAX_BAD_WORDS_PER_PARAGRAPH bad words.
    """
    # Generate lorem ipsum text
    paragraph = lorem.paragraph()
    paragraph = _filter_paragraph(paragraph, settings.MAX_BAD_WORDS_PER_PARAGRAPH)

    return paragraph


def _filter_paragraph(paragraph: str, max_bad_words: int) -> str:
    words = paragraph.split()
    bad_word_count = len([word for word in words if is_bad_word(word)])

    if bad_word_count > max_bad_words:
        filtered_words = [word for word in words if not is_bad_word(word)]
        filtered_paragraph = " ".join(filtered_words)
        return filtered_paragraph

    return paragraph
