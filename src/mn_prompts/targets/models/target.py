import typing as T

from mn_prompts.utils.dataclass import dataclass


@dataclass
class Target:
    name: str
    description: str = ""
    layer_names: T.List[str] = []
