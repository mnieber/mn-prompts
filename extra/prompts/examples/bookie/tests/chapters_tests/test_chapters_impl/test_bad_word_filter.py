from chapters_tests.chapters_test_env import Context, TestEnv

import lorem

from bookie.chapters.actions.create_paragraph import create_paragraph

# A bad word contains an "a" or a "b". There are 5 of them: amet, magna, aliqua,
# labore and abest.
TEXT_WITH_5_BAD_WORDS = (
    "Lorem ipsum amet dolor sit magna aliqua elit sed labore tempor dolore abest"
)
TEXT_WITH_6_BAD_WORDS = TEXT_WITH_5_BAD_WORDS + " ullamco"
TEXT_WITHOUT_BAD_WORDS = "Lorem ipsum dolor sit elit sed tempor dolore"

# The "aaa" prefix is ignored, so there is only 1 bad word: aaamagna
TEXT_WITH_PREFIXED_WORDS = (
    "Aaaipsum aaadolor aaasit aaaelit aaased aaatempor aaadolore aaamagna"
)


def create_env(context: Context):
    return Env(context)


def test_bad_word_filter(context: Context):
    # Create the test environment
    env = create_env(context)

    # We create a paragraph with 5 bad words.
    #
    # This is the maximum, so the paragraph should be kept as it is.
    if env.step(
        env.use_lorem_paragraph(TEXT_WITH_5_BAD_WORDS),
        env.create_paragraph(),
    ):
        assert env.paragraph == TEXT_WITH_5_BAD_WORDS

    # We create a paragraph with 6 bad words.
    #
    # The bad words should be removed from the paragraph.
    if env.step(
        env.use_lorem_paragraph(TEXT_WITH_6_BAD_WORDS),
        env.create_paragraph(),
    ):
        assert env.paragraph == TEXT_WITHOUT_BAD_WORDS

    # We create a paragraph in which most words start with "aaa".
    #
    # The paragraph should be kept as it is.
    if env.step(
        env.use_lorem_paragraph(TEXT_WITH_PREFIXED_WORDS),
        env.create_paragraph(),
    ):
        assert env.paragraph == TEXT_WITH_PREFIXED_WORDS


class Env(TestEnv):
    def use_lorem_paragraph(self, text: str):
        """Makes lorem.paragraph() return the given text."""
        self.context.monkeypatch.setattr(lorem, "paragraph", lambda: text)

    def create_paragraph(self):
        self.paragraph = create_paragraph()
