from functools import wraps
from django_filters.rest_framework import DjangoFilterBackend


def filtered_api_view(filterset_class, model):
    def decorator(cls):
        cls.filterset_class = filterset_class
        cls.filter_backends = [DjangoFilterBackend]
        cls.queryset = model.objects.none()

        @wraps(cls)
        class Wrapper(cls):
            pass

        return Wrapper

    return decorator
