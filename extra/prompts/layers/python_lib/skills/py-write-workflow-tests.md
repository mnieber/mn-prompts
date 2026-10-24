# Skill: py-write-workflow-tests

Applies when writing (or converting) tests. In the workflow-test style, a developer can read a test top to bottom,
like a story, and understand how the tool is used: the starting situation, what the user does, and what should
happen as a result.

---

## Kinds of tests

- **Workflow tests** explain the main workflows of a feature (the happy paths, and the scenarios of the specs).
  They live in `tests/<feature>_tests/test_<feature>/`.
- **Impl tests** cover edge cases and implementation details (error handling, validation, corner cases of a
  workflow). They live in `tests/<feature>_tests/test_<feature>_impl/`.
- **Unit tests** of small, pure pieces (e.g. a parser) may stay plain unit tests.

Rules of thumb:

- One workflow per test. When a workflow is finished, the next one starts in a new test.
- Many independent edge cases are split by theme into a handful of impl tests, not one test per assert and not
  one giant test. Within a test, later steps may change the same environment and check again.
- Every test is self-contained: it builds its own environment.

## File layout

```
tests/
  conftest.py                        ← ENABLED_TEST_PACKAGES (see below)
  <feature>_tests/
    __init__.py
    conftest.py                      ← the context fixture
    <feature>_test_env.py            ← the shared Env base class of the feature
    test_<feature>/
      test_<scenario_name>.py        ← one test function per file, named after the scenario
    test_<feature>_impl/
      test_<edge_case_theme>.py
```

- The test subdirectories have no `__init__.py` (the feature package has one). Import shared modules with an
  absolute import (`from books_tests.books_test_env import Context, TestEnv`). Never import from another test
  file.
- `tests/conftest.py` lists the enabled test packages in `ENABLED_TEST_PACKAGES`, in the order in which the code is
  implemented, and ignores the others (`collect_ignore`). Tests may be written before the code exists: the
  package is enabled when its code is written.

## Anatomy of a test

```python
from books_tests.books_test_env import Context, TestEnv

from bookie.books.actions.create_book import TooManyChaptersError

TITLE = "The Hobbit"


def create_env(context: Context):
    return Env(context)


def test_bookie_create_book_refuses_too_many_chapters(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have a library with the book The Hobbit.
    if env.step(
        env.create_library(),
        env.run_bookie("create-book", f"--title={TITLE}"),
        env.load_book(TITLE),
    ):
        assert env.book.chapters == []

    # We add 11 chapters to the book.
    #
    # The maximum is 10, so it should raise a TooManyChaptersError, and leave
    # the book unchanged.
    if env.step(
        env.run_bookie_and_catch_error("add-chapters", f"--title={TITLE}", "--count=11"),
        env.load_book(TITLE),
    ):
        assert isinstance(env.error, TooManyChaptersError)
        assert env.book.chapters == []


class Env(TestEnv):
    pass
```

Each step is a comment block, then `if env.step(<actions>):`, then a body with asserts.

