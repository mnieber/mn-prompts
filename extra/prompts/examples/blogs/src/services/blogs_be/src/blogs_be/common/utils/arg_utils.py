def optional_args(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}
