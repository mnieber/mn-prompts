import typing as T

from mn_prompts.utils.dataclass import dataclass


@dataclass
class Manifest:
    target_name: T.Optional[str] = None
    layer_names: T.List[str] = []
    agents_file_name: str = "CLAUDE.md"
