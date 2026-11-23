import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s10_a_user_creates_a_blog")


def run_scenario():
    r.frontend = c.External.Actors.Frontend
    r.create_blog_api_view = c.Blogs.ApiViews.CreateBlogApiView
    r.create_blog_action = c.Blogs.Actions.CreateBlog
    r.has_forbidden_words_rule = c.Blogs.Rules.HasForbiddenWords

    with goal().create_a(r.blog).for_the(r.user):
        the(r.frontend).calls(r.create_blog_api_view)
        with the(r.create_blog_api_view).calls(r.create_blog_action).with_the(
            r.create_blog_form
        ):
            it().calls(r.has_forbidden_words_rule).on_the(r.name).and_the(r.description)
            it().raises(r.forbidden_words_error).if_forbidden_words_are_found()
            it().creates(r.blog)
            it().returns(r.blog)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog")

markdown_node.markdown = """
The frontend creates a new blog for the user through the API of the backend. A blog with forbidden words in its
name or description is refused.

## Diagram

```mermaid
flowchart TD
    request(["The frontend calls the CreateBlogApiView"]) --> check

    subgraph create_blog ["Create a blog for the user"]
        check["Check the name and the description for forbidden words [1]"] --> forbidden{{"Are there forbidden words?"}}:::choice
        forbidden -- yes --> refused["Raise an error"]
        forbidden -- no --> create["Create the blog"]
        create --> returned["Return the blog"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The action checks the form before it creates the blog

The API view calls `create_blog` with the `create_blog_form`.</br>
`create_blog` calls `has_forbidden_words` on the `name` and the `description`. When it finds forbidden words, it
raises `CreateBlogFormContainsForbiddenWordsError`.</br>
"""
