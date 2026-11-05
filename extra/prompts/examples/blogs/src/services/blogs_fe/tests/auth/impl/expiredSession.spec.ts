import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { authenticationError } from '/tests/fakeBackend/authenticationError';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('the session expires while a user edits a blog post', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, we have a blog post, and we edit it.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Edit selected blog post')
    )
  ) {
  }

  // The session expires, and we press Save.
  //
  // It should go to the sign-in page, with the current url as the next url.
  if (
    env.step(
      //
      env.backend.failNext('updateBlogPost', authenticationError()),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.page).toHaveURL(
      `/sign-in?nextUrl=${encodeURIComponent('/blogs/judo/blog-posts/breakfalls')}`
    );
  }
});

class Env extends BlogPostsTestEnv {}
