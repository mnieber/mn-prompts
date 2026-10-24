import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_user_updates_a_blog_post")


def run_scenario():
    r.user = c.External.Actors.User
    r.blogs_page = c.Blogs.Views.BlogsPage
    r.blog_post_form_view = c.Blogs.Views.BlogPostFormView
    r.update_blog_post_mutation = c.Blogs.Mutations.UpdateBlogPost
    r.delete_blog_posts_mutation = c.Blogs.Mutations.DeleteBlogPosts

    with goal().edit_a(r.blog_post).in_the(r.blog):
        the(r.user).selects_the(r.blog_post).they_want_to_edit()
        the(r.blogs_page).shows(r.edit_blog_post_button)
        the(r.user).presses(r.edit_blog_post_button)
        the(r.user).submits(r.blog_post_form)
        with the(r.blog_post_form_view).calls(r.update_blog_post_mutation).with_the(r.blog_post_form_data):
            it().updates(r.blog_post)
            it().returns(r.blog_post)

    with goal().delete_some(r.blog_posts).in_the(r.blog):
        the(r.user).selects_the(r.blog_posts).they_want_to_delete()
        the(r.blogs_page).shows(r.delete_blog_posts_button)
        the(r.user).presses(r.delete_blog_posts_button)
        with the(r.blogs_page).calls(r.delete_blog_posts_mutation).with_the(r.blog_posts):
            it().deletes(r.blog_posts)


markdown_node = sunya.add_markdown_node(
    scenario, "A user updates and deletes a blog post"
)

markdown_node.markdown = """
The user can update or delete blog posts. To update, the user selects a blog post and uses
the edit form to submit changes. To delete, the user selects blog posts and confirms deletion.

### Steps

#### It edits a blog post

The user selects the blog post they want to edit.</br>
`BlogsPage` shows the edit-blog-post button.</br>
The user presses the edit-blog-post button to open `BlogPostFormView`.</br>
The user updates and submits the blog-post form.</br>
`BlogPostFormView` calls `UpdateBlogPost` with the blog-post form data.</br>
`UpdateBlogPost` updates and returns the blog post.</br>

#### It deletes blog posts

The user selects the blog posts they want to delete.</br>
`BlogsPage` shows the delete-blog-posts button.</br>
The user presses the delete-blog-posts button.</br>
`BlogsPage` calls `DeleteBlogPosts` with the selected blog posts.</br>
`DeleteBlogPosts` deletes the blog posts.</br>

### Diagram

```mermaid
sequenceDiagram
    participant User
    participant BP as BlogsPage
    participant BPFV as BlogPostFormView
    participant UBPM as UpdateBlogPost (mutation)
    participant DBPM as DeleteBlogPosts (mutation)

    Note over User,UBPM: Edit blog post
    User-->>BP: selects blog post to edit
    BP-->>User: shows edit-blog-post button
    User->>BPFV: presses edit-blog-post button
    User-->>BPFV: submits blog-post form
    BPFV->>UBPM: updateBlogPost(blogPostFormData)
    UBPM->>UBPM: update blog post
    UBPM-->>BPFV: blog post

    Note over User,DBPM: Delete blog posts
    User-->>BP: selects blog posts to delete
    BP-->>User: shows delete-blog-posts button
    User-->>BP: presses delete-blog-posts button
    BP->>DBPM: deleteBlogPosts(blogPosts)
    DBPM->>DBPM: delete blog posts
    DBPM-->>BP: (done)
```
"""
