# Skill: fe-write-workflow-tests

Applies when writing (or converting) tests for a React app. In the workflow-test style, a developer can read a test
top to bottom, like a story, and understand how the app is used: the starting situation, what the user does in the
browser, and what should happen as a result (on the screen, and in the requests to the backend).

The tests have two purposes: they verify the app, and they are the spec that the code is generated from (they are
written before the code exists). Every rule below serves both purposes.

This skill is the frontend counterpart of `py-write-workflow-tests` (python_lib layer). The principles are the same;
what differs is the tool (Playwright) and the boundary that is faked (the REST backend).

---

## Kinds of tests

- **Workflow tests** explain the main workflows of a feature (the happy paths, and the scenarios of the specs). They
  run the whole app in a real browser with **Playwright**, against a fake backend. They live in
  `tests/<feature>/workflows/`.
- **Impl tests** cover edge cases and details (validation messages, disabled buttons, cancel and restore, failing
  requests, keyboard selection). Most of them are Playwright tests as well, and live in `tests/<feature>/impl/`.
- **State tests** cover tricky logic of the State layer (how the facets of a container work together, e.g.
  Addition → Edit → Selection) without rendering components. They use **Vitest**, and live next to the impl tests in
  `tests/<feature>/state/`. Write them only when a Playwright test would be hard to read or slow (many combinations),
  not by default.
- **Unit tests** of small, pure pieces (e.g. `slugify`, `reformatBlogPost`) are plain Vitest tests, next to the code
  (`<name>.test.ts`).

Rules of thumb:

- One workflow per test. When a workflow is finished, the next one starts in a new test.
- Many independent edge cases are split by theme into a handful of impl tests, not one test per assert and not one
  giant test. Within a test, later steps may continue on the same page and check again.
- Every test is self-contained: it builds its own environment (backend data, signed-in user, start url).
- Never use Cypress, React Testing Library or Storybook interaction tests for workflow tests: every workflow test is a
  Playwright test, so that all workflows read the same way.

## File layout

