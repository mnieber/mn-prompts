from blogs_be.blogs.views.create_blog_api_view import CreateBlogApiView
from blogs_be.blogs.views.create_blog_post_api_view import CreateBlogPostApiView
from blogs_be.blogs.views.get_blogs_api_view import GetBlogsApiView
from django.urls import path
from blogs_be.blogs.views.get_blog_posts_api_view import GetBlogPostsApiView
from blogs_be.blogs.views.delete_blog_posts_api_view import DeleteBlogPostsApiView
from blogs_be.blogs.views.update_blog_post_api_view import UpdateBlogPostApiView

urlpatterns = [
    path(
        "create/",
        CreateBlogApiView.as_view(),
        name="create-blog",
    ),
    path(
        "list/",
        GetBlogsApiView.as_view(),
        #
        name="get-blogs",
    ),
    path(
        "<str:blog_key>/blog-posts/create/",
        CreateBlogPostApiView.as_view(),
        name="create-blog-post",
    ),
    path(
        "<str:blog_key>/blog-posts/<str:blog_post_key>/update/",
        UpdateBlogPostApiView.as_view(),
        name="update-blog-post",
    ),
    path(
        "<str:blog_key>/blog-posts/delete/",
        DeleteBlogPostsApiView.as_view(),
        name="delete-blog-posts",
    ),
    path(
        "<str:blog_key>/blog-posts/list/",
        GetBlogPostsApiView.as_view(),
        name="get-blog-posts",
    ),
]
