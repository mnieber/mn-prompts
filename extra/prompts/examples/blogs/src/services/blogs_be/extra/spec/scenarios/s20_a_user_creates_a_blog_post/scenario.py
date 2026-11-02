import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s20_a_user_creates_a_blog_post")


def run_scenario():
    r.frontend = c.External.Actors.Frontend
    r.create_blog_post_api_view = c.Blogs.ApiViews.CreateBlogPostApiView
    r.create_blog_post_action = c.Blogs.Actions.CreateBlogPost
    r.has_forbidden_words_rule = c.Blogs.Rules.HasForbiddenWords

    with goal().create_a(r.blog_post).in_the(r.blog):
        the(r.frontend).calls(r.create_blog_post_api_view)
        with the(r.create_blog_post_api_view).calls(r.create_blog_post_action).with_the(r.create_blog_post_form):
            it().calls(r.has_forbidden_words_rule).on_the(r.title).and_the(r.content)
            it().raises(r.forbidden_words_error).if_forbidden_words_are_found()
            it().creates(r.blog_post)
            it().returns(r.blog_post)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog post")

markdown_node.markdown = """
The frontend calls `CreateBlogPostApiView` to create a new blog post within a blog.
The API view delegates to the `create_blog_post` action, which checks the `title` and `content`
fields for forbidden words before persisting the post.

### Steps

#### It creates the blog post

The frontend calls `CreateBlogPostApiView`.</br>
The API view calls `create_blog_post` with the `create_blog_post_form`.</br>
`create_blog_post` calls `has_forbidden_words` on the `title` and `content` fields.</br>
If forbidden words are found, `create_blog_post` raises `CreateBlogPostFormContainsForbiddenWordsError`.</br>
Otherwise, `create_blog_post` creates and returns the `blog_post`.</br>

### Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant CBPAV as CreateBlogPostApiView
    participant CBPA as CreateBlogPost (action)
    participant HFW as HasForbiddenWords (rule)

    Note over Frontend,CBPA: Create blog post
    Frontend->>CBPAV: POST /blogs/{blog_id}/posts/
    CBPAV->>CBPA: create_blog_post(create_blog_post_form)
    CBPA->>HFW: has_forbidden_words(title)
    HFW-->>CBPA: result
    CBPA->>HFW: has_forbidden_words(content)
    HFW-->>CBPA: result

    alt forbidden words found
        CBPA-->>CBPAV: raise CreateBlogPostFormContainsForbiddenWordsError
    else no forbidden words
        CBPA->>CBPA: create blog_post
        CBPA-->>CBPAV: blog_post
    end
```
"""