```
playwright.config.ts                   ← enabledTestPackages (see below), webServer, browser settings
tests/
  tsconfig.json                        ← adds the `/tests/*` import path
  testEnv/
    TestEnv.ts                         ← the shared TestEnv base class
    FakeBackend.ts                     ← the fake REST backend (records requests, in-memory data)
    fixtures.ts                        ← `test` (with the `ctx` fixture) and the `Ctx` type
    urls.ts                            ← baseURL and apiUrl (shared with playwright.config.ts)
    endpoints/
      index.ts                         ← the list of all fake endpoints
      getBlogs.ts                      ← one fake endpoint per query or mutation
      createBlog.ts
  <feature>/
    <Feature>TestEnv.ts                ← the shared Env base class of the feature
    workflows/
      <scenarioName>.spec.ts           ← one test per file, named after the scenario
    impl/
      <edgeCaseTheme>.spec.ts
    state/                             ← optional Vitest tests of the State layer
      <theme>.test.ts
```

- File and directory names are camelCase, like the rest of the app (`blogPosts/workflows/userCreatesABlogPost.spec.ts`).
- Import shared modules with an absolute import (`import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv'`).
  Never import from another test file.
- `playwright.config.ts` lists the enabled test packages in `enabledTestPackages`, in the order in which the code is
  implemented, and builds `testMatch` from it. Tests may be written before the code exists: the package is enabled
  when its code is written.

## Anatomy of a test

```ts
import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const JUDO = { name: 'Judo', slug: 'judo' };
const TITLE = 'Breakfalls for beginners';
const CONTENT = 'Always tuck in your chin.';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user creates a blog post', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo without blog posts.
  if (env.step(await env.signIn('maarten'), await env.addBlog(JUDO))) {
  }

  // We visit the Judo blog.
  //
  // The blog should be highlighted in the BlogListView, and the BlogPostListView
  // should be empty.
  if (env.step(await env.visit('/blogs/judo'))) {
    await expect(env.blogListItem('Judo')).toHaveClass(/--highlighted/);
    await expect(env.blogPostListItems()).toHaveCount(0);
  }

  // We press the create-blog-post button.
  //
  // It should open the BlogPostFormView on the create route.
  if (env.step(await env.clickButton('Create blog post'))) {
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/create/_');
    await expect(env.view('BlogPostFormView')).toBeVisible();
  }

  // We fill out the form and press Save.
  //
  // It should call CreateBlogPost with the form data, show the new blog post, and
  // list it in the BlogPostListView.
  if (
    env.step(
      await env.fillField('TITLE', TITLE),
      await env.fillField('CONTENT', CONTENT),
      await env.clickButton('Save')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('createBlogPost')?.body)
      .toMatchObject({
        create_blog_post_form: { title: TITLE, content: CONTENT },
      });
    // The slug is derived from the title.
    await expect(env.page).toHaveURL(
      '/blogs/judo/blog-posts/breakfalls-for-beginners'
    );
    await expect(env.blogPostListItems()).toHaveText([TITLE]);
  }
});

class Env extends BlogPostsTestEnv {}
```

Each step is a comment block, then `if (env.step(<actions>))`, then a body with asserts.

- The comment starts with the **action**, as a story beat in the first person plural ("We visit ...", "We have ...",
  "We press ..."). If the step has expected results, an empty comment line (`//`) follows, and then the **expected
  result**, phrased with "should".
- A step without expected results has only the action part, and its body is empty (`{}`).
- A step that only inspects the page is `if (env.step())`, with a comment that says what we look at ("We look at the
  blog-post list. ...").
- A comment that explains _why_ goes directly above the assert that it explains.

Style rules:

- The actions are the arguments of `env.step(...)`, each one `await`ed, in the order in which they run (the arguments
  are evaluated left to right, and each `await` finishes before the next one starts). Keep a step small: one user
  action plus the set-up that it needs.
- The body only asserts: it runs no actions, and uses `env.<attribute>` and queries (not local variables).
- Asserts on the page are web-first (`await expect(locator).toHaveText(...)`), so that they wait for the UI.
  Asserts on the backend use `await expect.poll(() => env.backend....)`. Never use `page.waitForTimeout`.
- Use real-looking, readable values, and define shared texts and fixtures as module constants.
- Format with Prettier (the repo's `.prettierrc`).

## What a test tells the code generator

In Python, the imports of a test imply which code units exist. A Playwright test imports no app code, so the test
encodes the code structure through what it touches. Use these on purpose, because the code is generated from them:

| In the test                                             | Implies in the code                                         |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| a url (`env.visit('/blogs/judo')`, `toHaveURL(...)`)    | a route in `<module>/routes.ts` and a `<Route>` in a Switch |
| `env.view('BlogPostFormView')`                          | a component with that name (its root `div` has that class)  |
| a fake endpoint (`createBlogPost`) and its url and body | a query/mutation hook `useCreateBlogPost` with that url     |
| the json that a fake endpoint returns                   | the `XT` type and `XSchema` (camelCased) in `api/types/`    |
| a field label (`env.fillField('TITLE', ...)`)           | a `Field` with a `FormFieldLabel` in the FormView           |
| a modifier class (`--highlighted`, `--selected`)        | the Highlight / Selection facets and the ListView styles    |

- Locate elements the way the user sees them (`getByRole`, `getByLabel`, `getByText`), scoped to a view by its
  component class (`env.view('BlogListView').getByRole('link', { name: 'Judo' })`). Every component's root element has
  a class with the component name (see `fe-add-component`), so these locators are stable.
- Never locate by Tailwind classes, DOM structure (`div > div:nth-child(2)`) or generated ids.
- Mention a component name in a step comment when the scenario mentions it (e.g. "It should open the
  BlogPostFormView"), so that the test and the scenario use the same words.

## The Env classes

An Env holds the **state** of a test (attributes) and the **actions** that change it (methods).

- `Ctx` is a type with what the tests need: the Playwright `page`, the installed `backend` and the `pageErrors`. The
  `ctx` fixture is defined with `test.extend` in `tests/testEnv/fixtures.ts`: it installs the fake backend on the page
  (this is async, so it can't happen in a constructor) and collects uncaught page errors. Tests take `{ ctx }` as their
  only argument. (Don't call it `context`: Playwright already has a `context` fixture.)
- The base `TestEnv` lives in `tests/testEnv/TestEnv.ts`. Its constructor declares the common state (every attribute
  initialized, so that a reader sees which state exists): `page`, `backend`, `pageErrors`, copied from `ctx`. It
  calls the hook `postInit()`. `step(..._: unknown[])` ignores its arguments and returns `true`.
- The `ctx` fixture fails the test in its teardown when `pageErrors` or `backend.unexpectedRequests` is not empty.
  (Console errors are not page errors: they don't fail the test.)
- A feature with many shared actions gets an intermediate base class in `tests/<feature>/<Feature>TestEnv.ts` (e.g.
  `blogListItem(name)`, `addBlogWithPosts(...)`).
- Each test file ends with its own `class Env extends ...`, which adds only the actions that this file needs. Prefer
  duplicating a two-liner over sharing it between test files. An action that two or three features need goes into the
  closest shared base class.

Rules for actions:

- An action is `async`, runs immediately and returns `Promise<void>`. It reads and writes state on `this`, and its
  name says what the user or the world does (`visit`, `clickButton`, `fillField`, `pressKey`, `signIn`).
  Give it a short doc comment when its effect is not obvious.
- An action does the user's gesture and nothing more: it doesn't wait for the result of the gesture (the asserts do
  that). Exception: `visit` waits until the app has rendered `#App`.
- An action that stores a result may take a `storeAs` argument when a test needs more than one result.
- A query (e.g. `env.view(name)`, `env.blogPostListItems()`, `env.backend.lastRequest(name)`) returns a locator or a
  value for an assert, and is not passed to `env.step(...)`.
- Helpers that tests should not call directly are `private` or `protected`.

## The fake backend

The backend is the boundary of the app, and the only thing that is faked. `FakeBackend` intercepts the requests to
the api url with `page.route(...)`.

- It holds a small in-memory data set (e.g. `blogs`, `blogPosts`, `userId`), with rows in the shape of the real
  backend (`BlogRowT`, snake_case). Env actions seed it (`env.addBlog(...)`, `env.signIn(...)`) before the page is
  visited.
- Each query and mutation of the app has one fake endpoint in `tests/testEnv/endpoints/`, named after the hook
  (`getBlogs`, `createBlogPost`). It matches the method and url, reads/updates the data set, and returns json in the
  shape of the real backend (snake_case). A mutation updates the data set, so that a following query (after cache
  invalidation) returns the new state.
- It records every request (`name`, `method`, `url`, parsed `body`) in `env.backend.requests`, with
  `lastRequest(name)` and `requestsOf(name)` as queries.
- A request that no endpoint matches gets a 500 response and is stored in `unexpectedRequests`, which fails the test.
- A failing backend is scripted with `env.backend.failNext('createBlogPost', { status: 400, json: ['BLOG_NOT_FOUND'] })`.
  There is no `*_and_catch_error` variant: an error is asserted on what the user sees (e.g. the `GlobalError` of the
  form) and on the requests.
- Ids that the fake backend assigns are predictable (`blog-1`, `blog-post-1`).
- The MSW handlers (`fe-add-msw`) are for dev and Storybook; tests don't use them. The fake endpoints are the
  authoritative description of the api contract: when the hook and the fake endpoint disagree, the test is right.

## Running the app under test

- `yarn test:workflows` runs the Playwright tests.
- `playwright.config.ts` starts the app with `webServer` (`yarn vite --mode test --port 3100`), with
  `VITE_LOCALHOST_API_ENDPOINT` set to `http://localhost:3100/fake-api/`, which the fake backend intercepts. The api
  url has the same origin as the app, so that CORS plays no role.
- `serviceWorkers: 'block'` in the config, so that MSW can never answer instead of the fake backend.
- `waitOnDev` returns immediately in test mode (`import.meta.env.MODE === 'test'`), so that the tests don't wait for
  simulated latency.
- Playwright's own browsers don't run on Alpine (our `node:20-alpine` image). There, install `chromium` with `apk`;
  the config uses `/usr/bin/chromium` when it exists.
- Form inputs get `id={fieldName}` (in `useFieldProps`), so that the `FormFieldLabel` (`htmlFor={fieldName}`) labels
  them and `getByLabel` finds them.
- Make the environment deterministic: a fixed `locale`, `timezoneId` and viewport in the config, `page.clock` when the
  app shows dates, a fresh browser context (and so an empty `localStorage`) per test, and never depend on the
  developer's browser or shell.

## State tests (Vitest)

When a state test is warranted, it follows the same anatomy: a story of steps, an `Env` that builds the `XState` with
fake `props` (the hook functions: `getBlogPosts`, `saveBlogPost`, ...), actions that call the facets the way the views
do (`env.state.blogPostsCtr.addition.add(...)`), and asserts on the containers. The fake props record their calls,
just like the fake backend records requests. A state test imports the State class, so it also pins the facets and
the container layout of that State.

## Practical conventions

- Prefer real code paths over mocks: the whole app runs; only the backend is fake.
- Don't use `test.only`, retries or arbitrary timeouts to make a test pass. A flaky test is a bug in the test or the app.
- Use `test.step` only inside `TestEnv` helpers if needed for the report; tests use `env.step`.
- Run the tests that you changed and the whole test suite (`yarn playwright test`, `yarn vitest run`). Don't commit or
  stage anything unless asked to.

## Converting an existing test

1. List the distinct workflows and edge cases that the old test (or story) covers.
2. Decide for each: workflow test, impl test, state test or unit test. If unsure, ask.
3. Write each new test with the anatomy above, and remove the old test.
4. Keep the coverage of the old test: every assert that you drop is dropped on purpose.
5. Report which tests were created where, what was split or merged, and which asserts were dropped.

## Checklist

- [ ] One test per file, named after the scenario, in `<feature>/workflows/` or `<feature>/impl/`
- [ ] Every step has a comment block (action, then "should" results) and an `if (env.step(await ...))` with asserts only
- [ ] Asserts are web-first (`expect(locator)`) or polled (`expect.poll`); no `waitForTimeout`
- [ ] Elements are located by role/label/text, scoped by component class; no Tailwind or structural selectors
- [ ] Each file has its own small `Env`; shared actions live in the feature's test env
- [ ] Only the backend is faked, through `FakeBackend` endpoints named after the hooks; unexpected requests and page
      errors fail the test
- [ ] The test package is listed in `enabledTestPackages` once its code exists
