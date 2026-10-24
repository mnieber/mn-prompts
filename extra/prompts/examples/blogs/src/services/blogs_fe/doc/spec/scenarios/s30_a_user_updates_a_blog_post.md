[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: s30_a_user_updates_a_blog_post

## A user updates and deletes a blog post

```mermaid
sequenceDiagram
    participant User as User
    participant BlogView as BlogView
    participant BlogPostFormView as BlogPostFormView
    participant UpdateBlogPostMutation as UpdateBlogPostMutation
    participant DeleteBlogPostsMutation as DeleteBlogPostsMutation

    # 🔳 Edit Blog Post
    note over User: edit a blog_post in the blog
    User -->> BlogView: selects the blog_post they want to edit
    BlogView -->> User: shows edit_blog_post_button
    User ->> BlogPostFormView: presses edit_blog_post_button
    User -->> BlogPostFormView: submits blog_post_form
    BlogPostFormView -->> UpdateBlogPostMutation: calls(blog_post_form_data)
    UpdateBlogPostMutation -->> UpdateBlogPostMutation: updates blog_post
    UpdateBlogPostMutation -->> BlogPostFormView: returns(blog_post)

    # 🔳 Delete Blog Post
    note over User: delete a blog_post in the blog
    User -->> BlogView: selects the blog_post they want to delete
    BlogView -->> User: shows delete_blog_posts_button
    User -->> BlogView: presses delete_blog_posts_button
    BlogView -->> DeleteBlogPostsMutation: calls(blog_posts)
    DeleteBlogPostsMutation -->> DeleteBlogPostsMutation: deletes blog_posts
    DeleteBlogPostsMutation -->> BlogView: returns()
```

**Legend:**

- User → External.Actors.User
- BlogView → Blogs.Views.BlogView
- BlogPostFormView → Blogs.Views.BlogPostFormView
- UpdateBlogPostMutation → Blogs.Mutations.UpdateBlogPostMutation
- DeleteBlogPostsMutation → Blogs.Mutations.DeleteBlogPostsMutation

