import random
import typing as T

import pytest
from dataclassy import dataclass

from bookie.runtime.entrypoints.bookie import main, run


@dataclass
class Context:
    capsys: pytest.CaptureFixture
    monkeypatch: pytest.MonkeyPatch


class TestEnv:
    __test__ = False

    def __init__(self, context: Context):
        self.context = context
        self.output: T.Optional[str] = None
        self.error_output: T.Optional[str] = None
        self.exit_code: T.Optional[int] = None
        self.error: T.Optional[Exception] = None
        self.system_exit: T.Optional[SystemExit] = None

        # The lorem ipsum texts are random: make them the same in every run
        random.seed(0)

        self.__post_init__()

    def __post_init__(self):
        pass

    def step(self, *_):
        return True

    def run_bookie(self, *args: str):
        self.exit_code = run(list(args))
        self._store_output()

    def run_bookie_and_catch_error(self, *args: str):
        try:
            self.run_bookie(*args)
        except Exception as error:
            self.error = error
            self._store_output()

    def run_bookie_and_catch_exit(self, *args: str):
        try:
            self.run_bookie(*args)
        except SystemExit as system_exit:
            self.system_exit = system_exit
            self._store_output()

    def run_bookie_cli(self, *args: str):
        """Runs bookie like the user does: errors are printed, not raised."""
        self.exit_code = main(list(args))
        self._store_output()

    def _store_output(self):
        captured = self.context.capsys.readouterr()
        self.output = captured.out
        self.error_output = captured.err
