# Writing scenarios with a sequence diagram

`RULE`: only use this format when I ask for it. By default, the markdown section of a scenario has a flow chart
(see the `app-write-specs` skill).

This skill replaces the markdown section of the `app-write-specs` skill. Everything else in that skill (the
`run_scenario` function, the sunya DSL, the layout of the spec directory and the numbering) stays the same.

## The markdown section

`RULE:` The markdown section starts with a short description that should not duplicate the details that are already described in the steps. Avoid explaining the steps in the introduction and then explaining them again in the Steps section.

`RULE:` Don't insert cross-references to other scenarios, as these go stale quickly. Instead, assume that the reader will find the related scenarios on their own.

The markdown section has a **Steps** and a **Diagram** subsection, in this fixed structure:

````
A short description of the scenario.

### Steps

#### It does X

Step description.</br>

#### It does Y

Step description.</br>

### Diagram

\```mermaid
sequenceDiagram
    ...
\```
````

- There is one `####` section in Steps per goal of `run_scenario`, named "It <does the goal>".
- Each sentence (or group of related sentences) of a step description ends with `</br>`.
- The diagram has a participant per actor and code-unit, with its kind in the label (e.g.
  `participant CBA as CreateBlog (action)`).
- Each goal starts with a `Note over` that names it. Use `alt`/`else` for choices, `opt` for optional steps and
  `loop` for repeated steps.

## Example

```python
markdown_node = sunya.add_markdown_node(scenario, "A user creates a blog")

markdown_node.markdown = """
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

\```mermaid
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
\```
"""
```
