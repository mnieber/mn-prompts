from pathlib import Path

from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir


def get_agents_file() -> Path:
    return get_prompts_dir() / "agents_files" / "default.md"
