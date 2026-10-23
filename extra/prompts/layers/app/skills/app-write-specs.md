# Writing specs

When writing a scenario spec file, please follow the examples in the `spec_src` directories of the examples directory.

`RULE`: spec files should not document previous versions of the system. Especially when you change a spec, avoid referring
to the old solution (e.g. don't write down how the new solution improves on the old solution).

## The goal of spec files (VERY IMPORTANT)

The goal of the specification files is to make the high-level design understandable. The specification files do mention specific functions and models that are used in the source code when these are important for understanding the high-level design (and when this will later help the reader of the source code to understand it). However, it tries to strike a balance and avoids mentioning non-essential details.

`RULE`: a scenario describes the high-level workflow and the features that the user sees. Edge cases and details
(e.g. the exact error for each invalid input, or the order of the checks) are left to the tests, which the reader
can consult.

## There are no explicit module spec files

Modules are defined implicitly through the scenario spec files. All code-unit declarations are made implicitly in the scenario files by referencing module paths such as `c.Books.Actions.CreateBook`, which implies that the books module has an Actions section with a CreateBook action.

## Specs import from the sunya package

The sunya package can be used to render the spec_src to Markdown files. However, for our purposes, we can leave this step out of consideration.

### The External module

The `External` module is a special virtual namespace used only for external actors in scenarios, such as `c.External.Actors.User`. This module does not correspond to a code-unit in the code-base that we're directly working on.

## The scenarios

Each scenario file contains:

1. A `run_scenario()` function that describes the scenario logic using the sunya Python DSL.
2. A `markdown_node` with a structured markdown section. This markdown section has a fixed format with **Steps** and **Diagram** subsections.

## Numbering

Except in legacy spec_src directories, the initial scenarios use decadal numbering: s10_foo, s20_bar, s30_baz, etc.
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

`RULE:` The markdown section starts with a short description that should not duplicate the details that are already described in the steps. Avoid explaining the steps in the introduction and then explaining them again in the Steps section.

`RULE:` Don't insert cross-references to other scenarios, as these go stale quickly. Instead, assume that the reader will find the related scenarios on their own.

The markdown section uses this fixed structure:

````
A short description of the scenario.

### Steps

#### It does X

Step description.</br>

#### It does Y

Step description.</br>

### Diagram

\```mermaid
sequenceDiagram
    ...
\```
````

### The sunya DSL

Common patterns:

- `with goal().do_something(r.thing):` — a goal grouping steps
- `the(r.actor).calls(r.action).with_the(r.form)` — actor calls an action
- `it().creates(r.thing)` — creates something (shorthand for the nearest `the(...)`)
- `it().returns(r.thing)` — returns something
- `it().raises(r.error).if_something()` — raises an error conditionally
- `with the(r.actor).calls(r.action).with_the(r.form):` — a step with nested substeps
