# Skill: fe-add-api-hooks

Applies when adding API communication for a feature: writing query hooks and mutation hooks. After writing these, also write their fake endpoints — see the `fe-write-workflow-tests` skill.

See the `fe-add-model` skill for the `XT.ts` and `XSchema.ts` files that the hooks import.

---

## File locations

```
api/
  queries/
    use<QueryName>.ts      ← query hook + query function + invalidate helper
  mutations/
    use<MutationName>.ts   ← mutation hook + mutation function
```

Primary reference: `blogs_fe/src/api/queries/useGetBlogPosts.ts`, `blogs_fe/src/api/mutations/useCreateBlogPost.ts`

---

## 1. Query hooks — `api/queries/use<QueryName>.ts`

Reference: `blogs_fe/src/api/queries/useGetBlogPosts.ts`

### Structure

```ts
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';
import { queryClient } from '/src/api/queryClient';
import { get } from '/src/api/restClient';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { createQueryKey } from '/src/api/utils/createQueryKey';
import { parseResponse } from '/src/api/utils/parseResponse';
import { generatePath } from '/src/routes/utils';
import { waitOnDev } from '/src/utils/wait';

export type GetBlogPostsArgsT = {
  blogSlug: string;
};
export type OptionsT = {
  enabled?: boolean;
};

export type GetBlogPostsQueryKeyT = GetBlogPostsArgsT;
export function getBlogPostsQueryKey(args: GetBlogPostsQueryKeyT) {
  return createQueryKey<GetBlogPostsQueryKeyT>('getBlogPosts', args);
}

export const getBlogPostsUrl = '/blogs/:blogSlug/blog-posts/list/';

export const getBlogPosts = (args: GetBlogPostsArgsT) => {
  return get(generatePath(getBlogPostsUrl, { blogSlug: args.blogSlug })).then(
    (response) => {
      const res = parseResponse(z.array(BlogPostSchema), response.data);
      return waitOnDev(100, { blogPosts: res });
    }
  );
};

export const useGetBlogPosts = (args: GetBlogPostsArgsT, options?: OptionsT) => {
  return useQuery({
    queryKey: getBlogPostsQueryKey(args),
    queryFn: () => getBlogPosts(args),
    enabled: !!(options?.enabled ?? true),
  });
};

export const invalidateGetBlogPosts = (args: GetBlogPostsQueryKeyT) => {
  return queryClient.invalidateQueries({ queryKey: getBlogPostsQueryKey(args) });
};
```

### Key rules

- **`XxxUrl` constant** — define the URL string as a constant. Use `:param` tokens for path parameters.
- **`generatePath`** — use to expand `:param` tokens before calling `get(...)`.
- **`parseResponse(schema, data)`** — always validate the response against the Zod schema before returning.
- **`waitOnDev(ms, data)`** — wrap the return value; simulates network latency in dev without affecting production.
- **`getBlogPostsQueryKey`** — export the query key function; mutations import it to invalidate the cache after a write.
- **`invalidateXxx`** — export an invalidate helper; mutations call it in `onSuccess`.
- **`OptionsT` with `enabled`** — add when the query depends on another resource being loaded first (e.g. blog posts can only be fetched once a blog is selected). The `enabled: !!(options?.enabled ?? true)` pattern defaults to enabled.
- **Response shape** — wrap the parsed array/object in a named property (e.g. `{ blogPosts: res }`) so the call site accesses `getBlogPosts.data?.blogPosts` rather than `getBlogPosts.data` directly. This makes the shape explicit and extensible.

### Query hook used via `useObservableQuery`

In `useXState.ts`, queries are wrapped in `useObservableQuery` (not called directly):

```ts
const getBlogPosts = useObservableQuery(
  useGetBlogPosts(
    { blogSlug: props.getBlog()?.slug ?? '' },
    { enabled: !!props.getBlog() }
  ),
  { fetchAsLoad: true, debugLabel: 'getBlogPosts' }
);
```

The query hook itself (`useGetBlogPosts`) does not call `useObservableQuery` — that wrapping happens one level up in the state hook.

---

## 2. Mutation hooks — `api/mutations/use<MutationName>.ts`

Reference: `blogs_fe/src/api/mutations/useCreateBlogPost.ts`

### Structure

```ts
import snakecaseKeys from 'snakecase-keys';
import { useObservableMutation } from '/src/api/lib/ObservableMutation';
import { invalidateGetBlogPosts } from '/src/api/queries/useGetBlogPosts';
import { post } from '/src/api/restClient';
import { BlogPostSchema } from '/src/api/types/BlogPostSchema';
import { BlogT } from '/src/api/types/BlogT';
import { parseResponse } from '/src/api/utils/parseResponse';
import { ObjT } from '/src/utils/types';
import { waitOnDev } from '/src/utils/wait';

export type CreateBlogPostArgsT = {
  blog: BlogT;
  createBlogPostForm: {
    title: string;
    content: string;
  };
};

export const createBlogPost = (args: CreateBlogPostArgsT) => {
  const url = `/blogs/${args.blog.id}/blog-posts/create/`;
  return post(url, {
    create_blog_post_form: snakecaseKeys(args.createBlogPostForm),
    blogId: args.blog.id,
  })
    .then((response) => {
      const res = parseResponse(BlogPostSchema, response);
      return waitOnDev(1000, res);
    })
    .catch((error) => {
      const errorCodes = error.response.data;
      if (errorCodes.includes('BLOG_NOT_FOUND')) {
        return waitOnDev(1000, { success: false });
      }
      throw error;
    });
};

export const useCreateBlogPost = () => {
  return useObservableMutation({
    mutationFn: createBlogPost,
    onSuccess: (response: ObjT, args: CreateBlogPostArgsT) => {
      invalidateGetBlogPosts({ blogSlug: args.blog.slug });
    },
  });
};
```

### Key rules

- **`useObservableMutation`** — always use this instead of tanstack-query's `useMutation` directly. It wraps the result in a MobX-observable object so that `isRunning(mutation)` works in the StateProvider's `updateSources`.
- **`snakecaseKeys`** — use to convert camelCase form keys to snake_case before posting. The server expects snake_case; the frontend works in camelCase.
- **`post(url, body)`** — the `post` function from `restClient` does not convert keys automatically; apply `snakecaseKeys` manually on the form payload.
- **`onSuccess` → invalidate** — always invalidate the relevant query cache in `onSuccess` so the list refreshes after a write.
- **`parseResponse`** — validate the response when the mutation returns entity data (e.g. create returning the new entity). Omit for mutations that return no meaningful body.
- **`waitOnDev`** — wrap the return value for realistic dev latency.
- **Error handling** — catch known server error codes and return a structured failure value; re-throw unknown errors.
- **No URL constant needed** — mutations POST to dynamic URLs (containing entity ids). If the URL is static, define it the same way query hooks do.

---

## Checklist

- [ ] Query hook: `XxxUrl` constant defined
- [ ] Query hook: `parseResponse(schema, data)` validates the response
- [ ] Query hook: `waitOnDev(ms, data)` wraps the return value
- [ ] Query hook: `getBlogPostsQueryKey` and `invalidateXxx` exported for mutations
- [ ] Query hook: `OptionsT` with `enabled` added when query depends on another resource
- [ ] Query hook: response shape wraps array/object in a named property
- [ ] Mutation hook: uses `useObservableMutation`, not `useMutation`
- [ ] Mutation hook: `snakecaseKeys` applied to form payloads before posting
- [ ] Mutation hook: `onSuccess` invalidates the relevant query cache
- [ ] Fake endpoint written for every query and mutation — see `fe-write-workflow-tests` skill
