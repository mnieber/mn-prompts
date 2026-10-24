import typing as T
from pathlib import Path

import pytest
from dataclassy import dataclass

import mn_prompts
from mn_prompts.runtime.entrypoints.mn_prompts import main, run

AGENTS_FILE_TEXT = "# Agents\n\nRead instructions/index.md before you write any code.\n"


@dataclass
class Context:
    capsys: pytest.CaptureFixture
    monkeypatch: pytest.MonkeyPatch
    tmp_path: Path


class TestEnv:
    __test__ = False

    def __init__(self, context: Context):
        self.context = context
        self.clone_dir: T.Optional[Path] = None
        self.prompts_dir: T.Optional[Path] = None
        self.project_dir: T.Optional[Path] = None
        self.output: T.Optional[str] = None
        self.error_output: T.Optional[str] = None
        self.exit_code: T.Optional[int] = None
        self.error: T.Optional[Exception] = None
        self.system_exit: T.Optional[SystemExit] = None
        self.__post_init__()

    def __post_init__(self):
        pass

    def step(self, *_):
        return True

    def install_editable(self, target_names: T.List[str]):
        """Creates a clone of mn-prompts with these targets, and installs it."""
        self.clone_dir = self.context.tmp_path / "mn-prompts"
        self.prompts_dir = self.clone_dir / "extra" / "prompts"
        for target_name in target_names:
            target_dir = self.prompts_dir / "targets" / target_name
            target_dir.mkdir(parents=True)
            (target_dir / "index.md").write_text(f"# Instructions for {target_name}\n")
        (self.prompts_dir / "targets").mkdir(parents=True, exist_ok=True)
        (self.prompts_dir / "agents_files").mkdir(parents=True)
        (self.prompts_dir / "agents_files" / "default.md").write_text(AGENTS_FILE_TEXT)
        self._locate_package(self.clone_dir / "src" / "mn_prompts")

    def install_regular(self):
        """Installs mn-prompts in site-packages, where there is no prompts-dir."""
        self._locate_package(
            self.context.tmp_path / "env" / "site-packages" / "mn_prompts"
        )

    def enter_project_dir(self):
        self.project_dir = self.context.tmp_path / "my_project"
        self.project_dir.mkdir()
        self.context.monkeypatch.chdir(self.project_dir)

    def run_mn_prompts(self, *args: str):
        self.exit_code = run(list(args))
        self._store_output()

    def run_mn_prompts_and_catch_error(self, *args: str):
        try:
            self.run_mn_prompts(*args)
        except Exception as error:
            self.error = error
            self._store_output()

    def run_mn_prompts_cli(self, *args: str):
        """Runs mn-prompts like the user does: errors are printed, not raised."""
        self.exit_code = main(list(args))
        self._store_output()

    def _locate_package(self, package_dir: Path):
        # The prompts-dir is found relative to the source code of the package
        self.context.monkeypatch.setattr(
            mn_prompts, "__file__", str(package_dir / "__init__.py")
        )

    def _store_output(self):
        captured = self.context.capsys.readouterr()
        self.output = captured.out
        self.error_output = captured.err

    # Queries

    def output_lines(self) -> T.List[str]:
        return self.output.splitlines()
