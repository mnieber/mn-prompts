import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { O_SOTO_GARI } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user publishes a blog post', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have a blog post that is not published.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, O_SOTO_GARI)
    )
  ) {
  }

  // We open the blog post, and press the mark-as-published button.
  //
  // It should call MarkBlogPostAsPublished, and show the blog post as published.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(O_SOTO_GARI.title),
      await env.clickButton('Mark as Published')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('markBlogPostAsPublished')?.path)
      .toBe('/blogs/blog-1/blog-posts/blog-post-1/publish/');
    await expect(env.blogPostListItem(O_SOTO_GARI.title)).toContainText('✔️');
    await expect(env.button('Already Published')).toBeDisabled();
  }
});

class Env extends BlogPostsTestEnv {}
