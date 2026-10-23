# Skill: py-write-python-files

Applies to all Python files in the project — general conventions that cut across every file type.

---

## Comments

RULE: Functions, classes and files should not have a "header" comment at the top, nor should they have a docstring.

Inline comments are welcome when they outline a non-obvious step. Group related lines of code under a short comment that announces the step. Do not add comments for things that are already obvious from reading the code.

## Logging

Use the `logging` package for progress messages and error/warning messages.

RULE: The `print` statement should only be used for actual application output.
Progress messages that are part of the output of a command-line tool (as the specs describe them) are printed to
stderr, so that they stay apart from the output on stdout. Use `logging` for diagnostics.

## Dataclasses

RULE: Use the `dataclass` decorator from the `dataclassy` package (not the standard library `dataclasses`). In `dataclassy`, dict fields may be initialized with `= {}` and list fields with `= []`.
