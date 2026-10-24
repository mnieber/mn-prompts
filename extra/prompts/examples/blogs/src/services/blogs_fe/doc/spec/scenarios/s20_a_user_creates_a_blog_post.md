[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: s20_a_user_creates_a_blog_post

## A user creates a blog post

```mermaid
sequenceDiagram
    participant User as User
    participant BlogListView as BlogListView
    participant BlogView as BlogView
    participant BlogPostFormView as BlogPostFormView
    participant CreateBlogPostMutation as CreateBlogPostMutation

    # 🔳 Create Blog Post
    note over User: create a blog_post in the blog
    User ->> BlogListView: visits the blogs_route
    User ->> BlogView: clicks on a blog to visit the blog_route
    BlogView -->> User: shows create_blog_post_button
    User ->> BlogPostFormView: presses create_blog_post_button
    User -->> BlogPostFormView: submits blog_post_form
    BlogPostFormView -->> CreateBlogPostMutation: calls(blog_post_form_data)
    CreateBlogPostMutation -->> CreateBlogPostMutation: creates(blog_post)
    CreateBlogPostMutation -->> BlogPostFormView: returns(blog_post)
```

**Legend:**

- User → External.Actors.User
- BlogListView → Blogs.Views.BlogListView
- BlogView → Blogs.Views.BlogView
- BlogPostFormView → Blogs.Views.BlogPostFormView
- CreateBlogPostMutation → Blogs.Mutations.CreateBlogPostMutation

