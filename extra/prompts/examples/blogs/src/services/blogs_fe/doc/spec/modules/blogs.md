[comment]: <> (This file is auto-generated. Do not edit directly.)

# Module: blogs

## Blogs

```python
class Blogs(ReactModule):
    class Types:
        class Blog(Entity):
            name: str
            description: T.Optional[str]
            audience: str = 'expert | novice | any'

        class BlogPost(Entity):
            title: str
            content: T.Optional[str]
            isPublished: bool = False
            level: str = 'easy | medium | hard'
            tags: T.List[str] = []
            blog: FK['Blogs.Types.Blog']

    class Mutations:
        class CreateBlog(Mutation):
            class Args:
                createBlogForm: Form

        class CreateBlogPost(Mutation):
            class Args:
                createBlogPostForm: Form
                blog: 'Blogs.Types.Blog'

        class UpdateBlogPost(Mutation):
            class Args:
                updateBlogPostForm: Form
                blog: 'Blogs.Types.Blog'

        class DeleteBlogPosts(Mutation):
            class Args:
                deleteBlogPostsForm: Form
        class CreateBlogMutation:
            pass

        class CreateBlogPostMutation:
            pass

        class UpdateBlogPostMutation:
            pass

        class DeleteBlogPostsMutation:
            pass

    class Queries:
        class GetBlogs(Query):
            pass

        class GetBlogTags(Query):
            class Args:
                inputValue: str

        class GetBlogPosts(Query):
            pass

    class States:
        class BlogsState:
            class Containers:
                class BlogsCtr:
                    data: Facet
                    selection: Facet
                    highlight: Facet

        class BlogPostsState:
            class Containers:
                class BlogPostsCtr:
                    data: Facet
                    addition: Facet
                    deletion: Facet
                    edit: Facet
                    highlight: Facet
                    selection: Facet

    class Routes:
        class Blogs(Route):
            pass

        class Blog(Route):
            pass

    class StateProviders:
        class BlogsStateProvider:
            pass

        class BlogPostsStateProvider:
            pass

    class Views:
        class BlogFormView(Component):
            pass

        class BlogPostFormView(Component):
            pass

        class BlogListView(Component):
            pass

        class BlogPostListView(Component):
            pass

        class BlogsPage:
            root: Any = dict(__LeftSideBar=dict(blog_list_view=None), __RightCanvas=dict(blog_post_list_view=None, blog_post_form_view=None, create_blog_post_button=None, edit_blog_post_button=None, delete_blog_posts_button=None))
        class BlogView:
            pass

    class Effects:
        class SelectBlogEffect:
            pass

    class Components:
        class CreateBlogButton(DialogButton):
            pass

        class CreateBlogPostButton(DialogButton):
            pass

        class EditBlogPostButton(DialogButton):
            pass

        class DeleteBlogPostsButton(DialogButton):
            pass
```

