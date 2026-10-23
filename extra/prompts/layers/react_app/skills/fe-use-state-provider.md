# Skill: fe-use-state-provider

Applies when the React app must provide state to a collection of components in the View layer. A feature module may provide more than 1 type of state. Per type of state (e.g. BlogsState, or BlogPostsState) it provides: the `XState.ts` class, the `useXState.ts` hook, the `XStateProvider.tsx` component, and the `useXContext.ts` context file. These four files always go together and form the complete state wiring for one type of state.

---

## Overview of the four files

```
<module>/
  <Name>State/
    <Name>State.ts          ← State class: containers + child facet instances + props + actionsCtr
    register<Name>Ctr.ts    ← wires facets together (mapData only)
    facets/
      <Name>Data.ts         ← custom Data facet (one per container that needs it)
      <Name>Addition.ts     ← child class extending Addition<T> (if needed)
      <Name>Deletion.ts     ← child class extending Deletion<T> (if needed)
      <Name>Edit.ts         ← child class extending Edit (if needed)
      <Name>Selection.ts    ← child class extending Selection<T> (if needed)
      <Name>Insertion.ts    ← child class extending Insertion<T> (if needed)
      ... other child facets as needed
  hooks/
    use<Name>State.ts       ← React hook: queries/mutations + State construction
    use<Name>Context.ts     ← React context + typed selector object (<name>Ctx)
  components/
    <Name>StateProvider.tsx ← observer component: creates state, cache, provides context
```

Primary reference: `blogs_fe/src/blogPosts/` (BlogPostsState, useBlogPostsState, BlogPostsStateProvider, useBlogPostsContext)

---

## 1. `<Name>State.ts` — the State class

Reference: `blogs_fe/src/blogPosts/BlogPostsState/BlogPostsState.ts`

The State class owns the data and behavioural containers for one module resource.

### Structure

```ts
export type PropsT = {
  // Hook functions connecting State to the outside world
  getBlogPosts: () => BlogPostT[];
  deleteBlogPosts: (ids: string[]) => Promise<any>;
  saveBlogPost: (values: ObjT) => Promise<any>;
};

export class BlogPostsState {
  props: PropsT;

  // One container object per resource; each field is a child facet instance
  // Child facets receive `this` as constructor argument for full state access
  blogPostsCtr = {
    data: new BlogPostsData(),
    addition: new BlogPostsAddition(this),
    deletion: new BlogPostsDeletion(this),
    edit: new BlogPostsEdit(this),
    highlight: new Highlight<BlogPostT>(), // reusable facets that need no customization
    selection: new BlogPostsSelection(this),
  };

  // Optional: simple direct actions that don't warrant a full facet
  actionsCtr = {
    markBlogPostAsPublished: (blogPostId: string) => {
      return this.props.markBlogPostAsPublished(blogPostId);
    },
  };

  destroy() {
    Skandha.cleanUpCtr(this);
  }

  constructor(props: PropsT) {
    this.props = props;
    bindActionsCtr(this.actionsCtr, this); // omit if no actionsCtr
    registerBlogPostsCtr(this);
  }
}
```

### Key rules

- `props` holds hook functions, not raw data. The State never calls React hooks itself.
- Each container is a plain object (`blogPostsCtr = { ... }`). Multiple containers are allowed when the module manages more than one resource.
- The `destroy()` method calls `Skandha.cleanUpCtr(this)` — always include it.
- Omit `actionsCtr` when all interactions go through facets.
- If an action is too complex to inline, extract it to a lib file (e.g. `blogPosts/lib/reformatBlogPost.ts`) and call it from `actionsCtr`.

### Facets

Facets (from `skandha-facets`) are the standard building blocks for resource meta-state. Common ones:

