# The test packages are enabled in the order in which their code is implemented
ENABLED_TEST_PACKAGES = [
    "users_tests",
    "blogs_tests",
]

ALL_TEST_PACKAGES = [
    "blogs_tests",
    "users_tests",
]

collect_ignore = [
    package for package in ALL_TEST_PACKAGES if package not in ENABLED_TEST_PACKAGES
]
