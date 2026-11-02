import pytest
from list_tests.list_test_env import Context


@pytest.fixture
def context(capsys, monkeypatch, tmp_path):
    return Context(capsys=capsys, monkeypatch=monkeypatch, tmp_path=tmp_path)
