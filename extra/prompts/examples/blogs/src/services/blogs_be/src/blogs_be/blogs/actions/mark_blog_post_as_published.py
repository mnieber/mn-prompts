from blogs_be.blogs.models import BlogPost


def mark_blog_post_as_published(blog_post: BlogPost):
    blog_post.is_published = True
    blog_post.save(update_fields=["is_published"])

    return blog_post
