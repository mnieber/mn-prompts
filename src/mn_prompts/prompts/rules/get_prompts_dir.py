from pathlib import Path

import mn_prompts


def get_prompts_dir() -> Path:
    # This only works for an editable install, where the package source lives in a
    # clone of the mn-prompts repository
    return Path(mn_prompts.__file__).parents[2] / "extra" / "prompts"
