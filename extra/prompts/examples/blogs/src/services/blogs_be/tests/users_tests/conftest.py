import pytest
from users_tests.users_test_env import Context
from rest_framework.test import APIClient


@pytest.fixture
def context(db):
    return Context(api_client=APIClient())
