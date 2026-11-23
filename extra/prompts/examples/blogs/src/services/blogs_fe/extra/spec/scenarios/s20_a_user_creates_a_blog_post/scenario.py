import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s20_a_user_creates_a_blog_post")


def run_scenario():
    r.user = c.External.Actors.User
    r.blog_list_view = c.Blogs.Views.BlogListView
    r.blogs_page = c.Blogs.Views.BlogsPage
    r.blog_post_form_view = c.Blogs.Views.BlogPostFormView
    r.create_blog_post_mutation = c.Blogs.Mutations.CreateBlogPost

    with goal().create_a(r.blog_post).in_the(r.blog):
        the(r.user).visits_the(r.blogs_route)
        the(r.user).clicks_on_a(r.blog).to_visit_the(r.blog_route)
        the(r.blogs_page).shows(r.create_blog_post_button)
        the(r.user).presses(r.create_blog_post_button)
        the(r.user).submits(r.blog_post_form)
        with the(r.blog_post_form_view).calls(r.create_blog_post_mutation).with_the(r.blog_post_form_data):
            it().creates(r.blog_post)
            it().returns(r.blog_post)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog post")

markdown_node.markdown = """
The user creates a new blog post in a blog, with a form.

## Diagram

```mermaid
flowchart TD
    visit(["The user visits the blogs route"]) --> open_blog

    subgraph create_blog_post ["Create a blog post in the blog"]
        open_blog["The user clicks on a blog to open it"] --> button["Show the create-blog-post button in the BlogsPage"]
        button --> press["The user presses the create-blog-post button"]
        press --> form["The user fills out and submits the blog-post form"]
        form --> create["Create the blog post [1]"]
    end
```

### Footnotes

#### [1] - The BlogPostFormView creates the blog post with a mutation

`BlogPostFormView` calls `CreateBlogPost` with the blog-post form data. `CreateBlogPost` creates and returns the blog
post.</br>
"""
