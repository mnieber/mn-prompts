# Development of Applications

When you are asked to work on an application (in any phase: design, tests, code or scenarios), identify which of the below skills are needed and apply them.

## Skills

### Development phases

The five phases of developing a feature (design, test plan, tests, code and scenarios), and what to do in each of them. Start here.
→ [app-apply-development-phases](./skills/app-apply-development-phases.md)

### Writing specs

How to write scenario specs: the spec_src layout (flat or per topic), implicit code-unit declarations, the sunya DSL (goals and steps), and the markdown section.
→ [app-write-specs](./skills/app-write-specs.md)

### Mapping specs to implementation

How the module namespaces and code-units in the scenario specs map onto feature packages and source files.
→ [app-map-specs-to-implementation](./skills/app-map-specs-to-implementation.md)

### Generating code

General rules for generating code: following `RULE:`s closely, using the code-unit specific skills, and using example code as a template.
→ [app-generate-code](./skills/app-generate-code.md)

---

## Key Principles

- **Specs describe the high-level design** — edge cases and details are left to the tests
- **Implicit declarations** — all code-units (actions, models, rules, etc.) are implicitly declared in scenario specs
- **The External module is virtual** — it is only used for external actors in scenarios
- **Follow the examples** — the example spec_src and src directories show how specs map to code
- **Explicit is better** — when in doubt, ask for spec clarification rather than guessing
