import pytest
from list_targets_tests.list_targets_test_env import Context


@pytest.fixture
def context(capsys, monkeypatch, tmp_path):
    return Context(capsys=capsys, monkeypatch=monkeypatch, tmp_path=tmp_path)
