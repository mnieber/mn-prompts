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
The frontend can update or delete blog posts. Updating checks the `title` and `content`
fields for forbidden words and raises an error if any are found. Deleting removes the
selected posts directly.

### Steps

#### It edits a blog post

The frontend calls `UpdateBlogPostApiView`.</br>
The API view calls `update_blog_post` with the `update_blog_post_form`.</br>
`update_blog_post` calls `has_forbidden_words` on the `title` and `content` fields.</br>
If forbidden words are found, `update_blog_post` raises `UpdateBlogPostFormContainsForbiddenWordsError`.</br>
Otherwise, `update_blog_post` updates and returns the `blog_post`.</br>

#### It deletes blog posts

The frontend calls `DeleteBlogPostsApiView`.</br>
The API view calls `delete_blog_posts` with the `delete_blog_posts_form`.</br>
`delete_blog_posts` deletes the posts.</br>

### Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant UBPAV as UpdateBlogPostApiView
    participant UBPA as UpdateBlogPost (action)
    participant HFW as HasForbiddenWords (rule)
    participant DBPAV as DeleteBlogPostsApiView
    participant DBPA as DeleteBlogPosts (action)

    Note over Frontend,UBPA: Edit blog post
    Frontend->>UBPAV: PATCH /blogs/{blog_id}/posts/{post_id}/
    UBPAV->>UBPA: update_blog_post(update_blog_post_form)
    UBPA->>HFW: has_forbidden_words(title)
    HFW-->>UBPA: result
    UBPA->>HFW: has_forbidden_words(content)
    HFW-->>UBPA: result

    alt forbidden words found
        UBPA-->>UBPAV: raise UpdateBlogPostFormContainsForbiddenWordsError
    else no forbidden words
        UBPA->>UBPA: update blog_post
        UBPA-->>UBPAV: blog_post
    end

    Note over Frontend,DBPA: Delete blog posts
    Frontend->>DBPAV: DELETE /blogs/{blog_id}/posts/
    DBPAV->>DBPA: delete_blog_posts(delete_blog_posts_form)
    DBPA->>DBPA: delete blog_posts
    DBPA-->>DBPAV: (done)
```
"""
