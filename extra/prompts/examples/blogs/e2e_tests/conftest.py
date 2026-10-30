from pathlib import Path

import pytest
from e2e_test_env import Context

# The test files whose code is written, in the order in which it was implemented.
# The other test files are ignored until their code is written.
ENABLED_TEST_FILES = []

collect_ignore = [
    path.name
    for path in Path(__file__).parent.glob("test_*.py")
    if path.name not in ENABLED_TEST_FILES
]


@pytest.fixture
def context(tmp_path, monkeypatch, request):
    return Context(tmp_path=tmp_path, monkeypatch=monkeypatch, request=request)
