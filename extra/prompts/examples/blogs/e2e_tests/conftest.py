from pathlib import Path

import pytest
from e2e_test_env import Context

# The test files whose code is written, in the order in which it was implemented.
# The other test files are ignored until their code is written.
ENABLED_TEST_FILES = [
    "test_developer_runs_commands_in_a_tmux_session.py",
    "test_developer_builds_and_starts_the_stack.py",
    "test_developer_uses_local_settings.py",
    "test_compose_impl.py",
    "test_developer_restarts_the_stack.py",
    "test_developer_runs_a_command_in_a_new_container.py",
    "test_python_impl.py",
    "test_developer_publishes_a_python_lib.py",
    "test_developer_initialises_the_stack.py",
]

collect_ignore = [
    path.name
    for path in Path(__file__).parent.glob("test_*.py")
    if path.name not in ENABLED_TEST_FILES
]


@pytest.fixture
def context(tmp_path, monkeypatch, request):
    return Context(tmp_path=tmp_path, monkeypatch=monkeypatch, request=request)
