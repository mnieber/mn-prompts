import typing as T

from mn_prompts.prompts.rules.get_targets_dir import get_targets_dir


def get_target_names() -> T.List[str]:
    return sorted(
        path.name
        for path in get_targets_dir().iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
