# Skill: fe-add-model

Applies when defining a new data model: writing the `XT.ts` type file and the `XSchema.ts` Zod schema file. These two files always go together. Queries and mutations that use the type are covered by the `fe-add-api-hooks` skill.

---

## File locations

Both files live in `api/types/`:

```
api/types/
  <Name>T.ts       ← TypeScript type + create factory function
  <Name>Schema.ts  ← Zod schema that validates API responses
```

Types live in `api/types/` even when they are only used by a single feature module, because types tend to be imported across module boundaries (by queries, mutations, state, and components alike).

Primary reference: `blogs_fe/src/api/types/BlogPostT.ts` + `BlogPostSchema.ts`
Secondary references: `blogs_fe/src/api/types/BlogT.ts`

---

## 1. `<Name>T.ts` — the TypeScript type

### Entity models (have an `id`)

Use the `EntityT` mixin for any model that has a server-assigned id:

```ts
import { initRS } from "mobx-resource-states";
import { EntityT } from "/src/api/types/EntityT";
import { createUUID } from "/src/utils/ids";
import { ObjT } from "/src/utils/types";

export type BlogPostT = EntityT & {
  title: string;
  content: string | undefined;
  slug: string;
  isPublished: boolean;
  level: BlogPostLevelT;
  isTransient?: boolean; // present on transient (unsaved) instances
};

export type BlogPostLevelT = "easy" | "medium" | "hard";

export type BlogPostByIdT = { [id: string]: BlogPostT }; // add when a lookup map is needed

export const createBlogPost = (values: ObjT): BlogPostT => {
  return initRS({
    id: values.id ?? createUUID(),
    title: values.title ?? "New blog-post",
    slug: values.slug ?? "-",
    content: values.content,
    isPublished: values.isPublished ?? false,
    level: values.level ?? "medium",
    isTransient: true,
  } as BlogPostT);
};
```

Reference: `blogs_fe/src/api/types/BlogPostT.ts`

### Key rules

- **`T` suffix** — every exported TypeScript type ends in `T` (e.g. `BlogPostT`, `BlogPostLevelT`).
- **`EntityT` mixin** — always extend `EntityT` for models that have a server-assigned `id` field.
- **`isTransient?: boolean`** — include on entity types that support transient (unsaved) instances created via the `Addition` facet.
- **`create<Name>` factory** — required for every entity type. It constructs a transient instance with sensible defaults, and calls `initRS(...)` to initialise the resource-state tracking used by `isLoading`/`isUpdating` in the view layer.
- **`initRS`** — always wrap the returned object. Without it, `updateSources` in the StateProvider cannot attach loading/updating state to newly created instances.
- **`createUUID()`** — use for the transient `id`; it will be replaced by the server-assigned id after the entity is saved.
- **Union types** — define named union types (e.g. `BlogPostLevelT`) alongside the main type in the same file.
- **`<Name>ByIdT`** — add when the State's Data facet needs a lookup map (i.e. `blogPostById`). Omit otherwise.

### Optional: option-loader functions

If a field uses a `ValuePickerField` with a static option set, export the loader alongside the type:

```ts
export const getBlogPostLevelOptions = (args: {}) => {
  return Promise.resolve([
    { value: "easy", label: "Easy" },
    { value: "medium", label: "Medium" },
    { value: "hard", label: "Hard" },
  ]);
};
```

Reference: `blogs_fe/src/api/types/BlogPostT.ts`

---

## 2. `<Name>Schema.ts` — the Zod schema

The schema validates the raw API response before it reaches the rest of the app. It must match the TypeScript type exactly — Zod's `z.ZodType<NameT>` annotation enforces this at compile time.

### Entity schema

```ts
import { z } from "zod";
import { BlogPostT } from "/src/api/types/BlogPostT";
import { EntitySchema } from "/src/api/types/EntitySchema";

export const BlogPostSchema: z.ZodType<BlogPostT> = z.object({
  ...EntitySchema.shape, // spreads in { id: z.string() }
  title: z.string(),
  content: z.string(),
  slug: z.string(),
  isPublished: z.boolean(),
  level: z.union([z.literal("easy"), z.literal("medium"), z.literal("hard")]),
  isTransient: z.boolean().optional(),
});
```

Reference: `blogs_fe/src/api/types/BlogPostSchema.ts`

### Key rules

- **`z.ZodType<NameT>` annotation** — always declare the type parameter. This makes TypeScript report a compile error when the schema drifts from the type.
- **`...EntitySchema.shape`** — spread into entity schemas instead of repeating `id: z.string()`.
- **`optional()`** — use for fields typed as `X | undefined` or `X?` in the TypeScript type.
- **No `create` function here** — the schema file only validates; construction belongs in `XT.ts`.

---

## 3. Exporting from `api/types/index.ts`

Add the new type (not the schema) to the barrel export:

```ts
// api/types/index.ts
export { type BlogPostT } from "./BlogPostT";
export { type BlogT } from "./BlogT";
```

Only types are re-exported from `index.ts`; schemas are imported directly by the files that need them (query hooks, MSW handlers).

---

## Checklist

- [ ] `XT.ts`: type name ends in `T`; extends `EntityT` if the model has an `id`
- [ ] `XT.ts`: `isTransient?: boolean` present when the model supports transient instances
- [ ] `XT.ts`: `create<Name>` factory calls `initRS(...)` and uses `createUUID()` for the id
- [ ] `XT.ts`: union sub-types also end in `T` and are defined in the same file
- [ ] `XSchema.ts`: annotated as `z.ZodType<XT>` to enforce type/schema alignment
- [ ] `XSchema.ts`: spreads `...EntitySchema.shape` for entity models
- [ ] `XSchema.ts`: every optional TypeScript field uses `.optional()` in the schema
- [ ] `api/types/index.ts`: new type exported from the barrel (schemas are not barrel-exported)
