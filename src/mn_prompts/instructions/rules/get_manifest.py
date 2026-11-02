import typing as T
from pathlib import Path

import yaml

from mn_prompts.instructions.models import Manifest

MANIFEST_FILE_NAME = "mn-prompts.yaml"


def get_manifest(instructions_dir: Path) -> T.Optional[Manifest]:
    manifest_file = instructions_dir / MANIFEST_FILE_NAME
    if not manifest_file.is_file():
        return None
    data = yaml.safe_load(manifest_file.read_text()) or {}
    return Manifest(
        target_name=data.get("target"),
        layer_names=data.get("layers") or [],
        agents_file_name=data.get("agents_file") or Manifest.agents_file_name,
    )
