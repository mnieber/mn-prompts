import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_user_updates_a_blog_post")


def run_scenario():
    r.user = c.External.Actors.User
    r.blogs_page = c.Blogs.Views.BlogsPage
    r.blog_post_form_view = c.Blogs.Views.BlogPostFormView
    r.update_blog_post_mutation = c.Blogs.Mutations.UpdateBlogPost
    r.delete_blog_posts_mutation = c.Blogs.Mutations.DeleteBlogPosts

    with goal().edit_a(r.blog_post).in_the(r.blog):
        the(r.user).selects_the(r.blog_post).they_want_to_edit()
        the(r.blogs_page).shows(r.edit_blog_post_button)
        the(r.user).presses(r.edit_blog_post_button)
        the(r.user).submits(r.blog_post_form)
        with the(r.blog_post_form_view).calls(r.update_blog_post_mutation).with_the(r.blog_post_form_data):
            it().updates(r.blog_post)
            it().returns(r.blog_post)

    with goal().delete_some(r.blog_posts).in_the(r.blog):
        the(r.user).selects_the(r.blog_posts).they_want_to_delete()
        the(r.blogs_page).shows(r.delete_blog_posts_button)
        the(r.user).presses(r.delete_blog_posts_button)
        with the(r.blogs_page).calls(r.delete_blog_posts_mutation).with_the(r.blog_posts):
            it().deletes(r.blog_posts)


markdown_node = sunya.add_markdown_node(
    scenario, "A user updates and deletes a blog post"
)

markdown_node.markdown = """
The user updates or deletes the blog posts that they select in a blog.

## Diagram

```mermaid
flowchart TD
    select_post(["The user selects the blog post they want to edit"]) --> edit_button

    subgraph edit_blog_post ["Edit a blog post in the blog"]
        edit_button["Show the edit-blog-post button in the BlogsPage"] --> press_edit["The user presses the edit-blog-post button"]
        press_edit --> form["The user updates and submits the blog-post form"]
        form --> update["Update the blog post [1]"]
    end

    select_posts(["The user selects the blog posts they want to delete"]) --> delete_button

    subgraph delete_blog_posts ["Delete some blog posts in the blog"]
        delete_button["Show the delete-blog-posts button in the BlogsPage"] --> press_delete["The user presses the delete-blog-posts button"]
        press_delete --> delete_posts["Delete the blog posts [2]"]
    end
```

### Footnotes

#### [1] - The BlogPostFormView updates the blog post with a mutation

`BlogPostFormView` calls `UpdateBlogPost` with the blog-post form data. `UpdateBlogPost` updates and returns the
blog post.</br>

#### [2] - The BlogsPage deletes the selected blog posts with a mutation

`BlogsPage` calls `DeleteBlogPosts` with the selected blog posts, which deletes them.</br>
"""
