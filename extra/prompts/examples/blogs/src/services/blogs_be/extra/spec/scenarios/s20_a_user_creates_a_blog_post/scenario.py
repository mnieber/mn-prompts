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
The frontend creates a new blog post in a blog through the API of the backend. A blog post with forbidden words in
its title or content is refused.

## Diagram

```mermaid
flowchart TD
    request(["The frontend calls the CreateBlogPostApiView"]) --> check

    subgraph create_blog_post ["Create a blog post in the blog"]
        check["Check the title and the content for forbidden words [1]"] --> forbidden{{"Are there forbidden words?"}}:::choice
        forbidden -- yes --> refused["Raise an error"]
        forbidden -- no --> create["Create the blog post"]
        create --> returned["Return the blog post"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The action checks the form before it creates the blog post

The API view calls `create_blog_post` with the `create_blog_post_form`.</br>
`create_blog_post` calls `has_forbidden_words` on the `title` and the `content`. When it finds forbidden words, it
raises `CreateBlogPostFormContainsForbiddenWordsError`.</br>
"""
