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

RULE: Use the project's own `dataclass` decorator from `<package>/utils/dataclass.py` (not `dataclasses.dataclass`
from the standard library, and not the `dataclassy` package).

The decorator delegates to `dataclasses.dataclass`, so the result is an ordinary standard-library dataclass. In
addition, it lets list, dict and set fields be initialized with a literal (`= []`, `= {}`, `= set()`, or a non-empty
one such as `= ["a"]`): every instance gets its own deep copy of that default. Values passed to the constructor are
not copied.

If the project doesn't have `<package>/utils/dataclass.py` yet, copy it from the example
(`bookie/utils/dataclass.py`). It has no runtime dependencies.

Because the standard library does the rest of the work, its rules apply: a field without a default cannot follow a
field with a default.