| Facet       | Purpose                                              | Customization approach                                              |
| ----------- | ---------------------------------------------------- | ------------------------------------------------------------------- |
| `Data`      | custom; stores the resource list and derived lookups | Always custom (no parent in skandha-facets)                         |
| `Addition`  | transient-instance creation flow                     | Create child class extending `Addition<T>`                          |
| `Deletion`  | deletion flow                                        | Create child class extending `Deletion<T>` or `DeletionWithFlag<T>` |
| `Edit`      | edit/save flow                                       | Create child class extending `Edit`                                 |
| `Highlight` | single highlighted item                              | Use directly (rarely needs customization)                           |
| `Selection` | multi-select                                         | Create child class extending `Selection<T>`                         |
| `Insertion` | reordering items in a list                           | Create child class extending `Insertion<T>`                         |

The spec file states which facets a container needs. Use only what the spec requires.

### When to create child facet classes

Most reusable facets (Addition, Deletion, Edit, Selection, Insertion) need app-specific behavior. We use inheritance to implement callbacks (if needed) that wire facets together.

1. **Create a child class** in `<Name>State/facets/` that extends the parent facet from `skandha-facets`
2. **Pass `this` (the State instance)** to the child's constructor for full access to all state, props, and other facets
3. **Override protected methods** in the child class to implement app-specific behavior

**Do not override core facet methods** (like `delete()`, `add()`, `save()`, `selectItem()`) — these contain the workflow logic. Only override the **protected callback slots** that the parent provides.

Inheriting from a parent facet-class is often useful (because it leads to reusable solutions) but it's also fine to create the child facet class as a stand-alone class if this is more suitable.

### The Data facet

Each container that holds a list needs a custom Data class:

```ts
// facets/BlogPostsData.ts
export class BlogPostsData {
  static className = () => "BlogPostsData";

  @data blogPosts: BlogPostT[] = [];

  @data get blogPostById() {
    return R.indexBy(R.prop("id"), this.blogPosts);
  }
}
```

Reference: `blogs_fe/src/blogPosts/BlogPostsState/facets/BlogPostsData.ts`

### Example child facet classes

#### Addition example

```ts
// facets/BlogPostsAddition.ts
import { Addition } from "skandha-facets";
import { BlogPostT } from "/src/api/types";
import { BlogPostsState } from "/src/blogPosts/BlogPostsState";

export class BlogPostsAddition extends Addition<BlogPostT> {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected stageAdd(): void {
    this.parentId = this.state.blogPostsCtr.highlight.itemId;
  }

  protected highlightNewItem(item: BlogPostT): void {
    this.state.blogPostsCtr.selection.selectItem({ itemId: item.id });
    this.state.blogPostsCtr.edit.enable();
  }

  protected unstageAdd(parentId: string | undefined): void {
    this.state.blogPostsCtr.edit.cancel();
  }
}
```

Reference: `blogs_fe/src/blogPosts/BlogPostsState/facets/BlogPostsAddition.ts`

#### Deletion example

```ts
// facets/BlogPostsDeletion.ts
import { DeletionWithFlag } from "skandha-facets";
import { BlogPostT } from "/src/api/types";
import { BlogPostsState } from "/src/blogPosts/BlogPostsState";

export class BlogPostsDeletion extends DeletionWithFlag<BlogPostT> {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected deleteItems(args: {
    itemIds: string[];
    moveToTrash?: boolean;
  }): any {
    return this.state.props.deleteBlogPosts(args.itemIds);
  }
}
```

Reference: `blogs_fe/src/blogPosts/BlogPostsState/facets/BlogPostsDeletion.ts`

#### Edit example

```ts
// facets/BlogPostsEdit.ts
import { Edit } from "skandha-facets";
import { BlogPostsState } from "/src/blogPosts/BlogPostsState";
import { ObjT } from "/src/utils/types";

export class BlogPostsEdit extends Edit {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected saveItem(args: { values: any }): any {
    return this.state.props.saveBlogPost(args.values).then((response: ObjT) => {
      this.state.blogPostsCtr.addition.confirm();
      return response;
    });
  }

  protected onCancel(): void {
    this.state.blogPostsCtr.addition.cancel();
  }
}
```

Reference: `blogs_fe/src/blogPosts/BlogPostsState/facets/BlogPostsEdit.ts`

#### Selection example

