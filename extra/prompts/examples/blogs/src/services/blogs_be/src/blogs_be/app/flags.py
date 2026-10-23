_flags = dict()


def get_flag(flag):
    if flag not in _flags:
        raise KeyError(f"Flag does not exist: {flag}")
    return _flags.get(flag)


def set_flag(flag, value):
    if flag not in _flags:
        raise KeyError(f"Flag does not exist: {flag}")
    _flags[flag] = value
