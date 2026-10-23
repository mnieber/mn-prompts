from books_tests.books_test_env import Context, TestEnv

import bookie.settings as settings
from bookie.books.actions.create_book import TooManyChaptersError

TITLE = "The Hobbit"


def create_env(context: Context):
    return Env(context)


def test_book_size(context: Context):
    # Create the test environment
    env = create_env(context)

    # We create a book without choosing the number of chapters and paragraphs.
    #
    # The book should have 3 chapters of 5 paragraphs each.
    if env.step(
        env.run_bookie("create-book", f"--title={TITLE}"),
    ):
        assert "Number of chapters: 3" in env.output_lines()
        assert env.output.count("Paragraphs: 5") == 3

    # We create a book with the maximum number of chapters.
    #
    # The book should be created.
    if env.step(
        env.create_book(
            TITLE,
            num_chapters=settings.MAX_CHAPTERS_PER_BOOK,
            paragraphs_per_chapter=1,
        ),
    ):
        assert len(env.book.chapters) == settings.MAX_CHAPTERS_PER_BOOK

    # We create a book with one chapter more than the maximum.
    #
    # It should raise a TooManyChaptersError.
    if env.step(
        env.create_book_and_catch_error(
            TITLE,
            num_chapters=settings.MAX_CHAPTERS_PER_BOOK + 1,
            paragraphs_per_chapter=1,
        ),
    ):
        assert isinstance(env.error, TooManyChaptersError)
        assert str(env.error) == (
            "Cannot create book with 11 chapters. Maximum allowed is 10."
        )


class Env(TestEnv):
    pass
