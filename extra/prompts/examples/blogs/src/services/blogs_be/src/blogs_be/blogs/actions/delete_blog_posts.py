from blogs_be.common.utils.dataclass import dataclass
from typing import List
from django.db import transaction
from blogs_be.blogs.models import Blog, BlogPost


@dataclass
class DeleteBlogPostsForm:
    blog_post_ids: List[str]


@transaction.atomic
def delete_blog_posts(delete_blog_posts_form: DeleteBlogPostsForm, blog: Blog):
    blog_posts = BlogPost.objects.filter(
        id__in=delete_blog_posts_form.blog_post_ids, blog=blog
    )

    if len(blog_posts) != len(delete_blog_posts_form.blog_post_ids):
        found_ids = set(str(post.id) for post in blog_posts)
        missing_ids = set(delete_blog_posts_form.blog_post_ids) - found_ids
        raise BlogPostsNotFoundError(missing_ids)

    deleted_count = blog_posts.delete()[0]
    return deleted_count


class BlogPostsNotFoundError(Exception):
    def __init__(self, missing_ids):
        self.missing_ids = missing_ids
        super().__init__(f"Blog posts not found: {missing_ids}")
