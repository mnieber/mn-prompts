# General instructions for writing applications

Start with the [development workflow](./development_workflow.md): it describes the phases (design, tests, code
and scenarios), and what to do in each of them.

# Using specifications

## 1. Writing Specifications

If you're writing specifications:

- Start with [./writing_specs/instructions-for-writing-specs.md](./writing_specs/instructions-for-writing-specs.md)
- See examples in [examples/bookie/extra/spec_src/scenarios/](./examples/bookie/extra/spec_src/scenarios/)

**[instructions-for-writing-specs.md](./writing_specs/instructions-for-writing-specs.md)**

- How to write scenario specs
- Implicit code-unit declarations in scenarios
- Scenario syntax and DSL (goals, steps, markdown sections)
- The `sunya` package and special modules

## 2. Mapping Specs to Implementation

If you're implementing from specifications:

- Start with [./using_specs/instructions-for-mapping-specs-to-implementation.md](./using_specs/instructions-for-mapping-specs-to-implementation.md)
- Then read [general code generation instructions](./general_code_generation_instructions/) — rules for following project instructions and using example code as templates

**[instructions-for-mapping-specs-to-implementation.md](./using_specs/instructions-for-mapping-specs-to-implementation.md)**

- Section naming conventions (PascalCase → snake_case)
- File structure patterns
- Settings consolidation
- Validation by the tests

## Notes

- The `External` module is virtual and only used for external actors in scenarios
- All code-units (actions, models, rules, etc.) are implicitly declared in scenario specs
- The `sunya` package renders specs to Markdown but this is optional for implementation
