[comment]: <> (This file is auto-generated. Do not edit directly.)

# s10_a_user_creates_a_blog

## A user creates a blog

The frontend creates a new blog for the user through the API of the backend. A blog with forbidden words in its
name or description is refused.

## Diagram

```mermaid
flowchart TD
    request(["The frontend calls the CreateBlogApiView"]) --> check

    subgraph create_blog ["Create a blog for the user"]
        check["Check the name and the description for forbidden words [1]"] --> forbidden{{"Are there forbidden words?"}}:::choice
        forbidden -- yes --> refused["Raise an error"]
        forbidden -- no --> create["Create the blog"]
        create --> returned["Return the blog"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The action checks the form before it creates the blog

The API view calls `create_blog` with the `create_blog_form`.</br>
`create_blog` calls `has_forbidden_words` on the `name` and the `description`. When it finds forbidden words, it
raises `CreateBlogFormContainsForbiddenWordsError`.</br>

