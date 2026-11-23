import sunya

scenario = sunya.add_scenario("s20_a_user_exports_a_book")

markdown_node = sunya.add_markdown_node(scenario, "A user exports a book")

markdown_node.markdown = """
A user exports the book that Bookie creates to a file, so that they can read it in another program. Bookie writes
the book in Markdown or as plain text, and never overwrites a file without asking.

## Diagram

```mermaid
flowchart TD
    start(["The user creates a book with --export"]) --> create["Create the book"]

    subgraph render ["Render the book"]
        create --> format{{"Which format did the user choose? [1]"}}:::choice
        format -- markdown --> markdown["Render the chapters as Markdown sections"]
        format -- text --> text["Render the chapters as plain text"]
    end

    markdown --> exists
    text --> exists

    subgraph export ["Write the export file"]
        exists{{"Does the file exist? [2]"}}:::choice
        exists -- no --> write["Write the file"]
        exists -- yes --> confirm{{"Does the user confirm?"}}:::choice
        confirm -- yes --> write
        confirm -- no --> skipped["Keep the existing file"]
    end

    write --> report["Print the path of the file"]

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The format follows the extension

The user chooses the format with the extension of the file (`.md` or `.txt`).</br>

#### [2] - An existing file is never overwritten silently

Bookie asks before it overwrites a file.</br>

## Design notes (to be dropped)

### 1. Alice exports a book to Markdown

Groups: "Render the book", "Write the export file".

1. Alice runs `bookie create-book --title "The Lorem Book" --export the_lorem_book.md`. Bookie creates the book, and
   writes it to `the_lorem_book.md`: the title as a `#` heading, and each chapter as a `##` section with its
   paragraphs.
   - Detail: without a path (`--export` alone), the file name is the title of the book in snake case, with the
     `.md` extension.
   - Edge-case: an unknown extension (e.g. `.pdf`) fails before the book is created, with "Bookie can only export
     to .md or .txt".
2. Bookie prints the path of the file after the summary of the book.

### 2. Alice exports a book that was exported before

Groups: "Write the export file".

1. Alice exports "The Lorem Book" again. Bookie asks whether it should overwrite `the_lorem_book.md`, and Alice
   confirms.
   - Edge-case: with `--yes`, Bookie overwrites the file without asking.
   - Edge-case: when Alice doesn't confirm, the existing file stays, and Bookie prints "The book was not
     exported".

### 3. Bob exports a book as plain text

Groups: "Render the book".

1. Bob exports a book to `book.txt`. The chapter titles are underlined with `=`, and the paragraphs are wrapped at
   80 characters.
   - Detail: the title style of the chapters (see the chapter title styles) is kept in both formats.

### Decisions

- The format follows the extension of the file (the user's choice). Alternative: a `--format` option.
- An existing file is only overwritten after a confirmation, or with `--yes`. Alternative: add a number to the file
  name.
- Export is an option of `create-book`, since Bookie doesn't store books. Alternative: store the books, and add an
  `export-book` command.
- Open: can a user export a single chapter? Proposal: no, only whole books.
"""
