import os
from pathlib import Path

from mn_prompts_test_env import Context, TestEnv as MnPromptsTestEnv

__all__ = ["Context", "TestEnv"]


class TestEnv(MnPromptsTestEnv):
    def write_agents_file(self, text: str):
        (self.project_dir / "AGENTS.md").write_text(text)

    def create_instructions_symlink(self, target_path: Path):
        (self.project_dir / "instructions").symlink_to(target_path)

    # Queries

    def instructions_link(self) -> Path:
        return Path(os.readlink(self.project_dir / "instructions"))

    def project_path_exists(self, name: str) -> bool:
        # Also true for a dangling symlink
        return os.path.lexists(self.project_dir / name)

    def read_project_file(self, name: str) -> str:
        return (self.project_dir / name).read_text()

    def agents_file_source(self) -> Path:
        return self.prompts_dir / "agents_files" / "default.md"
