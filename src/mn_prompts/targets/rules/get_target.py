import yaml

from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir
from mn_prompts.targets.models import Target
from mn_prompts.targets.rules.get_target_names import get_target_names


def get_target(target_name: str) -> Target:
    target_names = get_target_names()
    if target_name not in target_names:
        raise UnknownTargetError(
            f"The target {target_name} does not exist. The available targets are:\n"
            + "\n".join(f"  {name}" for name in target_names)
        )

    target_file = get_prompts_dir() / "targets" / f"{target_name}.yaml"
    data = yaml.safe_load(target_file.read_text()) or {}
    return Target(
        name=target_name,
        description=data.get("description") or "",
        layer_names=data.get("layers") or [],
    )


class UnknownTargetError(Exception):
    pass
