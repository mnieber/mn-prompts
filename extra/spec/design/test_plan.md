# Test plan: the --git-ignore option

## Batch 1: adding the installed files to .gitignore (`tests/install_tests/`)

Workflow tests (`test_install/`):

- `test_a_user_ignores_the_installed_files.py`: `install --target=python_lib --git-ignore` in a project without
  `.gitignore` creates it with `/CLAUDE.md` and `/instructions/`; a second `install --git-ignore` (from the
  manifest) leaves it unchanged.

Impl tests (`test_install_impl/`):

- `test_git_ignore_entries.py`: an existing `.gitignore` keeps its lines and gets the entries appended (a newline is
  added when the file doesn't end with one); entries that are present in another form (`CLAUDE.md`,
  ` /CLAUDE.md `, `/instructions`, `instructions/`) are not added again; a missing entry is added on its own.
- `test_no_git_ignore_without_the_option.py`: without `--git-ignore` no `.gitignore` is created.
- `test_git_ignore_agents_file.py`: with `--agents-md` the entry is `/AGENTS.md`; a re-install without a selection
  uses the agents file of the manifest.
- `test_git_ignore_existing_agents_file.py`: an existing `CLAUDE.md` that was not replaced is still added.
- `test_git_ignore_after_an_error.py`: an install that raises `UnknownTargetError` leaves `.gitignore` unchanged.

Code units: `add_to_git_ignore` (instructions package), the entrypoint (`--git-ignore`).
