import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_user_edits_and_deletes_a_blog_post")


def run_scenario():
    r.frontend = c.External.Actors.Frontend
    r.update_blog_post_api_view = c.Blogs.ApiViews.UpdateBlogPostApiView
    r.update_blog_post_action = c.Blogs.Actions.UpdateBlogPost
    r.has_forbidden_words_rule = c.Blogs.Rules.HasForbiddenWords
    r.delete_blog_posts_api_view = c.Blogs.ApiViews.DeleteBlogPostsApiView
    r.delete_blog_posts_action = c.Blogs.Actions.DeleteBlogPosts

    with goal().edit_a(r.blog_post).in_the(r.blog):
        the(r.frontend).calls(r.update_blog_post_api_view)
        with the(r.update_blog_post_api_view).calls(r.update_blog_post_action).with_the(r.update_blog_post_form):
            it().calls(r.has_forbidden_words_rule).on_the(r.title).and_the(r.content)
            it().raises(r.forbidden_words_error).if_forbidden_words_are_found()
            it().updates(r.blog_post)
            it().returns(r.blog_post)

    with goal().delete_some(r.blog_posts).in_the(r.blog):
        the(r.frontend).calls(r.delete_blog_posts_api_view)
        with the(r.delete_blog_posts_api_view).calls(r.delete_blog_posts_action).with_the(r.delete_blog_posts_form):
            it().deletes(r.blog_posts)


markdown_node = sunya.add_markdown_node(
    scenario, "A user edits and deletes a blog post"
)

markdown_node.markdown = """
The frontend updates or deletes blog posts through the API of the backend. An update with forbidden words in the
title or content is refused.

## Diagram

```mermaid
flowchart TD
    update_request(["The frontend calls the UpdateBlogPostApiView"]) --> check

    subgraph edit_blog_post ["Edit a blog post in the blog"]
        check["Check the title and the content for forbidden words [1]"] --> forbidden{{"Are there forbidden words?"}}:::choice
        forbidden -- yes --> refused["Raise an error"]
        forbidden -- no --> update["Update the blog post"]
        update --> returned["Return the blog post"]
    end

    delete_request(["The frontend calls the DeleteBlogPostsApiView"]) --> delete_posts

    subgraph delete_blog_posts ["Delete some blog posts in the blog"]
        delete_posts["Delete the blog posts [2]"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The action checks the form before it updates the blog post

The API view calls `update_blog_post` with the `update_blog_post_form`.</br>
`update_blog_post` calls `has_forbidden_words` on the `title` and the `content`. When it finds forbidden words, it
raises `UpdateBlogPostFormContainsForbiddenWordsError`.</br>

#### [2] - The blog posts are deleted without a check

The API view calls `delete_blog_posts` with the `delete_blog_posts_form`, which deletes the selected posts.</br>
"""
