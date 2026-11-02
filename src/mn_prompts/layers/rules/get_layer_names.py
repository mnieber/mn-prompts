import typing as T

from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir


def get_layer_names() -> T.List[str]:
    return sorted(
        path.name
        for path in (get_prompts_dir() / "layers").iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
