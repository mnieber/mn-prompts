import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s10_a_user_creates_a_blog")


def run_scenario():
    r.user = c.External.Actors.User
    r.blog_list_view = c.Blogs.Views.BlogListView
    r.dashboard_frame = c.Frames.Views.DashboardFrame
    r.blog_form_view = c.Blogs.Views.BlogFormView
    r.create_blog_mutation = c.Blogs.Mutations.CreateBlog

    with goal().create_a(r.blog).for_the(r.user):
        the(r.user).visits_the(r.blogs_route)
        the(r.dashboard_frame).shows(r.create_blog_button)
        the(r.user).presses(r.create_blog_button)
        the(r.user).submits(r.blog_form)
        with the(r.blog_form_view).calls(r.create_blog_mutation).with_the(r.blog_form_data):
            it().creates(r.blog)
            it().returns(r.blog)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog")

markdown_node.markdown = """
The user creates a new blog from the blog list, with a form.

## Diagram

```mermaid
flowchart TD
    visit(["The user visits the blogs route"]) --> button

    subgraph create_blog ["Create a blog for the user"]
        button["Show the create-blog button in the top bar of the DashboardFrame"] --> press["The user presses the create-blog button"]
        press --> form["The user fills out and submits the blog form"]
        form --> create["Create the blog [1]"]
    end
```

### Footnotes

#### [1] - The BlogFormView creates the blog with a mutation

`BlogFormView` calls `CreateBlog` with the blog form data. `CreateBlog` creates and returns the blog.</br>
"""
