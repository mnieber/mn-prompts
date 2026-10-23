# Skill: py-write-action

Applies when writing an action file: a function that changes application state.

Primary reference: `bookie/books/actions/create_book.py`, `bookie/chapters/actions/create_chapter.py`

---

## File location

```
<module>/actions/<action_name>.py
```

RULE: Each action function must be in its own file.

## What is an action?

An action is a function that changes the application state. This contrasts with rules, which only retrieve or compute information without modifying state.

## Exceptions

An action should raise an exception if it cannot reach its goal. It does not return a success/failure flag; callers distinguish success from failure by whether an exception was raised.

RULE: Define the exception class in the action file itself. Only very generic exceptions (shared across many actions) belong in `utils/exceptions`.

Example from `create_book.py`:

```python
class TooManyChaptersError(Exception):
    pass
```

## Forms

RULE: If the action takes a form argument, define the form dataclass in the same action file. There is no separate `forms/` directory or `forms.py` file.

RULE: A form contains only simple values, not entity objects. For example, `CreateChapterForm` holds the chapter title and paragraph count — it does not hold the `Book` entity (that is passed as a separate argument).

```python
@dataclass
class CreateChapterForm:
    title: str
    nr_of_paragraphs: int
    content_mode: TitleStyles
```

## Comments

RULE: Do not add a header comment or docstring unless there is something non-obvious that a caller would not know. For example, `create_book` has a short note that it checks `MAX_CHAPTERS_PER_BOOK` because that constraint is not visible from the signature alone.

## Helper functions

RULE: Private helper functions inside an action file start with an underscore (e.g. `_filter_paragraph` in `create_paragraph.py`).

## Checklist

- [ ] Action function is in its own file under `<module>/actions/`
- [ ] Exception class defined in the same file (unless truly generic)
- [ ] Form dataclass defined in the same file if the action takes a form
- [ ] Form contains only simple values, not entity objects
- [ ] Helper functions start with an underscore
- [ ] No header comment/docstring unless the constraint is non-obvious from the signature