- The comment starts with the **action**, as a story beat in the first person plural ("We run ...", "We have
  ...", "The developer edits ..."). If the step has expected results, an empty comment line (`#`) follows, and
  then the **expected result**, phrased with "should".
- A step without expected results has only the action part, and its body is `pass`.
- A step that only inspects state is `if env.step():`, with a comment that says what we look at ("We look at the
  tags. ...").
- A comment that explains _why_ goes directly above the assert that it explains.

Style rules:

- The actions are the arguments of `env.step(...)`, one per line, in the order in which they run (Python evaluates
  them left to right). Keep a step small: one user action plus the set-up that it needs.
- The body only asserts on state: it runs no actions, and uses `env.<attribute>` and queries (not local
  variables).
- Use real-looking, readable values, and define shared texts as module constants.

## The Env classes

An Env holds the **state** of a test (attributes) and the **actions** that change it (methods).

- `Context` is a dataclass with the pytest fixtures that the tests need (e.g. `repo_dir` from `tmp_path`,
  `monkeypatch`, `capsys`). The `context` fixture is in the `conftest.py` of the test package, and tests take
  `context: Context` as their only argument.
- The base `TestEnv` lives in a shared module of the tests. Its `__init__` declares the common state (every
  attribute initialized to `None` or empty, so that a reader sees which state exists), resets singletons that could
  leak from an earlier test, and calls the hook `__post_init__()`. It sets `__test__ = False`, so that pytest
  doesn't collect it. `step(*_)` ignores its arguments and returns `True`.
- A feature with many shared actions (e.g. a git repo with a session, fake policies) gets an intermediate base
  class in `<feature>_test_env.py`.
- Each test file ends with its own `class Env(...)`, which adds only the actions that this file needs. Prefer
  duplicating a two-liner over sharing it between test files. An action that two or three features need goes into
  the closest shared base class.

Rules for actions:

- An action runs immediately and returns `None`. It reads and writes state on `self`, and its name says what the
  user or the world does (`run_bookie`, `write_file`, `commit_all`). Give it a short docstring when its effect is
  not obvious.
- An action that stores a result may take a `store_as` argument when a test needs more than one result (e.g.
  `load_book(store_as="old_book")`). It then leaves the default attribute untouched.
- A query (e.g. `env.git_status()`, `env.read_file(path)`) returns a value for an assert, and is not passed to
  `env.step(...)`.
- Queries go at the bottom of the class, below the actions and the private helpers, after a `# Queries`
  comment. This keeps the actions (which a reader follows in the steps) apart from the helpers of the asserts.
- To test that something raises, use a `*_and_catch_error` variant of the action that stores the exception in
  `env.error`. `SystemExit` is not an `Exception`: a `*_and_catch_exit` variant stores it in `env.system_exit`
  (e.g. for usage errors). Don't use `pytest.raises` in these tests.
- Patching (env vars, the cwd, `input`) happens in actions, through `monkeypatch`, never in the test body.
- Helpers that tests should not call directly are private (`_git`).

## Testing a command-line tool

- The entrypoint has a `run(argv)` that lets errors pass through, and a `main(argv)` for the console script that
  calls `run` in a try-catch block that prints the errors (with a hint) and returns the exit code
  (see [py-write-entrypoint](py-write-entrypoint.md)).
  Most tests call `run` (`run_bookie`), so that they can assert on the error. A test of what the user sees calls
  `main` (`run_bookie_cli`), and stores the exit code in `env.exit_code` and what was printed in `env.output` (via
  `capsys`).
- An action like `answer_prompts(answer)` replaces `input`: it stores the questions in `env.prompts`, and fails the
  test when the tool asks a question that the test didn't expect.

## Practical conventions

- Prefer real code paths over mocks. Use fakes only at the boundary (external services, expensive tools), through
  the policies of the code (see [py-write-policy](py-write-policy.md)), and keep them in a shared
  `fake_policies.py`. A fake records the requests that it receives, and raises an error for a request that the test
  didn't script.
- Make the environment deterministic: never depend on the developer's shell, and give the requests of a fake
  predictable ids.
- Git-based tests run in a real temporary git repo on branch `main`. Detect "HEAD moved" with
  `remember_git_head()` and `env.git_head() != env.remembered_git_head`.
- Format with `black`, follow the import order of the existing test files, and remove unused imports.
- Run the tests that you changed and the whole test suite. Don't commit or stage anything unless asked to.

## Converting an existing test

1. List the distinct workflows and edge cases that the old test covers.
2. Decide for each: workflow test, impl test, or unit test. If unsure, ask.
3. Write each new test with the anatomy above, and remove the old test.
4. Keep the coverage of the old test: every assert that you drop is dropped on purpose.
5. Report which tests were created where, what was split or merged, and which asserts were dropped.

## Checklist

- [ ] One test function per file, named after the scenario, in `test_<feature>/` or `test_<feature>_impl/`
- [ ] Every step has a comment block (action, then "should" results) and an `if env.step(...)` with asserts only
- [ ] Each file has its own small `Env`; shared actions live in the feature's test env
- [ ] Queries are at the bottom of each Env class, after a `# Queries` comment
- [ ] Errors are caught with `*_and_catch_error` / `*_and_catch_exit` actions, not `pytest.raises`
- [ ] Fakes only at the boundary, through the policies
- [ ] The test package is listed in `ENABLED_TEST_PACKAGES` once its code exists
