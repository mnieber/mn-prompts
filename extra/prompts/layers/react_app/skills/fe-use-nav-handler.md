# Skill: fe-use-nav-handler

Applies when adding navigation routes to a feature module: writing the `routes.ts` file, registering it in `createNavHandler.ts`, declaring route paths for `<Route>` components in Switch files, and calling `navTo(...)` from components and form handlers.

---

## Overview

The routing system has three layers:

1. **`<module>/routes.ts`** — declares URL patterns, the `Nav` class (delegates to `navHandler`), the `DefaultNav` handler (produces concrete URLs), and a singleton `moduleNav` instance
2. **`routes/createNavHandler.ts`** — registers all `DefaultNav` handlers into the global `navHandler` singleton at app startup
3. **Switch components + `navTo` call sites** — consume route patterns and the `moduleNav` singleton

Primary reference: `blogs_fe/src/blogs/routes.ts`, `blogs_fe/src/blogPosts/routes.ts`

---

## 1. `<module>/routes.ts`

Each module has exactly one `routes.ts` at the module root.

### Structure

```ts
import { history } from "/src/routes/history";
import { navHandler, RouteSpecT } from "/src/routes/navHandler";
import { generatePath } from "/src/routes/utils/generatePath";

// 1. Route patterns — used by <Route path={...}> in Switch components
export const blogsRoutes = {
  blog: () => "/blogs/:blogSlug",
  blogs: () => "/blogs",
  createBlog: () => "/blogs/create/_",
};

// 2. Nav class — defines the routing interface; delegates to the global navHandler
export class BlogsNav {
  blog(params: { blogSlug: string }, callerId?: string): RouteSpecT {
    return navHandler().run("blog", params, callerId);
  }
  blogs(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run("blogs", params, callerId);
  }
  createBlog(params: {}, callerId?: string): RouteSpecT {
    return navHandler().run("createBlog", params, callerId);
  }
}

// 3. DefaultNav — implements the interface with concrete URLs
export class DefaultBlogsNavHandler extends BlogsNav {
  blog(params: { blogSlug: string }, callerId?: string) {
    return { url: generatePath(blogsRoutes.blog(), params), nav: history.push };
  }
  blogs(params: {}, callerId?: string) {
    return {
      url: generatePath(blogsRoutes.blogs(), params),
      nav: history.push,
    };
  }
  createBlog(params: {}, callerId?: string) {
    return {
      url: generatePath(blogsRoutes.createBlog(), params),
      nav: history.push,
    };
  }
}

// 4. Singleton — imported by every call site that needs to navigate
export const blogsNav = new BlogsNav();
```

### Key rules

- **`blogsRoutes`** — a plain object of zero-argument functions returning path strings. Parameters use the `:paramName` convention. Always export it; Switch components import it directly to avoid duplicating path strings.
- **`BlogsNav`** — delegates every method to `navHandler().run(routeName, params, callerId)`. The route name string must match the method name exactly.
- **`DefaultBlogsNavHandler extends BlogsNav`** — overrides each method to return `{ url, nav }`. Uses `generatePath(pattern, params)` for parameterised routes.
- **`nav: history.push`** — always `history.push` for a normal navigation. Use `history.replace` only if the spec calls for a replace-style redirect.
- **Singleton `blogsNav`** — one instance per module. Never instantiate `BlogsNav` at call sites.

### When params aren't `:param` tokens

If the URL needs query-string params (not path params), build the suffix manually in the `DefaultNav` method rather than passing them through `generatePath`:

```ts
signIn(params: { nextUrl?: string }, callerId?: string) {
  const suffix = params.nextUrl ? '?nextUrl=' + encodeURIComponent(params.nextUrl) : '';
  return { url: generatePath(authRoutes.signIn(), {}) + suffix, nav: history.push };
}
```

Reference: `blogs_fe/src/auth/routes.ts`

---

## 2. `routes/createNavHandler.ts`

This file constructs the global `navHandler` singleton by registering all `DefaultNav` handlers. Add one `installDefaultNavHandler` call per module.

