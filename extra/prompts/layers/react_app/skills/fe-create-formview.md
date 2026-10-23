# Skill: fe-create-formview

Applies when writing a `FormView.tsx` component and its companion `form.ts` file. A FormView is a form backed by `react-form-state-context`, wired to MobX state via `withContextProps`, and laid out using `Field` + `FormFieldLabel` pairs.

---

## File structure

A FormView lives in its own directory and always contains these files:

```
<Module>/components/<Name>FormView/
  <Name>FormView.tsx   ← the component
  form.ts              ← form logic (values, errors, handlers)
  index.tsx            ← re-exports PropsT, ContextProps, and the component
  <Name>FormView.scss  ← intrinsic styles (often minimal)
```

Reference: `blogs_fe/src/blogPosts/components/BlogPostFormView/`

---

## FormView.tsx structure

Reference: `blogs_fe/src/blogPosts/components/BlogPostFormView/BlogPostFormView.tsx`

### Required parts, in order:

1. **`PropsT`** — only externally-passed props (usually just `className?: any`)
2. **`ContextProps`** — object mapping context property names to context selectors (e.g. `blogPostsCtx.blogPost`)
3. **The component** — `observer(withContextProps(..., ContextProps))`
4. Inside the component body:
   - Call `form.getInitialValues(props)` and `form.getInitialErrors(props)`
   - Guard: return `null` if a required resource is not yet available
   - Render `<FormStateProvider>` with `initialValues`, `initialErrors`, `handleValidate`, `handleSubmit`, `handleCancel`
   - Inside `<FormStateProvider>`: render `<GlobalError>`, then a `<Field>` block per form field, then a buttons row

### `withContextProps` usage

`withContextProps` is an HOC that merges context values into the component's props. The second argument is the `ContextProps` object. The component signature is `(props: PropsT & typeof ContextProps)`.

```tsx
export const BlogPostFormView = observer(
  withContextProps((props: PropsT & typeof ContextProps) => {
    // ...
  }, ContextProps)
);
```

### `FormStateProvider` props

```tsx
<FormStateProvider
  initialValues={initialValues}
  initialErrors={initialErrors}
  handleValidate={form.getHandleValidate(props)}
  handleSubmit={form.getHandleSubmit(props, initialValues, initialErrors)}
  handleCancel={form.getHandleCancel(props)}
>
```

Note: `handleCancel` is optional — omit it if the form has no cancel action.

### Field blocks

Each field is a `<Field fieldName="...">` wrapping a `<FormFieldLabel>` and the input widget:

```tsx
<Field fieldName="blogPostForm.title" className={MainFormS.Field()}>
  <FormFieldLabel label="TITLE" />
  <NameField tabIndex={2} controlled={true} autoSelect={true} />
</Field>
```

`FormFieldLabel` accepts an optional `buttons` prop for action buttons shown at the far right of the label row (e.g. a preview toggle button).

### Buttons row

Cancel and Save buttons sit in a `<div>` below the fields:

```tsx
<div className={cn(MainFormS.Buttons())}>
  <FormCancelButton theme="MainView" label="Cancel" tabIndex={10} ... />
  <FormSaveButton   theme="MainView" label="Save"   tabIndex={10} ... />
</div>
```

---

## form.ts structure

Reference: `blogs_fe/src/blogPosts/components/BlogPostFormView/form.ts`

`form.ts` exports a single `form` object with factory functions. All functions take `props` as their first argument so they can read context-provided state.

```ts
export const form = {
  getInitialValues,
  getInitialErrors,
  getHandleValidate,
  getHandleSubmit,
  getHandleCancel,   // omit if no cancel action
};
```

### `getInitialValues`

Two responsibilities: seed field values from props, and declare every field name the form uses (set to `null` if no initial value applies).

```ts
const getInitialValues = (props: PropsT & typeof ContextProps) => {
  const blogPost = props.blogPostsAddition.item ?? props.blogPost;
  return {
    'blogPostForm.title':   blogPost.title   ?? null,
    'blogPostForm.slug':    blogPost.slug    ?? null,
    'blogPostForm.content': blogPost.content ?? null,
  };
};
```

Field names use a `<formName>.<fieldName>` convention (e.g. `blogPostForm.title`).

### `getInitialErrors`

Seeds external validation errors from props into the form. Return `{}` when there are no external errors.

```ts
const getInitialErrors = (props: PropsT & typeof ContextProps) => {
  return {};
};
```

### `getHandleValidate`

Returns a validate callback. Use `setError(fieldName, message)` for field-level errors.

```ts
const getHandleValidate =
  (props: PropsT & typeof ContextProps) =>
  ({ values, setError }: HandleValidateArgsT) => {
    if (R.isNil(values['blogPostForm.title'])) {
      setError('blogPostForm.title', 'This field is required');
    }
  };
```

### `getHandleSubmit`

Returns a submit callback. After a successful save, call `formState.reset(initialValues, initialErrors)` and navigate away. On error, set the `'global'` error.

```ts
const getHandleSubmit =
  (props: PropsT & typeof ContextProps, initialValues, initialErrors) =>
  ({ formState, values }: HandleSubmitArgsT) => {
    return props.blogPostsEdit
      .save({ values: unflatten({ ...values }) })
      .then((response: ObjT) => {
        formState.reset(initialValues, initialErrors);
        navTo(blogPostsNav.blogPost({ ... }));
        return response;
      })
      .catch(() => {
        formState.setError('global', 'Oops, something went wrong, please try again later');
      });
  };
```

### `getHandleCancel`

Returns a cancel callback. Cancels the edit facet and restores the previous nav point (or falls back to a home route).

```ts
const getHandleCancel =
  (props: PropsT & typeof ContextProps) =>
  ({ formState }: HandleCancelArgsT) => {
    const mustRestore = !!props.blogPostsAddition.item;
    props.blogPostsEdit.cancel();
    if (mustRestore) {
      if (!props.navState.restoreNavPoint()) {
        navTo(authNav.home({}));
      }
    }
  };
```

---

## index.tsx

Always re-export `PropsT`, `ContextProps`, and the component so that `form.ts` can import from `./index` without circular-dependency issues.

```tsx
// index.tsx
export { BlogPostFormView, ContextProps, type PropsT } from './BlogPostFormView';
```

---

## Checklist

- [ ] Directory is `<Module>/components/<Name>FormView/` with all four files
- [ ] `PropsT` contains only externally-passed props (`className?: any` at minimum)
- [ ] `ContextProps` is a plain object (not a type) mapping names to context selectors
- [ ] Component is `observer(withContextProps(..., ContextProps))`
- [ ] Component guards against missing resource (returns `null` early)
- [ ] `FormStateProvider` receives all four handlers from `form.*`
- [ ] Each field is wrapped in `<Field fieldName="...">` with `<FormFieldLabel>` inside
- [ ] `form.ts` exports a `form` object (not individual functions)
- [ ] `getInitialValues` declares every field name (missing fields cause silent bugs)
- [ ] `getHandleSubmit` calls `formState.reset(...)` on success and sets `'global'` error on failure
- [ ] `index.tsx` re-exports `PropsT`, `ContextProps`, and the component
