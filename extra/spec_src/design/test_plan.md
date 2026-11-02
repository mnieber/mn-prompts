# Test plan: composable layers

The fake clone of the tests (`TestEnv.install_editable`) gets target yaml files, layer dirs with an `index.md` and
an `index-snippet.md` (with `requires` frontmatter when the layer requires other layers), an `index_template.md`
with a `{{layers}}` placeholder, an `examples` dir and the agents file. Each snippet is a single line
(`Consult ./<layer>_layer/index.md for <layer>.`), so that tests can read the order of the layers from the index.

## Batch 1: listing targets and layers (`tests/list_tests/`)

Replaces `tests/list_targets_tests/`.

- `test_list/test_a_user_lists_the_targets_and_layers.py`: the targets (sorted, with description and declared
  layers, in columns) and then the layers (sorted).
- `test_list_impl/test_list_edge_cases.py`: hidden entries and other files in the targets and layers dirs are
  skipped; a target without a description; no targets and no layers prints only the headers.
- `test_list_impl/test_missing_prompts_dir.py`: `PromptsDirNotFoundError` (from the `get_prompts_dir` rule), and
  the printed error with the editable-install hint.

Code units: `get_prompts_dir` (with `PromptsDirNotFoundError`), `get_target_names`, `get_target`,
`get_layer_names`, the entrypoint.

## Batch 2: installing the instructions (`tests/install_tests/`)

Replaces `tests/install_target_tests/`.

Workflow tests (`test_install/`):

- `test_a_user_installs_the_prompts_for_their_project.py`: `--target=django_app` gives the symlinks of the target's
  layers plus the required `python_lib`, `examples`, the generated `index.md` (exact text, in dependency order),
  the manifest and `CLAUDE.md`.
- `test_a_user_composes_layers.py`: a target plus a `--layer`; then only `--layer`s, which replaces the selection
  (the deselected symlink is removed, the manifest has no target).
- `test_a_user_reinstalls_after_a_pull.py`: the clone changes a snippet and adds a layer to the target; `install`
  without args regenerates the index and adds the symlink, and leaves the manifest unchanged.
- `test_a_user_installs_an_agents_md_file.py`: `--agents-md` writes `AGENTS.md` (and no `CLAUDE.md`), and records it
  in the manifest; `install` without args keeps using `AGENTS.md`.
- `test_a_team_member_recreates_the_instructions.py`: a project with only the committed files (manifest,
  `project.md`) is re-created with `install` without args; `project.md` is kept.

Impl tests (`test_install_impl/`):

- `test_install_errors.py`: `UnknownTargetError` (lists the targets), `UnknownLayerError` (lists the layers, also
  for a required layer), `MissingIndexSnippetError`, `LayerDependencyCycleError`, `MissingSelectionError`; none of
  them creates files.
- `test_existing_instructions.py`: `InstructionsExistError` for a dir without manifest, a symlink outside the
  prompts-dir, a symlink into the targets dir (an install of the old version), and a `*_layer` entry that is not a
  symlink.
- `test_reinstall_keeps_own_files.py`: own files in the instructions dir are kept; after the clone was moved, a
  re-install repairs the dangling symlinks and removes the stale symlink of a deselected layer.
- `test_generated_index.py`: frontmatter and surrounding blank lines of snippets are stripped; ties in the order
  are broken by name; a layer that is selected twice appears once.
- `test_existing_agents_file.py`: as before.
- `test_install_without_prompts_dir.py`: as before, with `--target`.

Code units: `install_instructions` (with `InstructionsExistError`, `MissingSelectionError`), `copy_agents_file`,
`get_manifest`, `get_index_text`, `get_selected_layers` (with `LayerDependencyCycleError`), `get_layer` (with
`UnknownLayerError`, `MissingIndexSnippetError`), `get_target` (with `UnknownTargetError`).
