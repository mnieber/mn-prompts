from chapters_tests.chapters_test_env import Context, TestEnv

from bookie.books.models import Book
from bookie.chapters.actions.create_chapter import CreateChapterForm, create_chapter
from bookie.chapters.enums import TitleStyles

TITLE = "An Unexpected Party"


def create_env(context: Context):
    return Env(context)


def test_chapter_title_styles(context: Context):
    # Create the test environment
    env = create_env(context)

    # We create a chapter with 2 paragraphs, without choosing a title style.
    #
    # The chapter should have the normal title style, which keeps the title as it is.
    if env.step(
        env.create_chapter(TITLE, nr_of_paragraphs=2),
    ):
        assert env.chapter.title == TITLE
        assert len(env.chapter.paragraphs) == 2

    # We create a chapter with the exclamations title style.
    #
    # The title should end with an exclamation mark.
    if env.step(
        env.create_chapter(
            TITLE, nr_of_paragraphs=2, content_mode=TitleStyles.EXCLAMATIONS
        ),
    ):
        assert env.chapter.title == TITLE + "!"


class Env(TestEnv):
    def create_chapter(self, title: str, nr_of_paragraphs: int, content_mode=None):
        form = CreateChapterForm(title=title, nr_of_paragraphs=nr_of_paragraphs)
        if content_mode:
            form.content_mode = content_mode
        self.chapter = create_chapter(
            book=Book(title="The Hobbit"), create_chapter_form=form
        )
