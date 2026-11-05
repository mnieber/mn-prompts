import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def clear_cache():
    """The rate limits of allauth are stored in the cache, which outlives a test."""
    cache.clear()


# The test packages are enabled in the order in which their code is implemented
ENABLED_TEST_PACKAGES = [
    "users_tests",
    "blogs_tests",
    "api_tests",
]

ALL_TEST_PACKAGES = [
    "api_tests",
    "blogs_tests",
    "users_tests",
]

collect_ignore = [
    package for package in ALL_TEST_PACKAGES if package not in ENABLED_TEST_PACKAGES
]
