import typing as T

from bookie_test_env import Context, TestEnv as BookieTestEnv

from bookie.books.actions.create_book import CreateBookForm, create_book
from bookie.books.models import Book

__all__ = ["Context", "TestEnv"]


class TestEnv(BookieTestEnv):
    def __post_init__(self):
        self.book: T.Optional[Book] = None

    def create_book(self, title: str, num_chapters: int, paragraphs_per_chapter: int):
        self.book = create_book(
            CreateBookForm(title=title, num_chapters=num_chapters),
            paragraphs_per_chapter=paragraphs_per_chapter,
        )

    def create_book_and_catch_error(self, *args, **kwargs):
        try:
            self.create_book(*args, **kwargs)
        except Exception as error:
            self.error = error

    # Queries

    def output_lines(self) -> T.List[str]:
        return self.output.splitlines()
