import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { validationError } from '/tests/fakeBackend/validationError';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user saves a blog post that no longer exists', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, we have a blog post, and the next update will fail because
  // the blog post is gone.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      env.backend.failNext(
        'updateBlogPost',
        validationError('BLOG_POST_NOT_FOUND')
      )
    )
  ) {
  }

  // We edit the blog post, and press Save.
  //
  // It should show the global error, and keep the form open with the new title.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Edit selected blog post'),
      await env.fillField('TITLE', 'New title'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Oops, something went wrong, please try again later'
    );
    await expect(env.view('BlogPostFormView')).toBeVisible();
    await expect(env.page.getByLabel('TITLE', { exact: true })).toHaveValue(
      'New title'
    );
  }
});

class Env extends BlogPostsTestEnv {}
