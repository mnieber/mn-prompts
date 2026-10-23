[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: ms2_a_user_creates_a_blog_post

## A user creates a blog post

```mermaid
sequenceDiagram
    participant Frontend as Frontend
    participant CreateBlogPostApiView as CreateBlogPost<br/>ApiView
    participant CreateBlogPostAction as CreateBlogPost<br/>Action
    participant HasForbiddenWordsRule as HasForbiddenWords<br/>Rule

    # 🔳 Create Blog Post
    note over Frontend: create a blog_post in the blog
    Frontend -->> CreateBlogPostApiView: calls()
    CreateBlogPostApiView -->> CreateBlogPostAction: calls(create_blog_post_form)
    CreateBlogPostAction -->> HasForbiddenWordsRule: runs blog_post
    HasForbiddenWordsRule -->> CreateBlogPostAction: returns()
    CreateBlogPostAction -->> CreateBlogPostAction: creates(blog_post)
    CreateBlogPostAction -->> CreateBlogPostApiView: returns(blog_post)
```

**Legend:**

- Frontend → External.Actors.Frontend
- CreateBlogPostApiView → Blogs.ApiViews.CreateBlogPostApiView
- CreateBlogPostAction → Blogs.Actions.CreateBlogPost
- HasForbiddenWordsRule → Blogs.Rules.HasForbiddenWords

