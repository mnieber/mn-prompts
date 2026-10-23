import typing as T

from bookie_test_env import Context, TestEnv as BookieTestEnv

from bookie.chapters.models import Chapter

__all__ = ["Context", "TestEnv"]


class TestEnv(BookieTestEnv):
    def __post_init__(self):
        self.chapter: T.Optional[Chapter] = None
        self.paragraph: T.Optional[str] = None
