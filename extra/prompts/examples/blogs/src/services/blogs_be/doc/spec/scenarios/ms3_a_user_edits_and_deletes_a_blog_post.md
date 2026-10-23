[comment]: <> (This file is auto-generated. Do not edit directly.)

# Scenario: ms3_a_user_edits_and_deletes_a_blog_post

## A user edits and deletes a blog post

```mermaid
sequenceDiagram
    participant Frontend as Frontend
    participant UpdateBlogPostApiView as UpdateBlogPost<br/>ApiView
    participant UpdateBlogPostAction as UpdateBlogPost<br/>Action
    participant HasForbiddenWordsRule as HasForbiddenWords<br/>Rule
    participant DeleteBlogPostsApiView as DeleteBlogPosts<br/>ApiView
    participant DeleteBlogPostsAction as DeleteBlogPosts<br/>Action

    # 🔳 Edit Blog Post
    note over Frontend: edit a blog_post in the blog
    Frontend -->> UpdateBlogPostApiView: calls()
    UpdateBlogPostApiView -->> UpdateBlogPostAction: calls(update_blog_post_form)
    UpdateBlogPostAction -->> HasForbiddenWordsRule: runs blog_post
    HasForbiddenWordsRule -->> UpdateBlogPostAction: returns()
    UpdateBlogPostAction -->> UpdateBlogPostAction: updates blog_post
    UpdateBlogPostAction -->> UpdateBlogPostApiView: returns(blog_post)

    # 🔳 Delete Blog Posts
    note over Frontend: delete some blog_posts in the blog
    Frontend -->> DeleteBlogPostsApiView: calls()
    DeleteBlogPostsApiView -->> DeleteBlogPostsAction: calls(blog_posts)
    DeleteBlogPostsAction -->> DeleteBlogPostsAction: deletes blog_posts
    DeleteBlogPostsAction -->> DeleteBlogPostsApiView: returns()
```

**Legend:**

- Frontend → External.Actors.Frontend
- UpdateBlogPostApiView → Blogs.ApiViews.UpdateBlogPostApiView
- UpdateBlogPostAction → Blogs.Actions.UpdateBlogPost
- HasForbiddenWordsRule → Blogs.Rules.HasForbiddenWords
- DeleteBlogPostsApiView → Blogs.ApiViews.DeleteBlogPostsApiView
- DeleteBlogPostsAction → Blogs.Actions.DeleteBlogPosts

