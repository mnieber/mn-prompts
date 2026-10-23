from blogs_be.common.serializers import EmptySerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema


class UserIdResponseSerializer(serializers.Serializer):
    user_id = serializers.EmailField()


class UserIdApiView(APIView):
    @extend_schema(
        request=EmptySerializer,
        responses={
            200: UserIdResponseSerializer,
        },
        data=dict(),
        permissions=[],
    )
    def get(self, request):
        response_data = dict(
            user_id=None if request.user.is_anonymous else request.user.email
        )

        return Response(response_data, status=status.HTTP_200_OK)
