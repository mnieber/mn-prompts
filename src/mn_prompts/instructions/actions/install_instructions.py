import os
import typing as T
from pathlib import Path

import yaml

from mn_prompts.instructions.models import Manifest
from mn_prompts.instructions.rules.get_index_text import get_index_text
from mn_prompts.instructions.rules.get_manifest import MANIFEST_FILE_NAME, get_manifest
from mn_prompts.layers.rules.get_selected_layers import get_selected_layers
from mn_prompts.prompts.rules.get_prompts_dir import get_prompts_dir
from mn_prompts.targets.rules.get_target import get_target

AGENTS_MD_FILE_NAME = "AGENTS.md"


def install_instructions(
    project_dir: Path,
    target_name: T.Optional[str] = None,
    layer_names: T.List[str] = [],
    agents_md: bool = False,
) -> Manifest:
    prompts_dir = get_prompts_dir().absolute()
    instructions_dir = project_dir / "instructions"

    # Check for errors before changing any file
    _check_instructions(instructions_dir)
    manifest = _get_requested_manifest(
        instructions_dir, target_name, layer_names, agents_md
    )
    target = get_target(manifest.target_name) if manifest.target_name else None
    layers = get_selected_layers(
        (target.layer_names if target else []) + manifest.layer_names
    )
    index_text = get_index_text(layers)
    _check_links(instructions_dir)

    # Link the selected layers and the examples
    instructions_dir.mkdir(exist_ok=True)

    # Every layer symlink belongs to mn-prompts, so the deselected ones are removed
    for path in instructions_dir.glob("*_layer"):
        path.unlink()
    for layer in layers:
        (instructions_dir / f"{layer.name}_layer").symlink_to(
            prompts_dir / "layers" / layer.name
        )
    _replace_symlink(instructions_dir / "examples", prompts_dir / "examples")

    # Write the generated files
    (instructions_dir / "index.md").write_text(index_text)
    (instructions_dir / MANIFEST_FILE_NAME).write_text(
        yaml.safe_dump(
            {
                "target": manifest.target_name,
                "layers": manifest.layer_names,
                "agents_file": manifest.agents_file_name,
            },
            sort_keys=False,
            default_flow_style=None,
        )
    )
    return manifest


def _check_instructions(instructions_dir: Path):
    if not os.path.lexists(instructions_dir):
        return
    if (
        not instructions_dir.is_symlink()
        and (instructions_dir / MANIFEST_FILE_NAME).is_file()
    ):
        return
    raise InstructionsExistError(
        f"{instructions_dir} already exists, and was not installed by mn-prompts. "
        "Remove it, and try again."
    )


def _get_requested_manifest(
    instructions_dir: Path,
    target_name: T.Optional[str],
    layer_names: T.List[str],
    agents_md: bool,
) -> Manifest:
    if target_name or layer_names:
        manifest = Manifest(target_name=target_name, layer_names=list(layer_names))
        if agents_md:
            manifest.agents_file_name = AGENTS_MD_FILE_NAME
        return manifest

    # Re-install the selection of an earlier install
    manifest = get_manifest(instructions_dir)
    if manifest is None:
        raise MissingSelectionError(
            "Choose what to install with --target and/or --layer (e.g. mn-prompts "
            "install --target=python_lib). Without these, mn-prompts re-installs the "
            f"selection in {instructions_dir / MANIFEST_FILE_NAME}, but there is no "
            "such file."
        )
    if agents_md:
        manifest.agents_file_name = AGENTS_MD_FILE_NAME
    return manifest


def _check_links(instructions_dir: Path):
    if not instructions_dir.is_dir():
        return
    paths = list(instructions_dir.glob("*_layer")) + [instructions_dir / "examples"]
    for path in paths:
        if os.path.lexists(path) and not path.is_symlink():
            raise InstructionsExistError(
                f"{path} is not a symlink, so mn-prompts can't replace it. Remove "
                "it, and try again."
            )


def _replace_symlink(path: Path, target_path: Path):
    if path.is_symlink():
        path.unlink()
    path.symlink_to(target_path)


class InstructionsExistError(Exception):
    pass


class MissingSelectionError(Exception):
    pass
