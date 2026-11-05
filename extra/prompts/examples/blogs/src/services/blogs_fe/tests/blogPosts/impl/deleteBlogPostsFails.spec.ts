import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS, O_SOTO_GARI } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user deletes a blog post that someone else already deleted', async ({
  ctx,
}) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have a blog with two blog posts.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      await env.addBlogPost(JUDO.slug, O_SOTO_GARI)
    )
  ) {
  }

  // We select both blog posts. Then Breakfalls is deleted behind our back, and
  // we press the delete-blog-posts button.
  //
  // The delete should fail, and O-soto-gari should still be there. The list
  // should be refetched, so that Breakfalls disappears from it.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.ctrlClickBlogPost(O_SOTO_GARI.title),
      await env.removeBlogPostFromBackend(BREAKFALLS.title),
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect
      .poll(() => env.backend.requestsOf('deleteBlogPosts').length)
      .toBe(1);
    await expect(env.blogPostListItems()).toHaveText([O_SOTO_GARI.title]);
    await expect(env.button('Delete selected blog posts')).toBeEnabled();
    await expect(env.view('ErrorBanner')).toContainText(
      'Some of these blog posts no longer exist'
    );
  }

  // We press the delete-blog-posts button again.
  //
  // It should only send O-soto-gari, delete it, and clear the banner.
  if (
    env.step(
      //
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('deleteBlogPosts')?.body)
      .toEqual({ delete_blog_posts_form: { blog_post_ids: ['blog-post-2'] } });
    await expect(env.blogPostListItems()).toHaveCount(0);
    await expect(env.view('ErrorBanner')).toHaveCount(0);
  }
});

class Env extends BlogPostsTestEnv {
  /** Removes the blog post from the backend, without the app knowing about it. */
  async removeBlogPostFromBackend(title: string) {
    this.backend.data.blogPosts = this.backend.data.blogPosts.filter(
      (x) => x.title !== title
    );
  }
}
