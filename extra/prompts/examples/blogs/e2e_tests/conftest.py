import pytest
from e2e_test_env import Context


@pytest.fixture
def context(tmp_path, monkeypatch, request):
    return Context(tmp_path=tmp_path, monkeypatch=monkeypatch, request=request)
