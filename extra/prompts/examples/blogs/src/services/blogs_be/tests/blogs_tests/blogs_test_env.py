import typing as T

from blogs_be_test_env import Context, TestEnv as BlogsBeTestEnv

from blogs_be.blogs.models import Blog, BlogPost

__all__ = ["Context", "TestEnv"]


class TestEnv(BlogsBeTestEnv):
    def create_blog(self, name: str, description=None):
        self._post(
            "create-blog",
            create_blog_form=dict(name=name, description=description),
        )

    def create_blog_post(self, blog_slug: str, title: str, content=None):
        self._post(
            "create-blog-post",
            url_kwargs=dict(blog_key=blog_slug),
            create_blog_post_form=dict(title=title, content=content),
        )

    def update_blog_post(
        self, blog_slug: str, blog_post_slug: str, title=None, content=None
    ):
        self._post(
            "update-blog-post",
            url_kwargs=dict(blog_key=blog_slug, blog_post_key=blog_post_slug),
            update_blog_post_form=dict(title=title, content=content),
        )

    def delete_blog_posts(self, blog_slug: str, blog_post_ids: T.List[str]):
        self._post(
            "delete-blog-posts",
            url_kwargs=dict(blog_key=blog_slug),
            delete_blog_posts_form=dict(blog_post_ids=blog_post_ids),
        )

    def get_blogs(self):
        self._get("get-blogs")

    def get_blog_posts(self, blog_slug: str):
        self._get("get-blog-posts", url_kwargs=dict(blog_key=blog_slug))

    def blog_id(self, slug: str) -> str:
        return str(Blog.objects.get(slug=slug).id)

    def blog_post_id(self, title: str) -> str:
        return str(BlogPost.objects.get(title=title).id)

    def blog_post_titles(self, blog_slug: str) -> T.List[str]:
        return sorted(
            BlogPost.objects.filter(blog__slug=blog_slug).values_list(
                "title", flat=True
            )
        )
