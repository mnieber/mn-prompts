# Skill: fe-add-create-effect

Applies when navigating to a "create" route should instantiate a transient resource. A `CreateXxxEffect` is a renderless observer component that watches the URL, calls `addition.add()` via a `useEffect`, and returns `null`. It is placed inside a `<Route>` in a Switch component so it only mounts when its path matches.

See the `fe-add-select-effect` skill for the companion `SelectXxxEffect` pattern.

---

## File location

```
<module>/components/Create<Name>Effect.tsx
```

Primary reference: `blogs_fe/src/blogs/components/CreateBlogEffect.tsx`
Secondary reference: `blogs_fe/src/blogPosts/components/CreateBlogPostEffect.tsx`

---

## Structure

```tsx
import { observer } from 'mobx-react-lite';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { BlogT, createBlog } from '/src/api/types/BlogT';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';

type PropsT = {};

const ContextProps = {
  blogsAddition: blogsCtx.blogsAddition,
};

export const CreateBlogEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { hasUrlChanged } = useRefUrl();
    const { blogsAddition } = props;

    React.useEffect(() => {
      if (hasUrlChanged) {
        if (!blogsAddition.item) {
          const values: BlogT = createBlog({});
          blogsAddition.add({ values });
        }
      }
    });

    return null;
  }, ContextProps)
);
```

---

## How it works

1. **`useRefUrl()`** — detects when the URL changes to the "create" route. Only `hasUrlChanged` is needed here; `updateRefUrl` is not called (see below).
2. **Guard** — only calls `addition.add()` when `addition.item` is not already set. This prevents creating a second transient instance on re-renders while the create form is already open.
3. **`create<Name>({})`** — constructs a transient instance with default values (see the `fe-add-model` skill). Pass it as `values` to `addition.add({ values })`.
4. **Returns `null`** — no visual output. The create form is rendered by the `FormView` component mounted at the same route.

**Why `updateRefUrl()` is not called:** the ref advances only when the create flow completes or is cancelled. That transition is handled by the FormView's cancel handler via `navState.restoreNavPoint()`, not by this effect.

---

## Placement in Switch components

Place the effect inside a `<Route>` so it only mounts when the "create" path matches:

```tsx
<Route path={ext(blogsRoutes.blogs())}>
  <BlogsPage />
  <Route path={blogsRoutes.createBlog()}>
    <CreateBlogEffect />
  </Route>
</Route>
```

The effect unmounts when the route no longer matches, which is the normal case after a successful save or cancel navigates away.

---

## Checklist

- [ ] Only `hasUrlChanged` used from `useRefUrl()`; `updateRefUrl` not called
- [ ] `addition.add()` guarded by `!addition.item` to prevent double-creation
- [ ] `create<Name>({})` factory used to build the transient instance passed as `values`
- [ ] Returns `null`
- [ ] Component wrapped in `observer(withContextProps(..., ContextProps))`
- [ ] Placed inside a matching `<Route>` in a Switch component
