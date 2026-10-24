[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: s10_a_user_creates_a_blog

## A user creates a blog

```mermaid
sequenceDiagram
    participant User as User
    participant BlogListView as BlogListView
    participant BlogFormView as BlogFormView
    participant CreateBlogMutation as CreateBlogMutation

    # 🔳 Create Blog
    note over User: create a blog for the user
    User ->> BlogListView: visits the blogs_route
    BlogListView -->> User: shows create_blog_button
    User ->> BlogFormView: presses create_blog_button
    User -->> BlogFormView: submits blog_form
    BlogFormView -->> CreateBlogMutation: calls(blog_form_data)
    CreateBlogMutation -->> CreateBlogMutation: creates(blog)
    CreateBlogMutation -->> BlogFormView: returns(blog)
```

**Legend:**

- User → External.Actors.User
- BlogListView → Blogs.Views.BlogListView
- BlogFormView → Blogs.Views.BlogFormView
- CreateBlogMutation → Blogs.Mutations.CreateBlogMutation