```ts
// facets/BlogPostsSelection.ts
import { Selection, handleSelectItem } from "skandha-facets";
import { BlogPostT } from "/src/api/types";
import { BlogPostsState } from "/src/blogPosts/BlogPostsState";

export class BlogPostsSelection extends Selection<BlogPostT> {
  constructor(private state: BlogPostsState) {
    super();
  }

  protected performSelection(args: {
    itemId: string;
    isCtrl: boolean;
    isShift: boolean;
  }): void {
    handleSelectItem(this, args);
    if (!args.isCtrl && !args.isShift) {
      this.state.blogPostsCtr.highlight.set({ itemId: args.itemId });
    }
  }
}
```

Reference: `blogs_fe/src/blogPosts/BlogPostsState/facets/BlogPostsSelection.ts`

### Key facet patterns

- **Always pass the State reference**: `constructor(private state: BlogPostsState)`
- **Access other facets via state**: `this.state.blogPostsCtr.edit.cancel()`
- **Access props via state**: `this.state.props.deleteBlogPosts(args.itemIds)`
- **Override only protected methods**, never core operation methods
- **Reusable facets that need no customization** (like `Highlight`) can be instantiated directly without a child class

---

## 2. `register<Name>Ctr.ts` — wiring facets

Reference: `blogs_fe/src/blogPosts/BlogPostsState/registerBlogPostsCtr.ts`

This file wires the container's facets together using `mapDataToProps`, then registers everything with `registerCtr` from `skandha-mobx`.

### Structure

```ts
const mapData = (state: BlogPostsState) => {
  const ctr = state.blogPostsCtr;
  const getBlogPostById = (x: string | undefined) =>
    x ? ctr.data.blogPostById[x] : undefined;

  mapDataToProps(ctr, {
    data: {
      blogPosts: () => state.props.getBlogPosts(),
    },
    selection: {
      selectableIds: () => R.map(R.prop("id"), ctr.data.blogPosts),
      items: () =>
        ctr.selection.itemIds
          .map(getBlogPostById)
          .filter((x?: BlogPostT) => !!x) as BlogPostT[],
    },
    highlight: {
      highlightableIds: () => R.map(R.prop("id"), ctr.data.blogPosts),
      item: () => getBlogPostById(ctr.highlight.itemId),
    },
  });
};

export const registerBlogPostsCtr = (state: BlogPostsState) => {
  registerCtr({
    ctr: state.blogPostsCtr,
    options: { name: "BlogPostsState.BlogPosts" },
    initCtr: () => {
      mapData(state);
    },
  });
};
```

### Key rules

- **`mapData` only**: Wire computed/derived data properties into facets. No callback maps.
- **Structure mirrors the container**: Each top-level key in the object passed to `mapDataToProps` corresponds to a facet name in the container (e.g., `data`, `selection`, `highlight`).
- **Each facet's object contains getters**: The keys are the facet's property names; the values are getter functions.
- **Behavioral customization is in child classes**, not in this file.

---

## 3. `use<Name>State.ts` — the React hook

Reference: `blogs_fe/src/blogPosts/hooks/useBlogPostsState.ts`

This hook instantiates queries and mutations, constructs the State object, and returns them for use by the StateProvider.

### Structure

```ts
export const useBlogPostsState = (props: PropsT) => {
  const graftResourceStatesFromMemo = useGraftResourceStatesFromMemo({});

  // Mutations
  const deleteBlogPosts = useDeleteBlogPosts();

  // Queries
  const getBlogPosts = useObservableQuery(
    useGetBlogPosts({ blogSlug: props.getBlog()?.slug ?? '' }, { enabled: !!props.getBlog() }),
    { fetchAsLoad: true, debugLabel: 'getBlogPosts' }
  );

  const blogPostsState = useBuilder(() => {
    const state = new BlogPostsState({
      getBlogPosts: () => {
        return graftResourceStatesFromMemo({ resources: getBlogPosts.data?.blogPosts ?? [] });
      },
      deleteBlogPosts: (ids: string[]) => {
        const blogPosts = lookUp(ids, blogPostsState.blogPostsCtr.data.blogPostById);
        return trackPromise({
          name: 'deleteBlogPosts',
          states: { updating: blogPosts },
          promise: deleteBlogPosts.mutateAsync({ ... }),
        }).result;
      },
    });
    return state;
  }) as BlogPostsState;

  React.useEffect(() => () => blogPostsState.destroy(), [blogPostsState]);

  return { blogPostsState, getBlogPosts, deleteBlogPosts };
};
```

