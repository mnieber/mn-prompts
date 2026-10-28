import logging

from bookie.books.models.book import Book
from bookie.chapters.actions.create_paragraph import create_paragraph
from bookie.chapters.enums import TitleStyles
from bookie.chapters.models.chapter import Chapter
from bookie.utils.dataclass import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CreateChapterForm:
    """Form for creating a chapter."""

    title: str
    nr_of_paragraphs: int
    content_mode: TitleStyles = TitleStyles.NORMAL


def create_chapter(book: Book, create_chapter_form: CreateChapterForm) -> Chapter:
    suffix = "!" if create_chapter_form.content_mode == TitleStyles.EXCLAMATIONS else ""
    chapter = Chapter(title=create_chapter_form.title + suffix)

    # Create the specified number of paragraphs
    for _ in range(create_chapter_form.nr_of_paragraphs):
        paragraph = create_paragraph()
        chapter.paragraphs.append(paragraph)

    return chapter
