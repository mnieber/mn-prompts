def pytest_collection_modifyitems(config, items):
    keyword_expression = config.getoption("-k")
    if keyword_expression.endswith("__"):
        # Correct the -k option to remove the "__" suffix
        new_keyword_expression = keyword_expression[:-2]
        config.option.keyword = new_keyword_expression

        # Reduce the number of items to only include the one test
        # that matches the new keyword expression
        modified_items = []
        for item in items:
            test_name = item.nodeid.split("::")[-1].split("[")[0]
            if test_name == new_keyword_expression:
                modified_items.append(item)

        items[:] = [item for item in modified_items]
