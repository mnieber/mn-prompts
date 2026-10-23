# Skill: fe-add-list-view

Applies when writing a ListView component and its companion ListViewItem. A ListView renders a collection of items from MobX state, handles loading state, and optionally wires keyboard selection and click-based navigation.

---

## File structure

```
<module>/components/
  <Name>ListView.tsx       ← list container: context props, loading guard, item mapping
  <Name>ListView.scss      ← intrinsic list styles
  <Name>ListViewItem.tsx   ← single item: selection handlers, navigation, updating state
  <Name>ListViewItem.scss  ← intrinsic item styles (selected, highlighted, updating)
```

Primary reference: `blogs_fe/src/blogPosts/components/BlogPostListView.tsx` + `BlogPostListViewItem.tsx`
Secondary reference: `blogs_fe/src/blogs/components/BlogListView.tsx` + `BlogListViewItem.tsx`

---

## 1. `<Name>ListView.tsx` — the list container

Reference: `blogs_fe/src/blogPosts/components/BlogPostListView.tsx`

### Structure

```tsx
import { observer } from "mobx-react-lite";
import { isLoading } from "mobx-resource-states";
import * as R from "ramda";
import KeyboardEventHandler from "react-keyboard-event-handler";
import { withContextProps } from "react-props-from-context";
import {
  SelectionUIConnector,
  createSelectionKeyHandlers,
} from "skandha-facets";
import { BlogPostT } from "/src/api/types";
import { BlogPostListViewItem } from "/src/blogPosts/components";
import { blogPostsCtx } from "/src/blogPosts/hooks/useBlogPostsContext";
import { blogsCtx } from "/src/blogs/hooks/useBlogsContext";
import { LoaderBar } from "/src/frames/components/LoaderBar";
import { L } from "/src/frames/layout";
import { createKeyDownHandler } from "/src/utils";
import { cn } from "/src/utils/classnames";
import "./BlogPostListView.scss";

export type PropsT = { className?: any };

const ContextProps = {
  blog: blogsCtx.blog,
  blogPosts: blogPostsCtx.blogPosts,
  blogPostsSelection: blogPostsCtx.blogPostsSelection,
  blogPostsHighlight: blogPostsCtx.blogPostsHighlight,
};

export const BlogPostListView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    if (isLoading(props.blogPosts)) {
      return <BlogPostListViewLoader />;
    }

    const selectionUIConnector = new SelectionUIConnector({
      selection: props.blogPostsSelection,
    });

    const keyHandlers = createSelectionKeyHandlers(props.blogPostsSelection);

    const blogPostDivs = props.blogPosts.map((blogPost: BlogPostT) => (
      <BlogPostListViewItem
        key={blogPost.id}
        className={{
          "BlogPostListViewItem--selected":
            props.blogPostsSelection.itemIds.includes(blogPost.id),
          "BlogPostListViewItem--highlighted":
            props.blogPostsHighlight.itemId === blogPost.id,
        }}
        blog={props.blog}
        blogPost={blogPost}
        selectionUIProps={selectionUIConnector.handle(blogPost.id)}
      />
    ));

    return (
      <KeyboardEventHandler
        handleKeys={R.keys(keyHandlers)}
        onKeyEvent={createKeyDownHandler(keyHandlers)}
      >
        <div
          className={cn("BlogPostListView", [L.col.banner()], props.className)}
          tabIndex={1}
        >
          {blogPostDivs}
        </div>
      </KeyboardEventHandler>
    );
  }, ContextProps)
);
```

### Loading guard

Always check `isLoading(props.items)` before rendering the list. Return a `<XxxListViewLoader>` component (co-located in the same file) that renders placeholder `<LoaderBar>` elements:

```tsx
export const BlogPostListViewLoader = (props: { className?: any }) => {
  const loaderBars = ["1", "2", "3"].map((id) => (
    <LoaderBar key={`item-${id}`} className={cn("my-1 h-6")} />
  ));
  return (
    <div
      className={cn("BlogPostListViewLoader", [
        L.col.banner(),
        "min-w-[50px]",
        props.className,
      ])}
    >
      {loaderBars}
    </div>
  );
};
```

