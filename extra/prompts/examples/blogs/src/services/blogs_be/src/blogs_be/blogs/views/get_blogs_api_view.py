from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs_be.blogs.models import Blog
from blogs_be.blogs.serializers import BlogSerializer
from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.utils.apply_filter_set_or_400 import apply_filter_set_or_400
from blogs_be.blogs.filters import BlogFilterSet


class GetBlogsApiView(APIView):
    filterset_class = BlogFilterSet
    queryset = Blog.objects.none()

    @extend_schema(
        responses={
            200: BlogSerializer(many=True),
        },
        data=dict(),
        permissions=[],
    )
    def get(self, request):
        blogs = apply_filter_set_or_400(
            Blog.objects.all(), BlogFilterSet, request.query_params
        )
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
