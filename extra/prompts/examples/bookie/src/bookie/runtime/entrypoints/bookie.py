import argparse
import logging
import sys
import traceback

from bookie.books.actions.create_book import create_book, CreateBookForm

logger = logging.getLogger(__name__)


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Bookie - A tool for creating books with lorem ipsum text"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True

    # Create book command
    create_book_parser = subparsers.add_parser("create-book", help="Create a new book")
    create_book_parser.add_argument("--title", required=True, help="Title of the book")
    create_book_parser.add_argument(
        "--chapters", type=int, default=3, help="Number of chapters to create"
    )
    create_book_parser.add_argument(
        "--paragraphs", type=int, default=5, help="Number of paragraphs per chapter"
    )

    # Global arguments
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )

    return parser.parse_args(argv)


def _setup_logging(verbosity):
    log_level = logging.WARNING
    if verbosity >= 2:
        log_level = logging.DEBUG
    elif verbosity >= 1:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


def _print_book(book):
    print(f"Created book: {book.title}")
    print(f"Number of chapters: {len(book.chapters)}")
    for i, chapter in enumerate(book.chapters, 1):
        print(f"  Chapter {i}: {chapter.title}")
        print(f"    Paragraphs: {len(chapter.paragraphs)}")


def run(argv=None):
    args = _parse_args(argv)
    _setup_logging(args.verbose)

    if args.command == "create-book":
        logger.info(f"Creating book with title: {args.title}")

        # Prepare the create_book_form
        create_book_form = CreateBookForm(title=args.title, num_chapters=args.chapters)

        book = create_book(
            create_book_form=create_book_form,
            paragraphs_per_chapter=args.paragraphs,
        )

        _print_book(book)
        logger.info("Book creation completed successfully")

    return 0


def main(argv=None):
    # Runs the tool for the user: errors are printed instead of raised
    try:
        return run(argv)
    except Exception as error:
        args = sys.argv[1:] if argv is None else argv
        verbose = any(arg.startswith("-v") or arg == "--verbose" for arg in args)
        if verbose:
            traceback.print_exc()
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        if not verbose:
            print("Hint: run with -v to see the traceback.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
