from dataclassy import dataclass
import typing as T

if T.TYPE_CHECKING:
    from bookie.chapters.models.chapter import Chapter


@dataclass
class Book:
    title: str
    chapters: T.List["Chapter"] = []
