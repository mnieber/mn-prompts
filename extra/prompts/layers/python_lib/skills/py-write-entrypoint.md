# Skill: py-write-entrypoint

Applies when writing an application entrypoint.

Primary reference: `bookie/runtime/entrypoints/bookie.py`, `bookie/pyproject.toml`

---

## File location

```
<app_package>/runtime/entrypoints/<name>.py
```

## Structure

An entrypoint file contains:

1. A `_parse_args(argv)` function using `argparse`.
2. Any private helper functions needed by `run()`.
3. A `run(argv=None)` function that calls `_parse_args(argv)` and dispatches to actions. It lets errors pass
   through, so that the tests can assert on them.
4. A `main(argv=None)` function for the console script: it delegates to `run`, but prints the errors (with a
   hint, and the traceback only with `-v`) and returns the exit code.
5. A `if __name__ == "__main__": sys.exit(main())` guard.

RULE: Use a separate `_parse_args()` function based on the `argparse` package.

```python
def _parse_args(argv):
    parser = argparse.ArgumentParser(description="...")
    # add arguments / subparsers
    return parser.parse_args(argv)


def run(argv=None):
    args = _parse_args(argv)
    # dispatch to actions
    return 0


def main(argv=None):
    # Runs the tool for the user: errors are printed instead of raised
    try:
        return run(argv)
    except Exception as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

## Registering in pyproject.toml

RULE: Add the entrypoint to the `[project.scripts]` section of `pyproject.toml`.

```toml
[project.scripts]
bookie = "bookie.runtime.entrypoints.bookie:main"
```

## Checklist

- [ ] Entrypoint file is under `<app_package>/runtime/entrypoints/`
- [ ] `_parse_args()` uses `argparse` and is a private function (leading underscore)
- [ ] `run()` calls `_parse_args()` and dispatches to action functions, without catching errors
- [ ] `main()` runs the same commands, prints the errors and returns the exit code
- [ ] `if __name__ == "__main__": sys.exit(main())` guard present
- [ ] Entry added to `[project.scripts]` in `pyproject.toml`
