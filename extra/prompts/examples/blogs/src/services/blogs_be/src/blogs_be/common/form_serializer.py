from argparse import Namespace
from typing import Union, get_args, get_origin
from uuid import UUID

from rest_framework import serializers


class FormSerializer(serializers.Serializer):
    def __init_subclass__(cls, **kwargs):
        form_class = _get_form_class(cls)
        for field_name, annotated_field_type in form_class.__annotations__.items():
            if field_name in cls._declared_fields:
                continue

            optional, field_type = _is_optional_type(annotated_field_type)
            if not field_type:
                raise Exception(
                    f"Unsupported optional type {field_type}. "
                    + f"Please check the '{field_name}' field."
                )

            is_list = _is_list_type(field_type)
            if is_list:
                field_type = get_args(field_type)[0]
            else:
                field_type = field_type

            field_kwargs = {}
            if not is_list and optional:
                field_kwargs["required"] = False
                if not field_type == bool:
                    field_kwargs["allow_blank"] = True
                    field_kwargs["allow_null"] = True

            if field_type == UUID:
                field = serializers.UUIDField(**field_kwargs)
            elif field_type == str:
                field = serializers.CharField(**field_kwargs)
            elif field_type == bool:
                field = serializers.BooleanField(**field_kwargs)
            elif hasattr(field_type, "choices"):
                field = serializers.ChoiceField(
                    choices=field_type.choices, **field_kwargs
                )
            elif not field_name.startswith("__"):
                raise Exception(
                    f"FormSerializer does not support {field_type}. "
                    + f"Please check the '{field_name}' field."
                )

            if is_list:
                list_kwargs = dict(child=field)
                if optional:
                    list_kwargs["required"] = False
                cls._declared_fields[field_name] = serializers.ListField(**list_kwargs)
            else:
                cls._declared_fields[field_name] = field

        super().__init_subclass__(**kwargs)

    def validate(self, data):
        return _get_form_class(self)(**data)


def _is_list_type(field_type):
    return get_origin(field_type) == list


def _is_optional_type(field_type):
    if get_origin(field_type) == Union:
        args = get_args(field_type)
        none_arg = [arg for arg in args if arg == type(None)]
        some_args = [arg for arg in args if arg != type(None)]
        some_arg = next(iter(some_args), None)
        return bool(none_arg), some_arg
    return False, field_type


def _get_form_class(cls):
    if hasattr(cls, "Meta") and getattr(cls.Meta, "form_class", None):
        return cls.Meta.form_class
    return Namespace
