import os
import re
import typing as T
from pathlib import Path

import yaml
from mn_prompts_test_env import Context, TestEnv as MnPromptsTestEnv

__all__ = ["Context", "TestEnv"]

DJANGO_LAYERS = {
    "app": [],
    "python_lib": ["app"],
    "django_app": ["app", "python_lib"],
    "react_app": ["app"],
    "local_env": [],
}


class TestEnv(MnPromptsTestEnv):
    def write_agents_file(self, text: str, name: str = "CLAUDE.md"):
        (self.project_dir / name).write_text(text)

    def write_project_file(self, name: str, text: str):
        (self.project_dir / name).write_text(text)

    def create_instructions_symlink(self, target_path: Path):
        (self.project_dir / "instructions").symlink_to(target_path)

    # Queries

    def instructions_entries(self) -> T.List[str]:
        return sorted(
            path.name for path in (self.project_dir / "instructions").iterdir()
        )

    def link(self, name: str) -> Path:
        return Path(os.readlink(self.project_dir / name))

    def layer_dir(self, layer_name: str) -> Path:
        return self.prompts_dir / "layers" / layer_name

    def project_path_exists(self, name: str) -> bool:
        # Also true for a dangling symlink
        return os.path.lexists(self.project_dir / name)

    def read_project_file(self, name: str) -> str:
        return (self.project_dir / name).read_text()

    def read_manifest(self) -> T.Dict:
        return yaml.safe_load(self.read_project_file("instructions/mn-prompts.yaml"))

    def index_layer_order(self) -> T.List[str]:
        """Returns the layers of the snippets in the generated index, in order."""
        return re.findall(
            r"Consult \./(\w+)_layer/", self.read_project_file("instructions/index.md")
        )

    def agents_file_source(self) -> Path:
        return self.prompts_dir / "agents_files" / "default.md"
