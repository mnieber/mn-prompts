import pytest
from django.urls import get_resolver

from blogs_be.api.utils.extend_schema import extend_schema

HANDLER_NAMES = ["get", "post", "put", "patch", "delete"]

# These views serve the auth endpoints and the api docs, and are not ours to decorate.
THIRD_PARTY_PACKAGES = ["allauth", "drf_spectacular"]


def test_every_view_declares_its_permissions():
    # We collect the request handlers of all the views that have a url.
    handlers = _get_handlers(get_resolver().url_patterns)

    # There should be at least one permission on each handler. A handler without
    # extend_schema would otherwise be public, because that is the default of DRF.
    assert handlers
    missing = [name for name, handler in handlers if not _get_permissions(handler)]
    assert missing == []


@pytest.mark.parametrize("permissions", [None, []])
def test_extend_schema_needs_a_permission(permissions):
    # Decorating a handler without a permission should fail right away, and not
    # when the endpoint is called.
    with pytest.raises(RuntimeError):
        extend_schema(permissions=permissions)


def _get_handlers(url_patterns):
    handlers = []
    for url_pattern in url_patterns:
        if hasattr(url_pattern, "url_patterns"):
            handlers += _get_handlers(url_pattern.url_patterns)
            continue

        view_class = getattr(url_pattern.callback, "cls", None)
        if (
            not view_class
            or view_class.__module__.split(".")[0] in THIRD_PARTY_PACKAGES
        ):
            continue

        for handler_name in HANDLER_NAMES:
            handler = getattr(view_class, handler_name, None)
            if handler:
                handlers.append((f"{view_class.__name__}.{handler_name}", handler))
    return handlers


def _get_permissions(handler):
    return getattr(handler, "permissions", None)