### `SelectionUIConnector` and `createSelectionKeyHandlers`

Both come from `skandha-facets`. Instantiate them inside the component body (after the loading guard) on every render — they are lightweight and stateless:

```ts
const selectionUIConnector = new SelectionUIConnector({
  selection: props.blogPostsSelection,
});
const keyHandlers = createSelectionKeyHandlers(props.blogPostsSelection);
```

- **`SelectionUIConnector`** — produces a `SelectionUIPropsT` object per item via `selectionUIConnector.handle(itemId)`. Pass this as the `selectionUIProps` prop to each `ListViewItem`. It carries the click/keyboard event data the item needs to participate in multi-select.
- **`createSelectionKeyHandlers`** — returns a map of key strings to handler functions (e.g. arrow-up/down, shift-click ranges). Keys may use semicolon-delimited multi-key syntax.

### `KeyboardEventHandler` + `createKeyDownHandler`

Wrap the list div in `KeyboardEventHandler` from `react-keyboard-event-handler`. Pass the key list and a dispatcher built with `createKeyDownHandler`:

```tsx
<KeyboardEventHandler
  handleKeys={R.keys(keyHandlers)}
  onKeyEvent={createKeyDownHandler(keyHandlers)}
>
  <div className={cn('BlogPostListView', ...)} tabIndex={1}>
    {itemDivs}
  </div>
</KeyboardEventHandler>
```

`createKeyDownHandler` (from `/src/utils`) adapts the `(key, event)` callback signature that `KeyboardEventHandler` expects into the plain function calls that `keyHandlers` provides. It also calls `e.preventDefault()` and `e.stopPropagation()` so key events don't bubble.

The inner `div` must have `tabIndex={1}` so it can receive focus and the keyboard events will fire.

### When selection is not needed

When the list doesn't support multi-select (e.g. `BlogListView` — a nav sidebar), omit `SelectionUIConnector`, `createSelectionKeyHandlers`, and `KeyboardEventHandler`. Instead, compute the navigation URL directly in the list and pass it as a prop to the item:

```tsx
const blogDivs = props.blogs.map((blog: BlogT) => {
  const url = blogsNav.blog({ blogSlug: blog.slug }).url;
  return (
    <BlogListViewItem
      key={blog.id}
      className={{
        "BlogListViewItem--highlighted":
          props.blogsHighlight.itemId === blog.id,
      }}
      blog={blog}
      url={url}
    />
  );
});
```

Reference: `blogs_fe/src/blogs/components/BlogListView.tsx`

### Selected / highlighted CSS classes

Pass selection and highlight state as a `className` object (using the `classnames`-compatible object form):

```tsx
className={{
  'BlogPostListViewItem--selected':    props.blogPostsSelection.itemIds.includes(blogPost.id),
  'BlogPostListViewItem--highlighted': props.blogPostsHighlight.itemId === blogPost.id,
}}
```

---

## 2. `<Name>ListViewItem.tsx` — the single item

Reference: `blogs_fe/src/blogPosts/components/BlogPostListViewItem.tsx`

### Structure (with selection)

```tsx
import classnames from "classnames";
import mergeProps from "merge-props";
import { observer } from "mobx-react-lite";
import { isUpdating } from "mobx-resource-states";
import React from "react";
import { selectionUIHandlers, SelectionUIPropsT } from "skandha-facets";
import "./BlogPostListViewItem.scss";
import { BlogPostT } from "/src/api/types";
import { blogPostsNav } from "/src/blogPosts/routes";
import { navTo } from "/src/routes/navHandler";

export type PropsT = {
  blog: BlogT;
  blogPost: BlogPostT;
  className?: any;
  selectionUIProps: SelectionUIPropsT;
};

export const BlogPostListViewItem: React.FC<PropsT> = observer(
  (props: PropsT) => {
    return (
      <div
        className={classnames(
          "BlogPostListViewItem",
          { "animate-delete": isUpdating(props.blogPost) },
          props.className
        )}
        {...mergeProps(selectionUIHandlers(props.selectionUIProps), {
          onClick: (e: React.MouseEvent<HTMLDivElement>) => {
            if (!(e.ctrlKey || e.shiftKey)) {
              navTo(
                blogPostsNav.blogPost({
                  blogSlug: props.blog.slug,
                  blogPostSlug: props.blogPost.slug,
                })
              );
            }
          },
        })}
      >
        {props.blogPost.title}
      </div>
    );
  }
);
```

