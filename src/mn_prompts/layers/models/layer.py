import typing as T

from mn_prompts.utils.dataclass import dataclass


@dataclass
class Layer:
    name: str
    snippet: str
    required_layer_names: T.List[str] = []
