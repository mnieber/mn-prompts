from pathlib import Path

from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir


def get_targets_dir() -> Path:
    prompts_dir = get_prompts_dir()
    if not prompts_dir.is_dir():
        raise PromptsDirNotFoundError(
            f"The prompts dir {prompts_dir} does not exist. mn-prompts must be "
            "installed as an editable install from a clone of the mn-prompts "
            "repository, e.g. with: pip install -e ~/mn-prompts"
        )
    return prompts_dir / "targets"


class PromptsDirNotFoundError(Exception):
    pass
