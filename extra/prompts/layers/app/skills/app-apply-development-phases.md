# The development workflow

A new feature goes through four phases. Each phase is a separate task: I tell you which one we're working on.

## 1. Design

The new features are described in a design doc (`extra/spec_src/design/design.md`): what the user does, what should
happen, and the decisions that were made. The design doc only describes the work that is not yet in the
scenarios.

`RULE`: when I ask you to review a design then focus on weaknesses and gaps in the main features and workflows. Details
and less important edge-cases can be identified later.

## 2. Tests

Translate the design doc into a test_plan.md document that contains a high-level description of the tests. Group the tests
in in batches (one feature or group of related features per batch). The described tests will be written before the code exists.
The tests follow the workflow-test skill file of the layer (for Python: the `py-write-workflow-tests` skill).

- Before writing a batch, ask me about the design choices that change what the tests assert, and propose an
  answer. I often refine the proposal.
- Record every decision in the design doc, so that it stays the single description of the design.
- The tests are the spec of the code structure: what they import (e.g. the action file that defines an error)
  implies which code units exist and where they live.

## 3. Code

You write the code that makes the tests pass, following the skills of the layer.

- Read the design doc and the tests of the feature first.
- Enable the new tests in batches, and make each batch pass before you continue.
- Run the whole test suite at the end. Don't run tests that cost money (e.g. e2e tests that call an external
  service) without asking.
- When the design doc and the tests don't settle a choice, pick a sensible option, and mention it in your report.
  When the choice matters to the design, ask.

## 4. Scenarios

The scenarios (`extra/spec_src/scenarios/`) are updated with the changes that affect the high-level workflows and
features (see [writing specs](./app-write-specs.md)). Edge cases and details are left
to the tests.

- Split the affected scenarios in one ore more suitable batches (as you see fit), write/update the scenarios for a batch, and ask me to review.
- After each review, remove the parts of the design doc that is covered by the batch, together with the details that the
  tests cover. When the design doc is empty, the feature is done.
- Format the scenario files with `black`. Don't render them with sunya: I do that myself.
