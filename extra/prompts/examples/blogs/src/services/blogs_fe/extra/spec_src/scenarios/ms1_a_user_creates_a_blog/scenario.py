import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("ms1_a_user_creates_a_blog")


def run_scenario():
    r.user = c.External.Actors.User
    r.blog_list_view = c.Blogs.Views.BlogListView
    r.blog_form_view = c.Blogs.Views.BlogFormView
    r.create_blog_mutation = c.Blogs.Mutations.CreateBlog

    with goal().create_a(r.blog).for_the(r.user):
        the(r.user).visits_the(r.blogs_route)
        the(r.blog_list_view).shows(r.create_blog_button)
        the(r.user).presses(r.create_blog_button)
        the(r.user).submits(r.blog_form)
        with the(r.blog_form_view).calls(r.create_blog_mutation).with_the(r.blog_form_data):
            it().creates(r.blog)
            it().returns(r.blog)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog")

markdown_node.markdown = """
The user visits the blogs route and presses the create-blog button to open the blog form.
After filling out the form and submitting, `BlogFormView` calls `CreateBlog` which creates
and returns the new blog.

### Steps

#### It creates the blog

The user visits the blogs route.</br>
`BlogListView` shows the create-blog button.</br>
The user presses the create-blog button to open `BlogFormView`.</br>
The user fills out and submits the blog form.</br>
`BlogFormView` calls `CreateBlog` with the blog form data.</br>
`CreateBlog` creates and returns the blog.</br>

### Diagram

```mermaid
sequenceDiagram
    participant User
    participant BLV as BlogListView
    participant BFV as BlogFormView
    participant CBM as CreateBlog (mutation)

    Note over User,CBM: Create blog
    User->>BLV: visits blogs route
    BLV-->>User: shows create-blog button
    User->>BFV: presses create-blog button
    User-->>BFV: submits blog form
    BFV->>CBM: createBlog(blogFormData)
    CBM->>CBM: create blog
    CBM-->>BFV: blog
```
"""
