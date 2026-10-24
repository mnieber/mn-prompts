[comment]: <> (This file is auto-generated. Do not edit directly.)

# ms3_a_user_edits_and_deletes_a_blog_post

## A user edits and deletes a blog post

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

