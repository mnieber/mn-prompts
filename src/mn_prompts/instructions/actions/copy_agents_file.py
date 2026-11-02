import os
import shutil
from pathlib import Path

from mn_prompts.prompts.rules.get_agents_file import get_agents_file


def copy_agents_file(project_dir: Path, agents_file_name: str) -> bool:
    """Returns False (and leaves the file unchanged) if the file already exists."""
    agents_file = project_dir / agents_file_name
    if os.path.lexists(agents_file):
        return False
    shutil.copyfile(get_agents_file(), agents_file)
    return True
