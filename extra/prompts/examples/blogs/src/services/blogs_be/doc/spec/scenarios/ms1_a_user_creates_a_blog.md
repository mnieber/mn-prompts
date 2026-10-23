[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: ms1_a_user_creates_a_blog

## A user creates a blog

```mermaid
sequenceDiagram
    participant Frontend as Frontend
    participant CreateBlogApiView as CreateBlog<br/>ApiView
    participant CreateBlogAction as CreateBlog<br/>Action
    participant HasForbiddenWordsRule as HasForbiddenWords<br/>Rule

    # 🔳 Create Blog
    note over Frontend: create a blog for the user
    Frontend -->> CreateBlogApiView: calls()
    CreateBlogApiView -->> CreateBlogAction: calls(create_blog_form)
    CreateBlogAction -->> HasForbiddenWordsRule: calls()
    HasForbiddenWordsRule -->> CreateBlogAction: returns()
    opt No forbidden words found
    CreateBlogAction -->> CreateBlogAction: creates(blog)
    end
    CreateBlogAction -->> CreateBlogApiView: returns(blog)

```

**Legend:**

- Frontend → External.Actors.Frontend
- CreateBlogApiView → Blogs.ApiViews.CreateBlogApiView
- CreateBlogAction → Blogs.Actions.CreateBlog
- HasForbiddenWordsRule → Blogs.Rules.HasForbiddenWords