```ts
import { DefaultAuthNavHandler } from "/src/auth/routes";
import { DefaultBlogPostsNavHandler } from "/src/blogPosts/routes";
import { DefaultBlogsNavHandler } from "/src/blogs/routes";
import { NavHandler } from "/src/routes/navHandler";

export const createNavHandler = () => {
  const navHandler = new NavHandler();
  navHandler.installDefaultNavHandler(new DefaultBlogsNavHandler());
  navHandler.installDefaultNavHandler(new DefaultBlogPostsNavHandler());
  navHandler.installDefaultNavHandler(new DefaultAuthNavHandler());
  return navHandler;
};
```

Reference: `blogs_fe/src/routes/createNavHandler.ts`

Every time a new module is added, its `DefaultXxxNavHandler` must be registered here.

---

## 3. Switch components — consuming route patterns

Switch components use `<Route path={...}>` from `wouter`. They import route patterns from `<module>/routes.ts` and the `ext()` helper from `navHandler`.

### `ext()` — matching a route and all its children

`ext(pattern)` appends `/*?` to a path, making it match the route itself and any deeper paths. Use it on the outer `<Route>` of a nested group:

```tsx
import { ext } from "/src/routes/navHandler";
import { tracesRoutes } from "/src/traces/routes";

<Switch>
  <Route path={ext(tracesRoutes.traces())}>
    {" "}
    {/* matches /traces and /traces/... */}
    <TraceExplorerView />
    <Route path={tracesRoutes.trace()}>
      {" "}
      {/* matches /traces/* only */}
      <SelectTraceEffect />
    </Route>
  </Route>
</Switch>;
```

Reference: `blogs_fe/src/blogs/components/BlogsSwitch.tsx`

### Switch file location

A Switch component lives in `<module>/components/<Module>Switch.tsx`. It is rendered by `App.tsx` (or a parent Switch) and groups all routes belonging to that module.

---

## 4. Navigating — `navTo` at call sites

Import the module singleton and call `navTo(moduleNav.routeName(params))`:

```ts
import { navTo } from "/src/routes/navHandler";
import { blogPostsNav } from "/src/blogPosts/routes";

// inside a form submit handler or button click:
navTo(
  blogPostsNav.blogPost({
    blogSlug: props.blog.slug,
    blogPostSlug: response.data.slug,
  })
);
```

`navTo` simply calls `routeSpec.nav(routeSpec.url)`. Never call `history.push` directly from components — always go through the `Nav` singleton so that specialized nav handlers installed later can override the behaviour.

### `RedirectEffect` — declarative nav inside JSX

When a redirect must be driven by component state (not an event), use `RedirectEffect`:

```tsx
import { RedirectEffect } from "/src/routes/components/RedirectEffect";

<Route path={framesRoutes.dashboard()}>
  <RedirectEffect
    getRoute={() => {
      if (props.blogsHighlight.item) {
        return blogsNav.blog({ blogSlug: props.blogsHighlight.item.slug });
      }
      return undefined; // returning undefined suppresses the redirect
    }}
  />
</Route>;
```

`RedirectEffect` calls `getRoute()` on each render and calls `navTo` in a `useEffect` whenever the result is defined.

Reference: `blogs_fe/src/blogs/components/BlogsSwitch.tsx`, `blogs_fe/src/routes/components/RedirectEffect.tsx`

---

## Checklist

- [ ] `routes.ts`: `XxxRoutes` object exports one zero-argument function per route
- [ ] `routes.ts`: `XxxNav` method names match the strings passed to `navHandler().run(...)`
- [ ] `routes.ts`: `DefaultXxxNavHandler extends XxxNav` and overrides every method
- [ ] `routes.ts`: each `Default` method returns `{ url, nav: history.push }`
- [ ] `routes.ts`: singleton `xxxNav = new XxxNav()` exported at the bottom
- [ ] `createNavHandler.ts`: new module's `DefaultXxxNavHandler` registered with `installDefaultNavHandler`
- [ ] Switch component: outer nested route uses `ext(pattern)`, inner routes use the plain pattern
- [ ] Call sites: `navTo(xxxNav.route(params))` — never `history.push` directly
- [ ] `RedirectEffect` used for state-driven redirects inside JSX, not `useEffect` + `history.push`
