# Writing specs

When writing a scenario spec file, please follow the examples in the `spec` directories of the examples directory.

`RULE`: spec files should not document previous versions of the system. Especially when you change a spec, avoid referring
to the old solution (e.g. don't write down how the new solution improves on the old solution).

## The goal of spec files (VERY IMPORTANT)

The goal of the specification files is to make the high-level design understandable. The specification files do mention specific functions and models that are used in the source code when these are important for understanding the high-level design (and when this will later help the reader of the source code to understand it). However, it tries to strike a balance and avoids mentioning non-essential details.

`RULE`: a scenario describes the high-level workflow and the features that the user sees. Edge cases and details
(e.g. the exact error for each invalid input, or the order of the checks) are left to the tests, which the reader
can consult.

## There are no explicit module spec files

Modules are defined implicitly through the scenario spec files. All code-unit declarations are made implicitly in the scenario files by referencing module paths such as `c.Books.Actions.CreateBook`, which implies that the books module has an Actions section with a CreateBook action.

## The layout of the spec directory

A `spec` directory has one of two layouts:

1. Flat: the `design` and `scenarios` directories are directly inside `spec`.

```
extra/spec/
├── design/
└── scenarios/
```

2. Per topic: `spec` has a subdirectory per topic (e.g. `changelog` and `release_notes`), and each topic has its
   own `design` and `scenarios` directories.

```
extra/spec/
├── changelog/
│   ├── sunya.config.yaml
│   ├── design/
│   └── scenarios/
└── release_notes/
    ├── sunya.config.yaml
    ├── design/
    └── scenarios/
```

   Each topic has its own `sunya.config.yaml`, and the root `sunya.config.yaml` lists all of them:

```yaml
configs:
  - extra/spec/changelog/sunya.config.yaml
  - extra/spec/release_notes/sunya.config.yaml
```

`RULE`: in the per-topic layout, ask me which topic we're working on when it's not clear from the task, and
put new scenarios in the scenarios directory of that topic. Don't add a new topic without asking. When you add a
topic, also add its `sunya.config.yaml` to the `configs` list of the root `sunya.config.yaml`.

In the rest of the skill files, paths such as `extra/spec/scenarios/` refer to the flat layout; in the per-topic
layout read them as `extra/spec/<topic>/scenarios/`.

## Specs import from the sunya package

The sunya package can be used to render the spec to Markdown files. However, for our purposes, we can leave this step out of consideration.

### The External module

The `External` module is a special virtual namespace used only for external actors in scenarios, such as `c.External.Actors.User`. This module does not correspond to a code-unit in the code-base that we're directly working on.

## The scenarios

Each scenario file contains:

1. A `run_scenario()` function that describes the scenario logic using the sunya Python DSL.
2. A `markdown_node` with a structured markdown section. This markdown section has a fixed format with a **Diagram**
   section (a flow chart) and a **Footnotes** subsection.

`RULE`: by default, the diagram of a scenario is a flow chart, as described below. Only use the sequence-diagram
format (see the `app-write-sequence-diagrams` skill) when I ask for it.

### Draft scenarios

In the design phase, a new feature is described in a draft scenario (see the
[development workflow](./app-apply-development-phases.md)): a scenario file without the `run_scenario` function, whose
markdown ends with a `## Design notes (to be dropped)` section. In the scenarios phase, the draft is converted into a
final scenario: the design notes are removed, and the `run_scenario` function is added. See
`examples/bookie/extra/spec/scenarios/s20_a_user_exports_a_book/scenario.py` for an example of a draft scenario.

## Numbering

Except in legacy spec directories, the initial scenarios use decadal numbering: s10_foo, s20_bar, s30_baz, etc.
This leaves room to insert other scenarios later (s05_hello).

### The run_scenario function

The `run_scenario` function describes the scenario by:

- Assigning roles to module code-units using `r.<role> = c.<Module>.<Section>.<CodeUnit>`
- Describing goals and steps using `with goal()...` blocks and `the(...)` / `it()` step expressions

#### Goals

Every step must be nested inside a top-level goal. Goals are written as `with` blocks:

```python
with goal().create_a(r.result).using_the(r.foo):
    the(r.actor).does_something_with(r.foo)
```

#### Steps

Steps describe what each participant does. Every step starts with either:

- `the(r.actor).does_something()` — when naming a specific actor
- `it().does_something()` — as a shorthand referring back to the nearest preceding `the(...)` expression

Steps can be nested using `with`:

```python
with the(r.frontend).calls_the(r.action).with_the(r.form):
    it().validates(r.form)
    it().creates(r.result)
    it().returns(r.result)
```

### The markdown section

`RULE:` The markdown section starts with a short description that should not duplicate the details that are already described in the diagram and the footnotes. Avoid explaining the flow in the introduction and then explaining it again in the diagram.

`RULE:` Don't insert cross-references to other scenarios, as these go stale quickly. Instead, assume that the reader will find the related scenarios on their own.

The markdown section uses this fixed structure:

````
A short description of the scenario.

## Diagram

\```mermaid
flowchart TD
    start(["The user does X"]) --> check{{"Is Y the case?"}}:::choice
    check -- yes --> done["Show Z [2]"]
    check -- no --> step_a

    subgraph goal_a ["Achieve goal A"]
        step_a["Do A [1]"] --> step_b["Do B"]
    end

    step_b --> done

    classDef choice color:#c9a227
\```

### Footnotes

#### [1] - A claim about doing A

Details of doing A, which mention the code-units that are involved (e.g. `create_foo` and `FooView`).</br>

#### [2] - A claim about showing Z

Details of showing Z.</br>
````

### The flow chart

The flow chart shows the workflow of the scenario as the reader would explain it: what triggers it, the choices
along the way, and what the user ends up with. It reads top to bottom (`flowchart TD`).

- The flow starts with a stadium-shaped node (`id(["..."])`) for what triggers the scenario, usually what the user
  (or another actor) does.
- A step is a box (`id["..."]`) with a short sentence: an instruction (e.g. "Create the local proxy") or what an
  actor does (e.g. "The user sets the user name"). Use plain language, and mention a code-unit only when it helps to
  understand the flow (e.g. "Show the WelcomeView").
- A choice is a hexagon with a question (`id{{"Is this the first start?"}}:::choice`). Its edges are labelled with
  the answers (`-- yes -->`, `-- no -->`, or `-- "the user cancels" -->`).
- A loop, or a retry, is an edge back to an earlier node: from a choice (e.g. `more -- yes --> paragraph`), or
  labelled with when it happens (e.g. `error -- "the user tries again" --> question_call`). When the loop doesn't
  matter to the flow, a single step says that it is done for several items (e.g. "Fetch each new document").
- The steps that achieve a goal of `run_scenario` are grouped in a `subgraph`, named after the goal (e.g.
  `subgraph start ["Start the local proxy"]`). Steps outside a goal (such as the trigger and the steps that connect
  the goals) stay outside the subgraphs.
- The node ids are short snake_case names (e.g. `has_settings`).
- When the chart has choices, it ends with `classDef choice color:#c9a227`, which colours them.
- A scenario with independent goals (e.g. editing and deleting a blog post) has a trigger per goal, so that the
  chart has several starting points.

`RULE`: keep the nodes short. The details go into footnotes: a node refers to its footnote with a marker at the end
of its label (e.g. `["Mark the interrupted calls [2]"]`). The footnotes are numbered in the order in which they
appear in the chart.

### The footnotes

Each footnote is a `####` section, named `[n] - <claim>`, where the claim is the main point of the footnote (e.g.
`#### [1] - The proxy only answers the SPA`). The body gives the details that the reader needs to understand the
design, and mentions the code-units that are involved. Each sentence (or group of related sentences) ends with
`</br>`.

`RULE`: a footnote explains the high-level design, not the edge cases (see the goal of the spec files). Only add a
footnote to a node when there is something to explain.

### The sunya DSL

Common patterns:

- `with goal().do_something(r.thing):` — a goal grouping steps
- `the(r.actor).calls(r.action).with_the(r.form)` — actor calls an action
- `it().creates(r.thing)` — creates something (shorthand for the nearest `the(...)`)
- `it().returns(r.thing)` — returns something
- `it().raises(r.error).if_something()` — raises an error conditionally
- `with the(r.actor).calls(r.action).with_the(r.form):` — a step with nested substeps
