from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    def request_user(self):
        if "request" not in self.context:
            raise ValueError("Serializer context is missing request")
        return self.context["request"].user


class ReadSerializerMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "to_internal_value" in cls.__dict__:
            raise TypeError("Overriding 'to_internal_value' is not allowed.")

    def to_internal_value(self, instance):
        raise NotImplementedError(
            "This serializer only supports serialization to JSON."
        )


class WriteSerializerMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "to_representation" in cls.__dict__:
            raise TypeError("Overriding 'to_representation' is not allowed.")

    def to_representation(self, instance):
        raise NotImplementedError(
            "This serializer only supports deserialization from JSON."
        )


class EmptySerializer(serializers.Serializer):
    pass
