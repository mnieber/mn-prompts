# The development workflow

A new feature goes through five phases. Each phase is a separate task: I tell you which one we're working on.

The paths below assume a flat `spec` directory. When `spec` has a subdirectory per topic (see
[writing specs](./app-write-specs.md)), they are relative to the topic directory (e.g.
`extra/spec/<topic>/design/test_plan.md`).

`RULE`: dont insert cross-references (e.g. to milestones) into the spec documents or the code. These cross-references are not helpful and easily go stale. The one exception is the design notes of a draft scenario (see below): they are dropped at the end, so their milestones may refer to the groups of the flow chart, and to other scenarios.

## Fast-tracking and brief-mode

I can ask you to fast-track a feature to a phase, e.g. "fast-track to the tests". You then do all the phases from
the current one up to and including that phase, in one go, without stopping for my reviews in between.

- Where a phase tells you to ask me about a design choice, pick the answer that you would have proposed, and record
  it in the decisions of the draft scenario as usual.
- When a choice is too uncertain or too important to make alone, stop and ask me.
- When you reach the end of the fast-tracked phase, list the decisions that you made on my behalf, and ask me to
  review the result. For each decision, also list the alternatives that you didn't pick, so that I can ask you to
  switch to one of them.

I will ask you to use brief-mode when I anticipate that the design notes and the test-plan are not going to be
interesting to me. In that case you can keep them very brief and just write down the essentials there so that they can serve you
in the next phases.

## 1. Design

The new features are designed in draft scenarios: new scenario files (`extra/spec/scenarios/`) that describe what
the user does, what should happen, and the decisions that were made. A draft scenario has the layout of a final
scenario (see [writing specs](./app-write-specs.md)), without the `run_scenario` function, and with an extra `##
Design notes (to be dropped)` section at the end of its markdown. The draft scenarios only describe the work that is
not yet in the scenarios.

`RULE`: in the design phase, only write new (draft) scenarios. Don't update the existing scenarios: when the feature
changes the behaviour of an existing scenario, say so in the decisions of the draft. The existing scenarios are
updated in the scenarios phase.

`RULE`: don't decide on the code units in the design phase: the tests decide them (see the test plan). The flow chart
and the footnotes describe the workflow and the features. Only name a code unit that already exists, when it helps
to understand the flow.

`RULE`: when I ask you to review a design then focus on weaknesses and gaps in the main features and workflows. Details and less important edge-cases can be identified later.

### The layout of a draft scenario

`RULE`: write a draft scenario in this layout (see the example in
`examples/bookie/extra/spec/scenarios/s20_a_user_exports_a_book/scenario.py`):

- The introduction, the diagram and the footnotes are written as in a final scenario. The flow chart groups its
  steps in titled subgraphs, one per goal (e.g. `subgraph export ["Write the export file"]`). The footnotes stay
  short: they describe the main design, and they grow when the draft is converted into the final scenario.
- The `## Design notes (to be dropped)` section holds what the final scenario leaves to the tests, or that is only
  needed while the feature is being made:
  - Each milestone is a numbered `###` section, named after what the user does (e.g. `### 2. Alice exports a book
    that was exported before`). Under the title, a `Groups:` line names the subgraphs of the flow chart that the
    milestone covers.
  - The milestone is a numbered list of the steps of the workflow: what the user does, and what should happen. Use
    example people and data (Alice, Bob, a concrete title), and nest numbered sub-steps when a step has parts.
  - Under the step that it belongs to, a `- Detail:` bullet adds a rule or a technical choice (e.g. how a file name
    is derived), and a `- Edge-case:` bullet describes what happens when something goes differently (e.g. the file
    exists, the disk is full). Keep these out of the numbered steps, so that the steps stay the main story.
  - The section ends with a `### Decisions` section: one bullet per decision that was made, with the
    alternative(s) that were not chosen, and "(the user's choice)" when I made the decision. Open questions also go
    here, marked as open, with a proposal. A change to the behaviour of an existing scenario is also listed here.