### `selectionUIHandlers` + `mergeProps`

`selectionUIHandlers(props.selectionUIProps)` returns a set of DOM event handlers (e.g. `onMouseDown`, `onClick`) that the `Selection` facet needs to track which items are selected and how (single, ctrl-click, shift-click).

These handlers must be **merged** with any other handlers on the same element using `mergeProps` from the `merge-props` package — never spread them directly, as that would overwrite the click handler or vice versa.

The navigation `onClick` should only fire when neither `ctrlKey` nor `shiftKey` is held, since those are multi-select gestures that should not trigger navigation:

```tsx
onClick: (e: React.MouseEvent<HTMLDivElement>) => {
  if (!(e.ctrlKey || e.shiftKey)) {
    navTo(xxxNav.item({ ... }));
  }
}
```

### `isUpdating` — deletion animation

Apply a CSS animation class while the item is being deleted (or otherwise mutated):

```tsx
{ 'animate-delete': isUpdating(props.blogPost) }
```

### Structure (without selection — link-based navigation)

When the list uses `<Link>` navigation instead of selection:

```tsx
import { Link } from "wouter";

export const BlogListViewItem: React.FC<PropsT> = observer((props: PropsT) => {
  return (
    <Link
      href={props.url}
      className={classnames(
        "BlogListViewItem",
        { "animate-delete": isUpdating(props.blog) },
        props.className
      )}
    >
      {props.blog.name}
    </Link>
  );
});
```

Reference: `blogs_fe/src/blogs/components/BlogListViewItem.tsx`

---

## 3. SCSS — selected, highlighted, and updating styles

Reference: `blogs_fe/src/blogPosts/components/BlogPostListViewItem.scss`

Define intrinsic styles and state modifier classes in the item's scss file:

```scss
.BlogPostListViewItem {
  display: flex;
  cursor: pointer;
  flex-direction: row;
  margin-bottom: 2px;
  user-select: none; /* prevent text selection during shift-click */
}

.BlogPostListViewItem--selected {
  @apply text-blue-400;
}

.BlogPostListViewItem--highlighted {
  text-decoration: underline;
  @apply font-bold;
}
```

`user-select: none` on the item is important — without it, shift-click range selection highlights text instead of selecting items.

---

## Checklist

- [ ] ListView: `isLoading(props.items)` guard renders `<XxxLoader>` before mapping items
- [ ] ListView: `SelectionUIConnector` and `createSelectionKeyHandlers` instantiated inside component body (after loading guard)
- [ ] ListView: `selectionUIConnector.handle(item.id)` passed as `selectionUIProps` to each item
- [ ] ListView: list `div` has `tabIndex={1}` so keyboard events fire
- [ ] ListView: `KeyboardEventHandler` wraps the list with `handleKeys={R.keys(keyHandlers)}` and `onKeyEvent={createKeyDownHandler(keyHandlers)}`
- [ ] ListView: selected/highlighted state passed as className object to each item
- [ ] ListView: `SelectionUIConnector` / `KeyboardEventHandler` omitted when selection is not needed
- [ ] ListViewItem: `selectionUIHandlers(props.selectionUIProps)` merged via `mergeProps`, not spread directly
- [ ] ListViewItem: navigation `onClick` guards against `ctrlKey || shiftKey`
- [ ] ListViewItem: `isUpdating(props.item)` drives the `animate-delete` class
- [ ] ListViewItem scss: `user-select: none` set to prevent text selection on shift-click
- [ ] ListViewItem scss: `--selected` and `--highlighted` modifier classes defined
