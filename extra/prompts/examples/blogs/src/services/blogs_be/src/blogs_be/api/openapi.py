from drf_spectacular.openapi import AutoSchema
from rest_framework import serializers
from rest_framework.permissions import AND, NOT, OR
from drf_spectacular.extensions import OpenApiFilterExtension
from blogs_be.api.utils.extend_schema import get_permissions_description
from django_filters.rest_framework import DjangoFilterBackend


class DummySerializer(serializers.Serializer):
    def to_internal_value(self, data):
        return data

    def to_representation(self, instance):
        return instance

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class ValidationErrorSerializer(DummySerializer):
    errors = serializers.DictField(
        child=serializers.ListSerializer(child=serializers.CharField())
    )
    non_field_errors = serializers.ListSerializer(child=serializers.CharField())


class GenericErrorSerializer(DummySerializer):
    detail = serializers.CharField()


class UnauthenticatedErrorSerializer(GenericErrorSerializer):
    pass


class ForbiddenErrorSerializer(GenericErrorSerializer):
    pass


class NotFoundErrorSerializer(GenericErrorSerializer):
    pass


class ConflictErrorSerializer(GenericErrorSerializer):
    pass


def permission_str(permission):
    if isinstance(permission, OR):
        op1 = permission_str(permission.op1)
        op2 = permission_str(permission.op2)
        return f"({op1} | {op2})"
    elif isinstance(permission, AND):
        op1 = permission_str(permission.op1)
        op2 = permission_str(permission.op2)
        return f"({op1} & {op2})"
    elif isinstance(permission, NOT):
        op1 = permission_str(permission.op1)
        return f"~{op1}"
    return permission.__class__.__name__


class AutoSchemaWithErrorResponses(AutoSchema):
    def _get_response_bodies(self):
        # Inspired by https://github.com/tfranzel/drf-spectacular/issues/101#issuecomment-1069383391

        response_bodies = super()._get_response_bodies()

        add_error_codes = []
        if not self.method == "GET":
            add_error_codes.append("400")
            add_error_codes.append("409")

        if self.get_auth():
            add_error_codes.append("401")
            add_error_codes.append("403")

        if not (self.method == "GET" and self._is_list_view()):
            if len(list(filter(lambda _: _["in"] == "path", self._get_parameters()))):
                add_error_codes.append("404")

        self.error_response_bodies = {
            "400": self._get_response_for_code(ValidationErrorSerializer, "400"),
            "401": self._get_response_for_code(UnauthenticatedErrorSerializer, "401"),
            "403": self._get_response_for_code(ForbiddenErrorSerializer, "403"),
            "404": self._get_response_for_code(NotFoundErrorSerializer, "404"),
            "409": self._get_response_for_code(ConflictErrorSerializer, "409"),
        } | response_bodies
        for code in add_error_codes:
            response_bodies[code] = self.error_response_bodies[code]
        return response_bodies

    def _get_filter_parameters(self):
        if getattr(self.view, "filterset_class", None) is None:
            return []

        filter_backends = getattr(self.view, "filter_backends", [DjangoFilterBackend])
        parameters = []
        for filter_backend in filter_backends:
            filter_extension = OpenApiFilterExtension.get_match(filter_backend())
            if filter_extension:
                parameters += filter_extension.get_schema_operation_parameters(self)
            else:
                parameters += filter_backend().get_schema_operation_parameters(
                    self.view
                )
        return parameters

    def get_description(self):
        """
        Append details about permissions to the description.
        """
        description = super().get_description()

        action_or_method = getattr(
            self.view, getattr(self.view, "action", self.method.lower()), None
        )
        action_or_method_permissions = getattr(action_or_method, "permissions", None)
        if action_or_method_permissions:
            description += get_permissions_description(action_or_method_permissions)

        permissions = self.view.get_permissions()
        if not permissions:
            return description
        return (
            description
            + "\n\nPermissions: "
            + " & ".join([permission_str(permission) for permission in permissions])
        )
