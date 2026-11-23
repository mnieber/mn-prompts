import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s10_a_user_creates_a_book")


def run_scenario():
    r.user = c.External.Actors.User
    r.create_book_action = c.Books.Actions.CreateBook
    r.create_chapter_action = c.Chapters.Actions.CreateChapter
    r.create_paragraph_action = c.Chapters.Actions.CreateParagraph
    r.is_bad_word_rule = c.Chapters.Rules.IsBadWord

    with goal().create_a(r.book).with_lorem_ipsum_text():

        # Create the book
        with the(r.user).calls(r.create_book_action).with_the(r.create_book_form):
            it().creates(r.book)

        # Create chapters
        with the(r.create_book_action).creates_chapters_for(r.book):
            with the(r.create_book_action).calls(r.create_chapter_action).with_the(r.create_chapter_form):
                it().creates(r.chapter)

                # Create paragraphs
                with the(r.create_chapter_action).creates_paragraphs_for(r.chapter):
                    with the(r.create_chapter_action).calls(r.create_paragraph_action):
                        it().creates(r.paragraph).with_lorem_ipsum_text()
                        it().filters(r.paragraph).to_have_at_most_N(r.bad_words)
                        it().calls(r.is_bad_word_rule).for_each_word()
                        it().adds(r.paragraph).to(r.chapter)

                it().adds(r.chapter).to(r.book)

        the(r.create_book_action).returns(r.book).to(r.user)


markdown_node = sunya.add_markdown_node(scenario, "A user creates a book")

markdown_node.markdown = """
A user creates a book with lorem ipsum text. The book has 3 chapters, and each chapter has paragraphs with at most N
bad words.

## Diagram

```mermaid
flowchart TD
    create(["The user calls create_book with the create_book_form"]) --> book

    subgraph create_book ["Create a book with lorem ipsum text"]
        book["Create the book"] --> chapter["Create a chapter [1]"]
        chapter --> paragraph["Create a paragraph with lorem ipsum text"]
        paragraph --> filter["Filter the paragraph to have at most N bad words [2]"]
        filter --> add_paragraph["Add the paragraph to the chapter"]
        add_paragraph --> more_paragraphs{{"Are there more paragraphs?"}}:::choice
        more_paragraphs -- yes --> paragraph
        more_paragraphs -- no --> add_chapter["Add the chapter to the book"]
        add_chapter --> all_chapters{{"Are there 3 chapters?"}}:::choice
        all_chapters -- no --> chapter
        all_chapters -- yes --> returned["Return the book"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - create_book delegates to the chapter actions

`create_book` calls `create_chapter` with the `create_chapter_form` for each chapter. `create_chapter` calls
`create_paragraph` for each paragraph.</br>

#### [2] - A bad word contains an 'a' or a 'b'

`create_paragraph` calls the `is_bad_word` rule for each word. A word is bad when it contains an 'a' or a 'b' after
stripping the "aaa" prefix.</br>
"""