### Key rules

- **`useBuilder`** — wraps State construction so the instance is created once and survives re-renders. Always cast the result to the concrete State type (`: BlogPostsState`).
- **`useEffect` cleanup** — always call `blogPostsState.destroy()` on unmount.
- **`graftResourceStatesFromMemo`** — must wrap the `getBlogPosts.data?.items ?? []` call inside the State's `getBlogPosts` prop. This grafts resource-states from the previous render onto freshly fetched items, so loading/updating indicators survive a refetch.
- **`trackPromise`** — wraps a mutation promise to attach loading/updating resource-states to specific items. Use `states: { updating: <items> }` to mark those items as updating while the promise runs.

---

## 4. `use<Name>Context.ts` — context + selectors

Reference: `blogs_fe/src/blogPosts/hooks/useBlogPostsContext.ts`

This file has three exports: the Context object, a typed `useXContext()` hook, and a `xCtx` selector object used by `withContextProps`.

```ts
export const BlogPostsContext = React.createContext<any>(null);

export const useBlogPostsContext = () => {
  const context = React.useContext(BlogPostsContext);
  if (!context)
    throw new Error(
      "useBlogPostsContext must be used within a BlogPostsContext.Provider"
    );
  return context;
};

export const blogPostsCtx = R.mergeAll([
  {
    blogPosts: [useBlogPostsContext, "blogPosts"] as any as BlogPostT[],
    blogPost: [useBlogPostsContext, "blogPost"] as any as BlogPostT,
    blogPostsAddition: [
      useBlogPostsContext,
      "blogPostsAddition",
    ] as any as Addition,
    blogPostsDeletion: [
      useBlogPostsContext,
      "blogPostsDeletion",
    ] as any as Deletion,
    blogPostsEdit: [useBlogPostsContext, "blogPostsEdit"] as any as Edit,
    blogPostsHighlight: [
      useBlogPostsContext,
      "blogPostsHighlight",
    ] as any as Highlight,
    blogPostsSelection: [
      useBlogPostsContext,
      "blogPostsSelection",
    ] as any as Selection,
  },
]);
```

Each entry in `blogPostsCtx` is a `[hookFn, 'keyName']` tuple cast to the correct type via `as any as T`. The selector object is what components pass to `withContextProps` to pull values from context.

---

## 5. `<Name>StateProvider.tsx` — the provider component

Reference: `blogs_fe/src/blogPosts/components/BlogPostsStateProvider.tsx`

The StateProvider is an `observer` component (wrapped in `withContextProps` if it needs context from a parent provider). It creates the state, builds the cache, and provides context to children.

### Structure

```tsx
export const BlogPostsStateProvider = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    const { blogPostsState, getBlogPosts, deleteBlogPosts } = useBlogPostsState(
      { getBlog: () => props.blogsHighlight.item }
    );

    // cache: MobX computed properties that enrich raw data with resource-state
    const cache = useBuilder(() =>
      makeAutoObservable({
        get blogPosts() {
          return updateSources(
            { resource: blogPostsState.blogPostsCtr.data.blogPosts },
            ["loading", () => isQueryLoading(getBlogPosts), "getBlogPosts"],
            ["updating", () => isRunning(deleteBlogPosts), "deleteBlogPosts"]
          );
        },
        get blogPost() {
          return updateSources({
            resource: blogPostsState.blogPostsCtr.highlight.item,
          });
        },
      })
    );

    const getBlogPostsContext = () =>
      createGetProps({
        blogPostsState: () => blogPostsState,
        blogPosts: () => cache.blogPosts,
        blogPost: () => cache.blogPost,
        blogPostsAddition: () => blogPostsState.blogPostsCtr.addition,
        blogPostsDeletion: () => blogPostsState.blogPostsCtr.deletion,
        blogPostsEdit: () => blogPostsState.blogPostsCtr.edit,
        blogPostsHighlight: () => blogPostsState.blogPostsCtr.highlight,
        blogPostsSelection: () => blogPostsState.blogPostsCtr.selection,
      });

    return (
      <BlogPostsContext.Provider value={getBlogPostsContext()}>
        {props.children}
      </BlogPostsContext.Provider>
    );
  }, ContextProps)
);
```

