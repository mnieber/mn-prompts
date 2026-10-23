import pytest
from blogs_tests.blogs_test_env import Context
from rest_framework.test import APIClient


@pytest.fixture
def context(db):
    return Context(api_client=APIClient())
