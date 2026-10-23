# Skill: fe-add-select-effect

Applies when a URL change should drive resource selection. A `SelectXxxEffect` is a renderless observer component that watches the URL, calls `selection.selectItem()` via a `useEffect`, and returns `<UrlEffectView>` to surface sync warnings in dev. It is placed inside a `<Route>` in a Switch component so it only mounts when its path matches.

See the `fe-add-create-effect` skill for the companion `CreateXxxEffect` pattern.

---

## File location

```
<module>/components/Select<Name>Effect.tsx
```

Primary reference: `blogs_fe/src/blogs/components/SelectBlogEffect.tsx`
Secondary references: `blogs_fe/src/blogPosts/components/SelectBlogPostEffect.tsx`, `woodstock_ui/src/traces/components/SelectTraceEffect.tsx`

---

## Structure

```tsx
import { observer } from 'mobx-react-lite';
import * as R from 'ramda';
import React from 'react';
import { withContextProps } from 'react-props-from-context';
import { useParams } from 'wouter';
import { BlogT } from '/src/api/types/BlogT';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { useRefUrl } from '/src/routes/hooks/useRefUrl';
import { UrlEffectView } from '/src/utils/components';
import { ObjT } from '/src/utils/types';

type PropsT = {};

const ContextProps = {
  blogs: blogsCtx.blogs,
  blog: blogsCtx.blog,
  blogsSelection: blogsCtx.blogsSelection,
};

export const SelectBlogEffect = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const params = useParams() as ObjT;
    const { updateRefUrl, hasUrlChanged } = useRefUrl();

    const { blogsSelection, blog, blogs } = props;
    const blogFromUrl = R.find((x: BlogT) => x.slug === params.blogSlug)(blogs);
    const isBlogInSyncWithUrl = blog?.id === blogFromUrl?.id;

    const selectBlog = (blog?: BlogT) => {
      blogsSelection.selectItem({ itemId: blog?.id });
    };

    React.useEffect(() => {
      if (hasUrlChanged) {
        if (blogFromUrl) {
          updateRefUrl();
          if (!isBlogInSyncWithUrl) {
            selectBlog(blogFromUrl);
          }
        } else {
          selectBlog(undefined);
        }
      }
    });

    return (
      <UrlEffectView
        resourceName="blog"
        isInSync={isBlogInSyncWithUrl}
        className="absolute"
      />
    );
  }, ContextProps)
);
```

---

## How it works

1. **`useParams()`** — reads URL params (e.g. `{ blogSlug: 'judo' }`) from the current route match. Cast to `ObjT`.
2. **`useRefUrl()`** — tracks a ref to the last-seen URL. `hasUrlChanged` is `true` when the current location differs from the ref. `updateRefUrl()` advances the ref to the current location.
3. **Find the resource** — use `R.find` to locate the matching item in the full list by whatever field is encoded in the URL (slug, id, natural key, etc.).
4. **Sync check** — compare the currently selected item's identity to the found item's identity. This produces the `isInSync` flag.
5. **`useEffect`** (no dependency array) — runs after every render. Only acts when `hasUrlChanged`:
   - If a match is found: call `updateRefUrl()`, then call `selectItem` if not already in sync.
   - If no match: call `selectItem({ itemId: undefined })` to clear the selection. Do **not** call `updateRefUrl()` on a miss — advancing the ref would suppress the next selection attempt.
6. **`UrlEffectView`** — always render it. It shows a visible warning in dev when `isInSync` is false for longer than a brief delay. Pass `className="absolute"` so it doesn't shift layout.

---

## Wildcard routes

When the route uses a wouter wildcard (e.g. `/traces/*`), the matched segment is at `params['*']` rather than a named param:

```ts
const traceKeyFromUrl = params['*'];
```

Reference: `woodstock_ui/src/traces/components/SelectTraceEffect.tsx`

---

## Identity field

The field used in `R.find` and in the sync check must be consistent:

- **Entity types** — find by URL param field (e.g. slug), check sync by `id`: `x.slug === params.blogSlug` to find; `blog?.id === blogFromUrl?.id` for sync.
- **Natural-key types** — find and check sync by the same key: `x.traceKey === traceKeyFromUrl`; `trace?.traceKey === traceFromUrl?.traceKey`.

---

## Placement in Switch components

Place the effect inside a `<Route>` so it only mounts when the path matches:

```tsx
<Route path={ext(blogsRoutes.blogs())}>
  <BlogsPage />
  <Route path={blogsRoutes.blog()}>
    <SelectBlogEffect />
  </Route>
</Route>
```

The effect unmounts when the route no longer matches, resetting `useRefUrl` cleanly on each navigation.

---

## Checklist

- [ ] `useParams()` cast to `ObjT`; wildcard routes use `params['*']`
- [ ] `R.find` locates the item by the URL param field
- [ ] Sync check compares the currently selected item's identity to the found item's identity (consistent field on both sides)
- [ ] `useEffect` has no dependency array (runs after every render)
- [ ] `updateRefUrl()` called only on a successful match, not on miss
- [ ] `selectItem({ itemId: undefined })` called when no match found (clears selection)
- [ ] `<UrlEffectView resourceName="..." isInSync={...} className="absolute" />` returned
- [ ] Component wrapped in `observer(withContextProps(..., ContextProps))`
- [ ] Placed inside a matching `<Route>` in a Switch component
