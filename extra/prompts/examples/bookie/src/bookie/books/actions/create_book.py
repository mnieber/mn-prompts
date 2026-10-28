import logging

import bookie.settings as settings
import lorem
from bookie.books.models.book import Book
from bookie.chapters.actions.create_chapter import CreateChapterForm, create_chapter
from bookie.utils.dataclass import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CreateBookForm:
    title: str
    num_chapters: int


def create_book(
    create_book_form: CreateBookForm,
    paragraphs_per_chapter: int = 5,
) -> Book:
    """
    Raises an exception if the number of chapters exceeds the maximum allowed.
    """
    book = Book(title=create_book_form.title)

    if create_book_form.num_chapters > settings.MAX_CHAPTERS_PER_BOOK:
        raise TooManyChaptersError(
            f"Cannot create book with {create_book_form.num_chapters} chapters. "
            f"Maximum allowed is {settings.MAX_CHAPTERS_PER_BOOK}."
        )

    # Create the specified number of chapters
    for i in range(create_book_form.num_chapters):
        # Prepare the create_chapter_form
        create_chapter_form = CreateChapterForm(
            title=f"Chapter {i+1}: {lorem.sentence()}",
            nr_of_paragraphs=paragraphs_per_chapter,
        )

        # Create the chapter
        chapter = create_chapter(book=book, create_chapter_form=create_chapter_form)
        book.chapters.append(chapter)

    return book


class TooManyChaptersError(Exception):
    pass
