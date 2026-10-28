from typing import List

from bookie.utils.dataclass import dataclass


@dataclass
class Chapter:
    title: str
    paragraphs: List[str] = []
