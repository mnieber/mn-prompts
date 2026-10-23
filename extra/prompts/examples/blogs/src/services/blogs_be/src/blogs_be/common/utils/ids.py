import uuid


def is_uuid(x):
    try:
        uuid.UUID(x)
        return True
    except ValueError:
        return False
