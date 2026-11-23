[comment]: <> (This file is auto-generated. Do not edit directly.)

# s20_a_user_creates_a_blog_post

## A user creates a blog post

The frontend creates a new blog post in a blog through the API of the backend. A blog post with forbidden words in
its title or content is refused.

## Diagram

```mermaid
flowchart TD
    request(["The frontend calls the CreateBlogPostApiView"]) --> check

    subgraph create_blog_post ["Create a blog post in the blog"]
        check["Check the title and the content for forbidden words [1]"] --> forbidden{{"Are there forbidden words?"}}:::choice
        forbidden -- yes --> refused["Raise an error"]
        forbidden -- no --> create["Create the blog post"]
        create --> returned["Return the blog post"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The action checks the form before it creates the blog post

The API view calls `create_blog_post` with the `create_blog_post_form`.</br>
`create_blog_post` calls `has_forbidden_words` on the `title` and the `content`. When it finds forbidden words, it
raises `CreateBlogPostFormContainsForbiddenWordsError`.</br>

