# Skill: fe-add-component

Applies when writing a general React component — one that is not a ListView, FormView, or other pattern that has its own dedicated skill. Use the more specific skill when one applies; use this skill for everything else (page components, button components, panels, etc.).

---

## File structure

```
<module>/components/
  <Name>.tsx        ← component
  <Name>.scss       ← intrinsic styles (omit if the component has no intrinsic styles)
```

Primary reference: `blogs_fe/src/blogs/components/BlogsPage.tsx`

---

## Structure

```tsx
import { observer } from 'mobx-react-lite';
import { withContextProps } from 'react-props-from-context';
import { blogsCtx } from '/src/blogs/hooks/useBlogsContext';
import { L } from '/src/frames/layout';
import { cn } from '/src/utils/classnames';
import './BlogsPage.scss';

export const ContextProps = {
  blogPostsAddition: blogPostsCtx.blogPostsAddition,
  blogPostsEdit: blogPostsCtx.blogPostsEdit,
};

export type PropsT = React.PropsWithChildren<{
  className?: any;
}>;

export const BlogsPage = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    return (
      <div className={cn('BlogsPage', L.row.bar(), props.className)}>
        {/* ... */}
      </div>
    );
  }, ContextProps)
);
```

---

## Key rules

### Props

- **Do not destructure `props`** — always access properties via `props.foo`, never `const { foo } = props`.
- **`className?: any`** — include on every component that can be placed in different layout contexts. This lets the parent pass ad-hoc positioning/sizing classes.
- **`ContextProps`** — declare a `ContextProps` object when the component needs MobX state from context. Each entry is a `[hookFn, 'key']` tuple from the module's context file. Omit `ContextProps` and `withContextProps` when the component takes everything through explicit props (e.g. a pure presentational button).

### `observer` + `withContextProps`

- Wrap every component that reads MobX state in `observer(withContextProps(..., ContextProps))`.
- `observer` makes the component re-render when observable values change.
- `withContextProps` injects the context values listed in `ContextProps` as additional props.
- Components that do not read MobX state (pure presentational) omit both wrappers.

### Layout object (`L`)

Use `L` from `frames/layout.ts` to express layout intent. The available layouts are defined there. Common ones:

| Expression       | Meaning                                     |
| ---------------- | ------------------------------------------- |
| `L.row.bar()`    | Horizontal flex row, no shrink              |
| `L.col.banner()` | Vertical flex column, fills available space |
| `L.col.canvas()` | Vertical flex column, main content area     |
| `L.col.skewer()` | Vertical flex column, items stacked         |

Pass `L.xxx()` as the first positional class to `cn(...)` after the component name class.

### SCSS — intrinsic vs ad-hoc styles

Styles are split into two categories:

- **Intrinsic styles** — styles that are not context-dependent (e.g. `display: flex`, `cursor: pointer`, `border-radius`). These go into the `.scss` file where they don't clutter the JSX.
- **Ad-hoc styles** — context-dependent styles (margins, background-color chosen by the parent, sizing applied at the call site). These are passed via `className` or inlined in the JSX.

Guidelines:

- **Margins are always ad-hoc** — they are outside the boundary of the element and belong to the parent.
- **Background-color is ad-hoc** when callers need to choose it (e.g. a card used in multiple places with different backgrounds). It is intrinsic when the component always has the same background.
- When in doubt, ask: "would a different caller want this to be different?" If yes, it's ad-hoc.
- Occasionally an intrinsic property is inlined instead of put in SCSS when it's architecturally interesting (e.g. a `position: relative` that creates a stacking context). Use judgement.

### `cn(...)` — class name composition

```tsx
<div className={cn('ComponentName', [L.col.banner(), 'some-tailwind-class'], props.className)}>
```

- First argument: the BEM root class name (same as the component name).
- Middle arguments: layout and structural classes (wrapped in an array).
- Last argument: `props.className` — ad-hoc classes from the caller.

---

## Checklist

- [ ] The top-level div has a class property with the component name (this aids inspection of the DOM)
- [ ] Props accessed via `props.foo`, never destructured
- [ ] `className?: any` included so callers can pass ad-hoc positioning
- [ ] `observer(withContextProps(..., ContextProps))` used when reading MobX state
- [ ] `L.xxx()` from `frames/layout.ts` used for layout intent
- [ ] Intrinsic styles in `.scss`; ad-hoc styles via `props.className` or inline
- [ ] `cn(name, [...classes], props.className)` pattern for class composition
