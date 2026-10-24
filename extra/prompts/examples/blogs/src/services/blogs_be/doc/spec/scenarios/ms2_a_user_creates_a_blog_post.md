[comment]: <> (This file is auto-generated. Do not edit directly.)

# ms2_a_user_creates_a_blog_post

## A user creates a blog post

The frontend calls `CreateBlogPostApiView` to create a new blog post within a blog.
The API view delegates to the `create_blog_post` action, which checks the `title` and `content`
fields for forbidden words before persisting the post.

### Steps

#### It creates the blog post

The frontend calls `CreateBlogPostApiView`.</br>
The API view calls `create_blog_post` with the `create_blog_post_form`.</br>
`create_blog_post` calls `has_forbidden_words` on the `title` and `content` fields.</br>
If forbidden words are found, `create_blog_post` raises `CreateBlogPostFormContainsForbiddenWordsError`.</br>
Otherwise, `create_blog_post` creates and returns the `blog_post`.</br>

### Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant CBPAV as CreateBlogPostApiView
    participant CBPA as CreateBlogPost (action)
    participant HFW as HasForbiddenWords (rule)

    Note over Frontend,CBPA: Create blog post
    Frontend->>CBPAV: POST /blogs/{blog_id}/posts/
    CBPAV->>CBPA: create_blog_post(create_blog_post_form)
    CBPA->>HFW: has_forbidden_words(title)
    HFW-->>CBPA: result
    CBPA->>HFW: has_forbidden_words(content)
    HFW-->>CBPA: result

    alt forbidden words found
        CBPA-->>CBPAV: raise CreateBlogPostFormContainsForbiddenWordsError
    else no forbidden words
        CBPA->>CBPA: create blog_post
        CBPA-->>CBPAV: blog_post
    end
```

