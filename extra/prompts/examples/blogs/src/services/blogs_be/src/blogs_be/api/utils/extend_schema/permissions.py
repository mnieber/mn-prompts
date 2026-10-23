from blogs_be.common.utils.inspect import get_argument_names


class PermissionResult:
    def __init__(self, permission_allowed, reason=None):
        self.permission_allowed = permission_allowed
        self.reason = reason

    def __bool__(self):
        return self.permission_allowed


def check_permission_spec(permission_fn, resolved_data):
    var_names = get_argument_names(permission_fn)
    kwargs = {
        arg_name: resolved_data[arg_name]
        for arg_name in var_names
        if arg_name in resolved_data
    }
    if len(kwargs) != len(var_names):
        raise ValueError(
            f"Cannot resolve dependencies of permission fn {permission_fn}"
        )

    return permission_fn(**kwargs)


def allow():
    return PermissionResult(True)


def deny(reason):
    return PermissionResult(False, reason)


def checks_permission(fn, permission_fn):
    if not hasattr(fn, "permissions"):
        return False
    return any(permission_fn == p for _, p, *rest in fn.permissions)


def parse_permission_spec(permission_spec):
    if len(permission_spec) not in (2, 3):
        raise ValueError(f"Invalid permission spec: {permission_spec}")

    error_code, permission_fn, *rest = permission_spec
    if rest:
        reason = rest[0]
        if not isinstance(reason, str):
            raise ValueError(f"Invalid permission spec: {permission_spec}")
    else:
        reason = None

    return error_code, permission_fn, reason


def get_permissions_description(permissions):
    permission_names = []
    for permission_spec in permissions if permissions else []:
        error_code, permission_fn, reason = parse_permission_spec(permission_spec)
        permission_names.append(f"- {permission_fn.__name__}\n")

    return (
        "Entrypoint permissions:\n" + "".join(permission_names)
        if permission_names
        else ""
    )
