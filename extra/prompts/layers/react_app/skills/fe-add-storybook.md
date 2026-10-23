# Skill: fe-add-storybook

Applies when writing a Storybook story file for a View or reusable Component. Stories provide isolated, MSW-backed previews of components without requiring a running backend.

---

## When to write a story

Write a story for every:

- **Standalone View** — a View that exists as a meaningful endpoint in itself, not merely as a building block inside a larger View. For example, `BlogListView` is standalone; `BlogListViewItem` is not (it only exists as a building block of `BlogListView` and is already shown there).
- **Reusable Component** — a component used across multiple Views, not just as a widget inside one View that already has its own story.

When in doubt, ask rather than guessing.

---

## File location

```
stories/<Name>.stories.tsx
```

Primary reference: `blogs_fe/src/stories/BlogListView.stories.tsx`

---

## Structure

```tsx
import { Meta, StoryObj } from '@storybook/react';
import { StorybookProvider } from '/src/app/components';
import { BlogListView } from '/src/blogs/components';
import { BlogsStateProvider } from '/src/blogs/components/BlogsStateProvider';
import { passthroughHandlers } from '/src/mocks/browser/defaultPassthrough';
import { handleGetBlogs } from '/src/mocks/queries/handleGetBlogs';

const meta: Meta<typeof BlogListView> = {
  component: BlogListView,
  parameters: {
    msw: {
      handlers: [handleGetBlogs, ...passthroughHandlers],
    },
  },
};

export default meta;

type Story = StoryObj<typeof BlogListView>;

export const Default: Story = {
  render: () => {
    return (
      <StorybookProvider>
        <BlogsStateProvider>
          <BlogListView />
        </BlogsStateProvider>
      </StorybookProvider>
    );
  },
};
```

---

## `StorybookProvider`

`StorybookProvider` (from `app/components/StorybookProvider.tsx`) is a thin wrapper that provides the minimum set of providers every story needs — typically `QueryClientProvider` and `AuthStateProvider`. Always use it as the outermost wrapper rather than duplicating provider setup in each story file.

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

## MSW handlers

Stories must not depend on a real backend. Install MSW handlers in `parameters.msw.handlers` for every query the component (or its StateProviders) will run:

```ts
parameters: {
  msw: {
    handlers: [handleGetBlogs, ...passthroughHandlers],
  },
},
```

- Import handlers from `mocks/queries/handle<QueryName>.ts` (see `fe-add-api-hooks` skill).
- Always spread `passthroughHandlers` from `mocks/browser/defaultPassthrough` — it passes through unmatched requests rather than letting MSW error on fonts, source maps, etc.
- Add one handler per query that the wrapped StateProviders execute.

---

## StateProvider wrapping

Include only the StateProviders the component actually needs. Inspect which context selectors the component (and its children) pull from and include the providers for those contexts only — do not wrap with the full App provider tree.

```tsx
<StorybookProvider>
  <BlogsStateProvider>       {/* needed: BlogListView reads blogsCtx */}
    <BlogListView />
  </BlogsStateProvider>
</StorybookProvider>
```

---

## Checklist

- [ ] Story file is in `stories/<Name>.stories.tsx`
- [ ] `meta` exports `component` and `parameters.msw.handlers`
- [ ] MSW handlers cover every query run by the component and its wrapped StateProviders
- [ ] `passthroughHandlers` spread into `handlers`
- [ ] `StorybookProvider` is the outermost wrapper in `render`
- [ ] Only the StateProviders the component actually needs are included
- [ ] At least a `Default` story exported
