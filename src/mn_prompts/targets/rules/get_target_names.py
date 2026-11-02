import typing as T

from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir


def get_target_names() -> T.List[str]:
    return sorted(
        path.stem
        for path in (get_prompts_dir() / "targets").glob("*.yaml")
        if path.is_file() and not path.name.startswith(".")
    )