```markdown
## Design notes (to be dropped)

### 2. Alice exports a book that was exported before

Groups: "Write the export file".

1. Alice exports "The Lorem Book" again. Bookie asks whether it should overwrite `the_lorem_book.md`, and Alice
   confirms.
   - Detail: the file name is the title of the book in snake case.
   - Edge-case: with `--yes`, Bookie overwrites the file without asking.

### Decisions

- An existing file is only overwritten after a confirmation (the user's choice). Alternative: add a number to the
  file name.
- Open: can a user export a single chapter? Proposal: no, only whole books.
```

### The glossary

The important concepts of the project are described in a glossary (`extra/spec/design/glossary.md`). Unlike the
design notes, the glossary is never emptied: it describes the concepts of the whole project, not only of the feature
that is being designed.

`RULE`: when a design introduces a new concept that seems important (e.g. a term that the specs, tests or code will
use, or that a reader needs to know to understand the design), add it to the glossary. When a design changes the
meaning of a concept that is already in the glossary, update its entry. Create the glossary if it doesn't exist yet.

Each entry is a `###` heading with the name of the concept, followed by a short description of what it is and how
it relates to other concepts. Keep the entries in alphabetical order.

```markdown
# Glossary

### Library

The collection of books of a user. A book belongs to exactly one library.
```

## 2. Test plan

Translate the draft scenarios into a test plan (`extra/spec/design/test_plan.md`) that contains a high-level
description of the tests. Group the tests in batches (one feature or group of related features per batch). In this
phase we only write and review the test plan: no tests are written yet.

- Before writing a batch, ask me about the design choices that change what the tests assert, and propose an
  answer. I often refine the proposal.
- Record every decision in the draft scenario (in its design notes, or in its flow chart and footnotes when the
  decision changes the workflow), so that the draft scenarios stay the single description of the design.
- Per batch, the test plan lists the test files, and the code units (e.g. action files, rules files, and the errors
  that they define) that the tests exercise. The tests are the spec of the code structure: what they import (e.g. the
  action file that defines an error) implies which code units exist and where they live. Browser tests import no app
  code; there, the urls, component names, fake endpoints and field labels that they use play this role.
- Ask me to review the test plan when it's done.

`RULE`: after generating the test-plan you don't need to summarize it for me.

## 3. Tests

Write all the tests of the test plan, batch by batch. The tests follow the workflow-test skill file of the layer
(for Python: the `py-write-workflow-tests` skill; for React apps: the `fe-write-workflow-tests` skill). All the tests
are written before the code exists, so they stay disabled until their code is written.

- When writing a test raises a design choice that the draft scenarios don't settle, ask me, and record the decision
  in the draft scenario.
- When a test deviates from the test plan (e.g. a test is split in two files), update the test plan.

## 4. Code

You write the code that makes the tests pass, following the skills of the layer.

- Read the draft scenarios and the tests of the feature first.
- Enable the new tests in batches, and make each batch pass before you continue.
- Run the whole test suite at the end. Don't run tests that cost money (e.g. e2e tests that call an external
  service) without asking.
- When the draft scenarios and the tests don't settle a choice, pick a sensible option, and mention it in your report. When the choice matters to the design, ask.

## 5. Scenarios

The draft scenarios are converted into final scenarios, and the existing scenarios are updated with the changes
that affect the high-level workflows and features (see [writing specs](./app-write-specs.md)). Edge cases and details
are left to the tests.

- Split the work in one or more suitable batches (as you see fit), and ask me to review each batch.
- To convert a draft scenario into a final scenario:
  - Bring the introduction, the flow chart and the footnotes up to date with what was built: the decisions that
    were made in the later phases, and the code units that the tests and the code introduced.
  - Move what the reader needs to understand the high-level design from the design notes into the footnotes. The
    rest is covered by the tests.
  - Add the `run_scenario` function, with the code units of the feature.
  - Remove the `## Design notes (to be dropped)` section.
- Update the existing scenarios whose behaviour the feature changed (the decisions of the draft list the ones that
  were known in the design phase). A draft scenario may also be merged into an existing scenario, when that reads
  better.
- When no draft scenario is left, the feature is done. The glossary is not emptied: check that the concepts of the
  feature are in it, and that their entries match the final design.
- Format the scenario files with `black`. Don't render them with sunya: I do that myself.
