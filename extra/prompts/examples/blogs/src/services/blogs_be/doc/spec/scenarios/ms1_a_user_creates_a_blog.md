[comment]: <> (This file is auto-generated. Do not edit directly.)

# ms1_a_user_creates_a_blog

## A user creates a blog

The frontend calls `CreateBlogApiView` to create a new blog for a user.
The API view delegates to the `create_blog` action, which checks the `name` and `description`
fields for forbidden words before persisting the blog.

### Steps

#### It creates the blog

The frontend calls `CreateBlogApiView`.</br>
The API view calls `create_blog` with the `create_blog_form`.</br>
`create_blog` calls `has_forbidden_words` on the `name` and `description` fields.</br>
If forbidden words are found, `create_blog` raises `CreateBlogFormContainsForbiddenWordsError`.</br>
Otherwise, `create_blog` creates and returns the `blog`.</br>

### Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant CBAV as CreateBlogApiView
    participant CBA as CreateBlog (action)
    participant HFW as HasForbiddenWords (rule)

    Note over Frontend,CBA: Create blog
    Frontend->>CBAV: POST /blogs/
    CBAV->>CBA: create_blog(create_blog_form)
    CBA->>HFW: has_forbidden_words(name)
    HFW-->>CBA: result
    CBA->>HFW: has_forbidden_words(description)
    HFW-->>CBA: result

    alt forbidden words found
        CBA-->>CBAV: raise CreateBlogFormContainsForbiddenWordsError
    else no forbidden words
        CBA->>CBA: create blog
        CBA-->>CBAV: blog
    end
```

