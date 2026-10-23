import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario(f"ms1_a_user_creates_a_book")


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
A user creates a book with lorem ipsum text by calling the `create_book` action with a form.
The action creates the book, then creates chapters (3 times) each with their paragraphs.
Each paragraph is filtered to have at most N bad words (words containing 'a' or 'b' after
stripping the "aaa" prefix) using the `is_bad_word` rule.

### Steps

#### It creates the book

The user calls `create_book` with the `create_book_form`.</br>
`create_book` creates the `book`.</br>

#### It creates chapters and paragraphs

For each chapter (3 times), `create_book` calls `create_chapter` with the `create_chapter_form`.</br>
`create_chapter` creates the `chapter`, then for each paragraph calls `create_paragraph`.</br>
`create_paragraph` creates a paragraph with lorem ipsum text, filters it to have at most N bad
words using the `is_bad_word` rule, and adds the accepted paragraph to the chapter.</br>
Each chapter is added to the book.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant CreateBook as CreateBook (action)
    participant CreateChapter as CreateChapter (action)
    participant CreateParagraph as CreateParagraph (action)
    participant IsBadWord as IsBadWord (rule)

    Note over User,CreateBook: Create book
    User->>CreateBook: create_book(create_book_form)
    CreateBook->>CreateBook: create book

    loop for each chapter (3 times)
        Note over CreateBook,CreateChapter: Create chapter
        CreateBook->>CreateChapter: create_chapter(create_chapter_form)
        CreateChapter->>CreateChapter: create chapter

        loop for each paragraph
            Note over CreateChapter,IsBadWord: Create paragraph
            CreateChapter->>CreateParagraph: create_paragraph()
            CreateParagraph->>CreateParagraph: create paragraph with lorem ipsum text
            CreateParagraph->>CreateParagraph: filter paragraph to have at most N bad_words
            loop for each word
                CreateParagraph->>IsBadWord: is_bad_word(word)
                IsBadWord-->>CreateParagraph: true / false
            end
            CreateParagraph->>CreateChapter: paragraph
        end

        CreateChapter->>CreateChapter: add chapter to book
        CreateChapter-->>CreateBook: chapter
    end

    CreateBook-->>User: book
```
"""
