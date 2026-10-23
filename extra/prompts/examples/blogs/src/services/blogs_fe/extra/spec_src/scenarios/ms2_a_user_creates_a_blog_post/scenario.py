import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("ms2_a_user_creates_a_blog_post")


def run_scenario():
    r.user = c.External.Actors.User
    r.blog_list_view = c.Blogs.Views.BlogListView
    r.blog_view = c.Blogs.Views.BlogView
    r.blog_post_form_view = c.Blogs.Views.BlogPostFormView
    r.create_blog_post_mutation = c.Blogs.Mutations.CreateBlogPost

    with goal().create_a(r.blog_post).in_the(r.blog):
        the(r.user).visits_the(r.blogs_route)
        the(r.user).clicks_on_a(r.blog).to_visit_the(r.blog_route)
        the(r.blog_view).shows(r.create_blog_post_button)
        the(r.user).presses(r.create_blog_post_button)
        the(r.user).submits(r.blog_post_form)
        with the(r.blog_post_form_view).calls(r.create_blog_post_mutation).with_the(r.blog_post_form_data):
            it().creates(r.blog_post)
            it().returns(r.blog_post)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog post")

markdown_node.markdown = """
The user visits a blog and presses the create-blog-post button to open the blog-post form.
After filling out the form and submitting, `BlogPostFormView` calls `CreateBlogPost` which
creates and returns the new blog post.

### Steps

#### It creates the blog post

The user visits the blogs route and clicks on a blog to open it.</br>
`BlogView` shows the create-blog-post button.</br>
The user presses the create-blog-post button to open `BlogPostFormView`.</br>
The user fills out and submits the blog-post form.</br>
`BlogPostFormView` calls `CreateBlogPost` with the blog-post form data.</br>
`CreateBlogPost` creates and returns the blog post.</br>

### Diagram

```mermaid
sequenceDiagram
    participant User
    participant BLV as BlogListView
    participant BV as BlogView
    participant BPFV as BlogPostFormView
    participant CBPM as CreateBlogPost (mutation)

    Note over User,CBPM: Create blog post
    User->>BLV: visits blogs route
    User->>BV: clicks on a blog
    BV-->>User: shows create-blog-post button
    User->>BPFV: presses create-blog-post button
    User-->>BPFV: submits blog-post form
    BPFV->>CBPM: createBlogPost(blogPostFormData)
    CBPM->>CBPM: create blog post
    CBPM-->>BPFV: blog post
```
"""
