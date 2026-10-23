from blogs_be.blogs.shortcuts import get_blog_or_400
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.blogs.models import BlogPost
from blogs_be.blogs.serializers import BlogPostSerializer
from blogs_be.blogs.filters import BlogPostFilterSet
from blogs_be.common.utils.apply_filter_set_or_400 import apply_filter_set_or_400


class GetBlogPostsApiView(APIView):
    filterset_class = BlogPostFilterSet
    queryset = BlogPost.objects.none()

    @extend_schema(
        responses={
            200: BlogPostSerializer(many=True),
        },
        data=dict(
            blog=get_blog_or_400,
        ),
        permissions=[],
    )
    def get(self, request, blog):
        blog_posts = apply_filter_set_or_400(
            BlogPost.objects.filter(blog=blog), BlogPostFilterSet, request.query_params
        )
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
