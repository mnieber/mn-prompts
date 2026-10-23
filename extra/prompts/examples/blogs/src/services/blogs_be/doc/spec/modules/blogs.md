[comment]: <> (This file is auto-generated. Do not edit directly.)

# Module: blogs

## Blogs

```python
class Blogs(DjangoModule):
    class Models:
        class Blog(Entity):
            name: str
            description: T.Optional[str]
            audience: str = 'Audiences: expert | novice | any'
            blog_posts: RelatedSet['Blogs.Models.BlogPost'] = []

        class BlogPost(Entity):
            title: str
            content: T.Optional[str]
            blog: FK['Blogs.Models.Blog']

    class DomainEvents:
        class BlogCreated:
            pass

        class BlogPostCreated:
            pass

    class ApiViews:
        class CreateBlogApiView:
            pass

        class CreateBlogPostApiView:
            pass

        class UpdateBlogPostApiView:
            pass

        class DeleteBlogPostsApiView:
            pass

    class Actions:
        class CreateBlog:
            pass

        class CreateBlogPost:
            pass

        class UpdateBlogPost:
            pass

        class DeleteBlogPosts:
            pass

    class Rules:
        class HasForbiddenWords:
            pass
```

