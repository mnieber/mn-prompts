# Development of React Apps

When you are asked to generate code, or to plan for generating code, identify which of the below skills are needed and apply them.

## Skills

### Data model

Define a TypeScript type and its Zod validation schema for a new entity or value object.
→ [fe-add-model](./skills/fe-add-model.md)

### API — queries and mutations

Write a `useQuery` hook and/or a `useMutation` hook to fetch or write data via the REST API.
→ [fe-add-api-hooks](./skills/fe-add-api-hooks.md)

### API — MSW mock handlers

Add MSW handlers so the app and Storybook can run without a real backend. Also covers enabling MSW in `main.tsx`.
→ [fe-add-msw](./skills/fe-add-msw.md)

### State layer

Provide MobX-based application state to the View components (containers, facets, `useXState` hook, `registerXCtr`, `XStateProvider`).
→ [fe-use-state-provider](./skills/fe-use-state-provider.md)

### Routing

Define module routes (`XxxRoutes`, `XxxNav`, `DefaultXxxNavHandler`) and wire Switch components.
→ [fe-use-nav-handler](./skills/fe-use-nav-handler.md)

### Form view

Write a form component (`XFormView.tsx`) and its companion `form.ts` (initial values, validation, submit, cancel).
→ [fe-create-formview](./skills/fe-create-formview.md)

### List view

Write a `XListView` + `XListViewItem` with loading guard, keyboard selection, and highlight/selected styles.
→ [fe-add-list-view](./skills/fe-add-list-view.md)

### Select effect

Write a `SelectXxxEffect` that reads a URL param and drives the selection facet (which is part of the state layer) when the URL changes.
→ [fe-add-select-effect](./skills/fe-add-select-effect.md)

### Create effect

Write a `CreateXxxEffect` that instantiates a transient resource when the "create" route is entered. This effect is used in combination
with the addition facet (which is part of the state layer).

→ [fe-add-create-effect](./skills/fe-add-create-effect.md)

### General component

Write a page, panel, or button component that reads MobX state and/or accepts layout props.
→ [fe-add-component](./skills/fe-add-component.md)

### Trimmed component

Write a shared UI primitive (button, card, badge) with a structured `trim` styling interface.
→ [fe-add-trimmed-component](./skills/fe-add-trimmed-component.md)

### App root

Compose providers, `AppBody`, and Switch components in `App.tsx`.
→ [fe-add-app-component](./skills/fe-add-app-component.md)

### Storybook stories

Write isolated stories for standalone views and reusable components, backed by MSW handlers.
→ [fe-add-storybook](./skills/fe-add-storybook.md)

---

### Key Principles

- **camelCase file names** - File and directory names match the spec name in camelCase (e.g. `BlogPostsState/`, `useCreateBlog.ts`)
- **One file per code unit** - Each mutation hook, query hook, State, StateProvider, or component gets its own file
- **Props not unpacked** - Component props are accessed as `props.foo`, not destructured
- **MobX + React Context** - State is MobX-observable; Contexts pass it to consuming components
- **Types in api module** - TypeScript types often live in the `api/types/` directory since they cut across feature modules
- **Follow the examples** - The blogs_fe example serves as the primary reference template
- **Explicit is better** - When in doubt, ask for spec clarification rather than guessing

## Key Principles

- **camelCase file names** - File and directory names match the spec name in camelCase (e.g. `BlogPostsState/`, `useCreateBlog.ts`)
- **One file per code unit** - Each mutation hook, query hook, State, StateProvider, or component gets its own file
- **Props not unpacked** - Component props are accessed as `props.foo`, not destructured
- **MobX + React Context** - State is MobX-observable; Contexts pass it to consuming components
- **Types in api module** - TypeScript types often live in the `api/types/` directory since they cut across feature modules
- **Follow the examples** - The blogs_fe example serves as the primary reference template
- **Explicit is better** - When in doubt, ask for spec clarification rather than guessing
