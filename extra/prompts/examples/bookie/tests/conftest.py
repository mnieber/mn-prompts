# The test packages are enabled in the order in which their code is implemented
ENABLED_TEST_PACKAGES = [
    "chapters_tests",
    "books_tests",
]

ALL_TEST_PACKAGES = [
    "books_tests",
    "chapters_tests",
]

collect_ignore = [
    package for package in ALL_TEST_PACKAGES if package not in ENABLED_TEST_PACKAGES
]
