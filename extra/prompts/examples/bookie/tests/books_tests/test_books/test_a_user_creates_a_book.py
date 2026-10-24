from books_tests.books_test_env import Context, TestEnv

TITLE = "The Hobbit"


def create_env(context: Context):
    return Env(context)


def test_a_user_creates_a_book(context: Context):
    # Create the test environment
    env = create_env(context)

    # We create the book The Hobbit with 3 chapters of 2 paragraphs each.
    #
    # Bookie should report the title and the number of chapters, followed by the
    # title and the number of paragraphs of each chapter.
    if env.step(
        env.run_bookie(
            "create-book", f"--title={TITLE}", "--chapters=3", "--paragraphs=2"
        ),
    ):
        assert env.exit_code == 0
        assert env.output_lines()[:2] == [
            "Created book: The Hobbit",
            "Number of chapters: 3",
        ]

        # The chapter titles are numbered, and end with a lorem ipsum sentence
        assert [line.split(":")[0] for line in env.chapter_title_lines()] == [
            "  Chapter 1",
            "  Chapter 2",
            "  Chapter 3",
        ]
        assert env.paragraph_count_lines() == ["    Paragraphs: 2"] * 3


class Env(TestEnv):
    # Queries

    def chapter_title_lines(self):
        return [line for line in self.output_lines() if line.startswith("  Chapter")]

    def paragraph_count_lines(self):
        return [line for line in self.output_lines() if "Paragraphs:" in line]
