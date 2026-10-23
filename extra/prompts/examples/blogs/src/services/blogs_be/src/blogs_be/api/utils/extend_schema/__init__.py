from drf_spectacular.utils import extend_schema as drf_extend_schema
from rest_framework.response import Response

from blogs_be.api.utils.extend_schema.data_spec import (
    get_data_kwargs,
    resolve_data_spec,
)
from blogs_be.api.utils.extend_schema.permissions import (  # noqa: F401
    PermissionResult,
    allow,
    check_permission_spec,
    deny,
    get_permissions_description,
    parse_permission_spec,
)
from blogs_be.common.utils.inspect import get_argument_names


def extend_schema(
    *args,
    data=None,
    permissions=None,
    request_arg_pos=1,
    **kwargs,
):
    serializer_class = kwargs.get("request")

    def wrapper(f):
        def wrapped_f(*args, **kwargs):
            request = (
                args[request_arg_pos] if request_arg_pos != -1 else kwargs["request"]
            )
            initial_resolved_data = kwargs.copy()
            if request:
                initial_resolved_data["user"] = request.user
                if serializer_class:
                    serializer = serializer_class(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    request_data = serializer.validated_data
                    initial_resolved_data.update(request_data.__dict__)
                else:
                    request_data = None

            resolved_data = resolve_data_spec(data or {}, initial_resolved_data)
            for permission_spec in permissions or []:
                error_code, permission_fn, reason = parse_permission_spec(
                    permission_spec
                )
                permission_result = check_permission_spec(permission_fn, resolved_data)
                assert isinstance(permission_result, PermissionResult)
                if not permission_result.permission_allowed:
                    return Response(
                        dict(detail=reason or permission_result.reason),
                        status=error_code,
                    )

            data_kwargs = get_data_kwargs(
                get_argument_names(f),
                request_data,
                resolved_data,
                # TODO: do we still need this block-list?
                ["serializer", "user"],
            )

            return f(*args, **data_kwargs)

        wrapped_f.permissions = permissions

        return drf_extend_schema(**kwargs)(wrapped_f)

    return wrapper
