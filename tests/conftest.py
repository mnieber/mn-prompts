# The test packages are enabled in the order in which their code is implemented
ENABLED_TEST_PACKAGES = []

ALL_TEST_PACKAGES = [
    "list_targets_tests",
    "install_target_tests",
]

collect_ignore = [
    package for package in ALL_TEST_PACKAGES if package not in ENABLED_TEST_PACKAGES
]
