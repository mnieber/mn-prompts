# Design: the --git-ignore option

## What the user does

```bash
mn-prompts install --target=python_lib --git-ignore               # also adds CLAUDE.md and instructions to .gitignore
mn-prompts install --target=python_lib --agents-md --git-ignore   # adds AGENTS.md instead of CLAUDE.md
mn-prompts install --git-ignore                                   # re-install from the manifest, and update .gitignore
```

## What should happen

With `--git-ignore`, `install` adds two entries to the `.gitignore` of the project dir (the dir in which it creates
`instructions` and the agents file), and creates that `.gitignore` if it doesn't exist:

```
/CLAUDE.md
/instructions/
```

The agents file entry is the one of this install: `/AGENTS.md` with `--agents-md`, or the agents file of the manifest
on a re-install without a selection.

## Decisions

- **G1. The entries are anchored to the project dir** (`/CLAUDE.md`, `/instructions/`), so that a `CLAUDE.md` or
  `instructions` dir deeper in the tree is not ignored. Alternative: unanchored `CLAUDE.md` and `instructions/`
  (shorter, but they also match in sub-dirs).
- **G2. An entry that is already in `.gitignore` is not added again**, so that the option can be repeated. An entry
  counts as present when a line, stripped of whitespace, equals the entry, or the entry without its leading `/`
  and/or trailing `/` (e.g. `CLAUDE.md`, `instructions`, `/instructions`). Other patterns that happen to match (e.g.
  `*.md`) are not detected.
- **G3. New entries are appended at the end of the file, without a comment line.** When the file doesn't end with a
  newline, one is added first. Alternative: a `# mn-prompts` comment above the entries.
- **G4. The agents file is added also when it already existed** (and was therefore not replaced). If it is already
  tracked by git, ignoring it has no effect; mn-prompts doesn't check this (it doesn't call git).
- **G5. `--git-ignore` is not recorded in the manifest.** It's a one-time change to a file outside the instructions
  dir, and with `/instructions/` ignored, the manifest isn't committed anyway. Switching to `--agents-md` later
  doesn't remove the old entry. Alternative: record it, so that a re-install without arguments also updates
  `.gitignore`.
- **G6. The `.gitignore` is updated after the instructions and the agents file are installed**, so that an install
  error (e.g. `UnknownTargetError` or `InstructionsExistError`) leaves `.gitignore` unchanged.
- **G7. Code unit: an `add_to_git_ignore(project_dir, entries)` action in the `instructions` package**, called by the
  entrypoint. It does not raise errors of its own.
- **G8. mn-prompts still leaves version control to the user by default**; `--git-ignore` is an opt-in for users who
  don't commit the instructions.

## Changes to the scenarios

- s30 (installs the prompts): an optional step that adds the agents file and `instructions` to `.gitignore`.

