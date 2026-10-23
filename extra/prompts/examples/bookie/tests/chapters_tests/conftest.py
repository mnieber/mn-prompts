import pytest
from chapters_tests.chapters_test_env import Context


@pytest.fixture
def context(capsys, monkeypatch):
    return Context(capsys=capsys, monkeypatch=monkeypatch)