### The cache object and `updateSources`

`updateSources` attaches resource-state metadata to a resource. Each extra argument is a tuple `['loading' | 'updating', sourceFn, debugLabel]`. The result is the same resource object enriched with loading/updating state that components can query with `isLoading(x)` or `isUpdating(x)`.

- Use `'loading'` for query-driven state (`isQueryLoading(query)`).
- Use `'updating'` for mutation-driven state (`isRunning(mutation)`).
- A resource without any extra sources (e.g. a single highlighted item) only needs `updateSources({ resource: ... })` with no extra tuples.

The cache uses `makeAutoObservable` + `useBuilder` so MobX tracks the computed properties without triggering re-renders in the StateProvider itself.

### `createGetProps`

`createGetProps` converts a plain object of getter functions into get-properties. This is critical: it prevents the StateProvider from reading MobX-observable values during render, which would make the StateProvider itself reactive and cause unnecessary re-renders. Always use `createGetProps` — never pass the values directly.

### When to use `withContextProps` on the StateProvider

Wrap the StateProvider in `withContextProps` only when it needs to consume values from a sibling or parent context (e.g. `BlogPostsStateProvider` reads `blogsHighlight` from `BlogsContext`). If the StateProvider needs no parent context, use `observer((props: PropsT) => { ... })` directly.

---

## Resource state in consuming components

Components access resource state via `isLoading` and `isUpdating` from `mobx-resource-states`:

```tsx
import { isLoading, isUpdating } from "mobx-resource-states";

// show a spinner while the list is loading
if (isLoading(props.blogPosts)) return <Spinner />;

// disable a button while an item is being deleted
<button disabled={isUpdating(props.blogPost)}>Delete</button>;
```

The resource-state is attached by `updateSources` in the cache — components just call `isLoading`/`isUpdating` on whatever resource they received from context.

---

## Checklist

- [ ] `XState.ts`: `PropsT` contains only hook functions, not raw data
- [ ] `XState.ts`: `destroy()` calls `Skandha.cleanUpCtr(this)`
- [ ] `XState.ts`: `actionsCtr` omitted if all interactions go through facets
- [ ] `XState.ts`: child facet instances receive `this` in constructor (e.g., `new XAddition(this)`)
- [ ] `facets/XAddition.ts` (and similar): child class extends parent from `skandha-facets`
- [ ] `facets/XAddition.ts` (and similar): constructor receives `private state: XState` parameter
- [ ] `facets/XAddition.ts` (and similar): overrides only protected methods, not core operations
- [ ] `registerXCtr.ts`: `mapData` wires computed properties; no `setCallbacks` function
- [ ] `useXState.ts`: State constructed inside `useBuilder()`; result cast to concrete type
- [ ] `useXState.ts`: `useEffect` cleanup calls `state.destroy()`
- [ ] `useXState.ts`: `getBlogPosts` prop wraps data in `graftResourceStatesFromMemo`
- [ ] `useXState.ts`: mutation props use `trackPromise` with appropriate `states`
- [ ] `useXContext.ts`: each `xCtx` entry is a `[hookFn, 'key']` tuple cast with `as any as T`
- [ ] `XStateProvider.tsx`: cache built with `makeAutoObservable` inside `useBuilder`
- [ ] `XStateProvider.tsx`: every resource exposed through context goes through `updateSources`
- [ ] `XStateProvider.tsx`: context value built with `createGetProps`, not a plain object
- [ ] `XStateProvider.tsx`: `withContextProps` used only when parent context is needed
