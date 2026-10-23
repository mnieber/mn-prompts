from dataclassy import dataclass
from typing import List


@dataclass
class Chapter:
    title: str
    paragraphs: List[str] = []
