import typing as T

from bookie.utils.dataclass import dataclass

if T.TYPE_CHECKING:
    from bookie.chapters.models.chapter import Chapter


@dataclass
class Book:
    title: str
    chapters: T.List["Chapter"] = []
