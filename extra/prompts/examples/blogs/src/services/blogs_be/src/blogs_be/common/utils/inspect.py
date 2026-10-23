import inspect


def get_argument_names(f):
    signature = inspect.signature(f)
    return list(signature.parameters.keys())
