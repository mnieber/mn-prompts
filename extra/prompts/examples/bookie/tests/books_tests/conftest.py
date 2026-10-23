import pytest
from books_tests.books_test_env import Context


@pytest.fixture
def context(capsys, monkeypatch):
    return Context(capsys=capsys, monkeypatch=monkeypatch)
