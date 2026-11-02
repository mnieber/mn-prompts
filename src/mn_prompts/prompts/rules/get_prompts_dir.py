from pathlib import Path

import mn_prompts


def get_prompts_dir() -> Path:
    # This only works for an editable install, where the package source lives in a
    # clone of the mn-prompts repository
    prompts_dir = Path(mn_prompts.__file__).parents[2] / "extra" / "prompts"
    if not prompts_dir.is_dir():
        raise PromptsDirNotFoundError(
            f"The prompts dir {prompts_dir} does not exist. mn-prompts must be "
            "installed as an editable install from a clone of the mn-prompts "
            "repository, e.g. with: pip install -e ~/mn-prompts"
        )
    return prompts_dir


class PromptsDirNotFoundError(Exception):
    pass
