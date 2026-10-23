# Skill: fe-add-app-component

Applies when writing or updating `App.tsx` — the root component that composes all providers, the `AppBody` shell, and the top-level Switch components into a single tree.

---

## File location

```
app/components/App.tsx
```

Primary reference: `blogs_fe/src/app/components/App.tsx`
Secondary reference: `woodstock_ui/src/app/components/App.tsx`

---

## Structure

```tsx
import { QueryClientProvider } from '@tanstack/react-query';
import * as R from 'ramda';
import { queryClient } from '/src/api/queryClient';
import { AuthStateProvider } from '/src/auth/components/AuthStateProvider';
import { AuthSwitch } from '/src/auth/components/AuthSwitch';
import { BlogPostsStateProvider } from '/src/blogPosts/components/BlogPostsStateProvider';
import { BlogsStateProvider } from '/src/blogs/components/BlogsStateProvider';
import { BlogsSwitch } from '/src/blogs/components/BlogsSwitch';
import { DashboardFrame } from '/src/frames/components/DashboardFrame';
import { L } from '/src/frames/layout';
import { NavStateProvider } from '/src/routes/components/NavStateProvider';
import { cn } from '/src/utils/classnames';

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthStateProvider>
        <NavStateProvider>
          <AppBody>
            <DashboardFrame>
              <AuthSwitch />
              <BlogsStateProvider>
                <BlogPostsStateProvider>
                  <BlogsSwitch />
                </BlogPostsStateProvider>
              </BlogsStateProvider>
            </DashboardFrame>
          </AppBody>
        </NavStateProvider>
      </AuthStateProvider>
    </QueryClientProvider>
  );
};

const AppBody = (props: React.PropsWithChildren<{}>) => {
  return (
    <div
      id="App"
      className={cn('App', [
        R.values({
          root: L.col.banner(),
          size: `min-width-[320px] h-screen max-w-[1600px]`,
          pos: `mx-auto`,
          scroll: 'overflow-x-hidden',
        }),
      ])}
      tabIndex={0}
      ref={(x: any) => x?.focus()}
    >
      {props.children}
    </div>
  );
};
```

---

## Providers

Providers supply MobX state to the component subtree beneath them. Two rules govern their placement:

1. **High enough** — a provider must wrap every component that consumes its context. Providers needed app-wide (e.g. `QueryClientProvider`, `AuthStateProvider`) go at the top.
2. **No higher than necessary** — a provider that is only needed within one section of the UI should wrap only that section. For example, `BlogPostsStateProvider` only wraps the components that need blog-post state.

Don't over-think provider placement — it is easy to adjust later and the spec owner will correct it if needed.

### Fixed outer providers (always present)

| Provider | Purpose |
|---|---|
| `QueryClientProvider` | tanstack-query client; outermost |
| `AuthStateProvider` | authentication state; needed app-wide |
| `NavStateProvider` | nav-point history for restore-on-cancel |

### Feature providers

Each feature module's `XStateProvider` wraps the Switch (and any other components) that consume that state. Nest them to reflect data dependencies — e.g. `BlogPostsStateProvider` is nested inside `BlogsStateProvider` because blog-posts depend on the currently selected blog.

---

## `AppBody`

`AppBody` is a small private component that provides the root `<div>` shell: full viewport height, horizontal scroll suppressed, auto-focused on mount so keyboard events are immediately captured. Extract it to keep `App` readable. Always include:

- `id="App"` — used by E2E tests and dev tools
- `tabIndex={0}` — makes the root focusable
- `ref={(x) => x?.focus()}` — focuses on mount so `KeyboardEventHandler` in list views fires immediately

Use `L.col.banner()` from `frames/layout.ts` as the root layout class.

---

## Switches

Switch components group a module's routes into a single object to avoid bloating `App`. Each module that has routes contributes one Switch component (e.g. `BlogsSwitch`, `AuthSwitch`, `TracesSwitch`). Render Switches inside the providers they depend on, and inside the frame component that provides the page shell.

---

## Checklist

- [ ] `QueryClientProvider` is the outermost provider
- [ ] App-wide providers (`AuthStateProvider`, `NavStateProvider`) wrap the full tree
- [ ] Feature `XStateProvider`s wrap only the subtree that needs them
- [ ] Provider nesting reflects data dependencies (dependent providers nested inside their dependencies)
- [ ] `AppBody` is extracted as a private component with `id="App"`, `tabIndex={0}`, and `ref` auto-focus
- [ ] Each feature module with routes contributes a Switch component rendered inside the relevant providers
