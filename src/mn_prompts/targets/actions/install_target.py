import os
from pathlib import Path

from mn_prompts.prompts.rules.get_targets_dir import get_targets_dir
from mn_prompts.targets.rules.get_target_names import get_target_names


def install_target(target_name: str, project_dir: Path):
    targets_dir = get_targets_dir()

    # Check for errors before changing any file
    target_names = get_target_names()
    if target_name not in target_names:
        raise UnknownTargetError(
            f"The target {target_name} does not exist. The available targets are:\n"
            + "\n".join(f"  {name}" for name in target_names)
        )

    instructions = project_dir / "instructions"
    if os.path.lexists(instructions):
        if not _is_symlink_into(instructions, targets_dir):
            raise InstructionsExistError(
                f"{instructions} already exists. Remove it, and try again."
            )
        # The symlink is ours (possibly dangling): replace it
        instructions.unlink()

    instructions.symlink_to((targets_dir / target_name).absolute())


def _is_symlink_into(path: Path, parent_dir: Path) -> bool:
    if not path.is_symlink():
        return False
    link = Path(os.readlink(path))
    if not link.is_absolute():
        link = path.parent / link
    return os.path.normpath(link.parent) == os.path.normpath(parent_dir.absolute())


class UnknownTargetError(Exception):
    pass


class InstructionsExistError(Exception):
    pass
