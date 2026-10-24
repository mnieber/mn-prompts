import pytest
from install_target_tests.install_target_test_env import Context


@pytest.fixture
def context(capsys, monkeypatch, tmp_path):
    return Context(capsys=capsys, monkeypatch=monkeypatch, tmp_path=tmp_path)
