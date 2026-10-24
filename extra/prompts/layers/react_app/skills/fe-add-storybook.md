# Skill: fe-add-storybook

Applies when writing a Storybook story file for a reusable Component or a View. Stories provide isolated previews of
components without requiring a backend.

---

## When to write a story

Write a story for every:

- **Reusable Component** — a component used across multiple Views (e.g. `DialogButton`), not just as a widget inside
  one View.
- **Standalone View that needs no backend data** — a View that exists as a meaningful endpoint in itself, not merely as
  a building block inside a larger View, and that renders without running queries.

A View that loads data from the backend (e.g. `BlogListView`) gets no story. To try it out without a real backend,
write a playground instead (see "Playgrounds" in the `fe-write-workflow-tests` skill).

When in doubt, ask rather than guessing.

---

## File location

```
stories/<Name>.stories.tsx
```

---

## Structure

```tsx
import { Meta, StoryObj } from '@storybook/react';
import { DialogButton } from '/src/frames/components/DialogButton/DialogButton';

const meta: Meta<typeof DialogButton> = {
  component: DialogButton,
};

export default meta;

type Story = StoryObj<typeof DialogButton>;

export const Default: Story = {
  args: { label: 'Create blog' },
};

export const Disabled: Story = {
  args: { label: 'Create blog', disabled: true },
};
```

---

## `StorybookProvider`

`StorybookProvider` (from `app/components/StorybookProvider.tsx`) is a thin wrapper that provides the minimum set of
providers that a component may need — typically `QueryClientProvider` and `AuthStateProvider`. When a component reads
from these contexts, use it as the outermost wrapper in `render` rather than duplicating provider setup in each story
file.

```tsx
// app/components/StorybookProvider.tsx
export const StorybookProvider = (props: React.PropsWithChildren<{}>) => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthStateProvider>{props.children}</AuthStateProvider>
    </QueryClientProvider>
  );
};
```

Reference: `blogs_fe/src/app/components/StorybookProvider.tsx`

---

## StateProvider wrapping

Include only the StateProviders the component actually needs. Inspect which context selectors the component (and its
children) pull from and include the providers for those contexts only — do not wrap with the full App provider tree.
If a needed StateProvider runs queries, the component needs backend data: write a playground instead of a story.

---

## Checklist

- [ ] Story file is in `stories/<Name>.stories.tsx`
- [ ] The component renders without backend data (otherwise: a playground, not a story)
- [ ] `meta` exports `component`
- [ ] `StorybookProvider` is the outermost wrapper in `render` when the component reads its contexts
- [ ] Only the StateProviders the component actually needs are included
- [ ] At least a `Default` story exported
