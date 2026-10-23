import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("ms1_a_user_creates_a_blog")


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
The frontend calls `CreateBlogApiView` to create a new blog for a user.
The API view delegates to the `create_blog` action, which checks the `name` and `description`
fields for forbidden words before persisting the blog.

### Steps

#### It creates the blog

The frontend calls `CreateBlogApiView`.</br>
The API view calls `create_blog` with the `create_blog_form`.</br>
`create_blog` calls `has_forbidden_words` on the `name` and `description` fields.</br>
If forbidden words are found, `create_blog` raises `CreateBlogFormContainsForbiddenWordsError`.</br>
Otherwise, `create_blog` creates and returns the `blog`.</br>

### Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant CBAV as CreateBlogApiView
    participant CBA as CreateBlog (action)
    participant HFW as HasForbiddenWords (rule)

    Note over Frontend,CBA: Create blog
    Frontend->>CBAV: POST /blogs/
    CBAV->>CBA: create_blog(create_blog_form)
    CBA->>HFW: has_forbidden_words(name)
    HFW-->>CBA: result
    CBA->>HFW: has_forbidden_words(description)
    HFW-->>CBA: result

    alt forbidden words found
        CBA-->>CBAV: raise CreateBlogFormContainsForbiddenWordsError
    else no forbidden words
        CBA->>CBA: create blog
        CBA-->>CBAV: blog
    end
```
"""
