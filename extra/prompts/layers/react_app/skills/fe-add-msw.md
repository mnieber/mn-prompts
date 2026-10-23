# Skill: fe-add-msw

Applies when adding or updating MSW (Mock Service Worker) mock handlers for a query or mutation. MSW intercepts HTTP requests in the browser so the app can run fully in isolation — local dev, Storybook, and tests all work without a real backend.

See the `fe-add-api-hooks` skill for the query/mutation hook files that MSW handlers mirror.
See the `fe-add-storybook` skill for how to wire handlers into Storybook stories.

---

## File structure

```
mocks/
  queries/
    handle<QueryName>.ts       ← MSW GET handler
  mutations/
    handle<MutationName>.ts    ← MSW POST handler
  browser/
    index.ts                   ← registers all handlers with setupWorker
    defaultPassthrough/
      index.ts                 ← passthrough handlers for fonts, source maps, etc.
```

Primary reference: `blogs_fe/src/mocks/queries/handleGetBlogs.ts`, `blogs_fe/src/mocks/queries/handleGetBlogPosts.ts`
Secondary reference: `woodstock_ui/src/mocks/queries/handleQueryTraces.ts`

---

## Rule: every query and mutation needs a handler

Every query hook and every mutation hook must have a corresponding MSW handler. This ensures the app can always run in isolation without a real backend.

---

## 1. Query handler — `mocks/queries/handle<QueryName>.ts`

```ts
import { http, HttpResponse } from 'msw';
import { getBlogPostsUrl } from '/src/api/queries/useGetBlogPosts';
import { hostUrl } from '/src/api/restClient';
import { createBlogPost } from '/src/api/types/BlogPostT';
import { joinUrls } from '/src/utils/urls';

export const handleGetBlogPosts = http.get(
  joinUrls(hostUrl, getBlogPostsUrl),
  () => {
    return HttpResponse.json([
      createBlogPost({ title: 'First Post', slug: 'first-post', content: 'One' }),
      createBlogPost({ title: 'Second Post', slug: 'second-post', content: 'Two' }),
    ]);
  }
);
```

### Key rules

- **Import `XxxUrl`** from the query hook file — never duplicate the URL string.
- **`joinUrls(hostUrl, url)`** — use to build the full URL that MSW will intercept. MSW matches `:param` tokens as wildcards, so parameterised URLs (e.g. `/blogs/:blogSlug/blog-posts/list/`) work without special handling.
- **`create<Name>(...)`** — use factory functions from the model type file (see `fe-add-model` skill) to build realistic fixture data with resource-state initialised.
- **`http.get(...)`** — always `http.get` for query handlers.

### Handler with query-parameter filtering

When the endpoint accepts query parameters that affect results, read them from `request.url` and filter the fixture data:

```ts
export const handleQueryTraces = http.get(
  joinUrls(hostUrl, queryTracesUrl),
  ({ request }) => {
    const url = new URL(request.url);
    const traceKeyPrefix = url.searchParams.get('trace_key_prefix');

    let filtered = [...mockTraces];
    if (traceKeyPrefix) {
      filtered = filtered.filter(t => t.traceKey.startsWith(traceKeyPrefix));
    }

    return HttpResponse.json({ items: filtered });
  }
);
```

Reference: `woodstock_ui/src/mocks/queries/handleQueryTraces.ts`

---

## 2. Mutation handler — `mocks/mutations/handle<MutationName>.ts`

```ts
import { http, HttpResponse } from 'msw';
import { hostUrl } from '/src/api/restClient';
import { getBlogTagsUrl } from '/src/api/mutations/useGetBlogTags';

export const handleGetBlogTags = http.post(
  `${hostUrl}${getBlogTagsUrl}*`,
  () => {
    return HttpResponse.json({ tags: ['sports', 'music'] });
  }
);
```

Reference: `blogs_fe/src/mocks/mutations/handleGetBlogTags.ts`

- **`http.post(...)`** — always `http.post` for mutation handlers.
- Return a plausible response shape matching what the mutation's `parseResponse` expects (if it validates the response).
- For mutations with dynamic URL segments (entity ids), append `*` to match any suffix.

---

## 3. Registering handlers — `mocks/browser/index.ts`

Import and add every new handler to the `handlers` array. Always spread `passthroughHandlers` last:

```ts
import { setupWorker } from 'msw/browser';
import { handleGetBlogs }     from '/src/mocks/queries/handleGetBlogs';
import { handleGetBlogPosts } from '/src/mocks/queries/handleGetBlogPosts';
import { handleGetBlogTags }  from '/src/mocks/mutations/handleGetBlogTags';
import { passthroughHandlers } from './defaultPassthrough';

export const handlers = [
  handleGetBlogs,
  handleGetBlogPosts,
  handleGetBlogTags,
  ...passthroughHandlers,
];

export const worker = setupWorker(...handlers);
```

Reference: `blogs_fe/src/mocks/browser/index.ts`

`passthroughHandlers` passes through unmatched requests (fonts, source maps, Vite HMR, etc.) so MSW doesn't error on them.

---

## 4. Enabling MSW in `main.tsx`

MSW is activated at startup via the `enableMocking()` function in `main.tsx`. It runs only in non-production environments and only when `flags.useMsw` is set to `true`:

```ts
const isProduction = process.env.NODE_ENV === 'production';

async function enableMocking(): Promise<void> {
  if (isProduction || !flags.useMsw) {
    return;
  }
  const { worker } = await import('./mocks/browser');
  await worker.start();
}

enableMocking().then(() => {
  ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
    .render(<App />);
});
```

Reference: `blogs_fe/src/main.tsx`, `woodstock_ui/src/main.tsx`

The app is rendered inside the `.then()` callback so that the Service Worker is registered and ready before the first request fires.

### `flags.useMsw`

`flags` is a MobX observable in `app/flags.ts`. Set `useMsw: true` locally to activate MSW for a dev session. It defaults to `false` so production builds are never intercepted:

```ts
export const flags = observable({
  useMsw: false,   // set to true locally to enable MSW
  // ...
});
```

Reference: `blogs_fe/src/app/flags.ts`

---

## Checklist

- [ ] One handler file per query (`mocks/queries/`) and per mutation (`mocks/mutations/`)
- [ ] Query handler: imports `XxxUrl` from the hook file; uses `joinUrls(hostUrl, url)`
- [ ] Query handler: uses `create<Name>(...)` factories for fixture data
- [ ] Query handler: filters on query params when the endpoint supports them
- [ ] Mutation handler: uses `http.post(...)`; appends `*` for dynamic URL segments
- [ ] All handlers registered in `mocks/browser/index.ts` with `passthroughHandlers` spread last
- [ ] `main.tsx`: `enableMocking()` wraps `ReactDOM.createRoot` in `.then()`
- [ ] `main.tsx`: MSW only starts when `!isProduction && flags.useMsw`
