import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS, O_SOTO_GARI } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { validationError } from '/tests/fakeBackend/validationError';
import { test, type Ctx } from '/tests/testEnv/fixtures';

// The query client tries a failing query four times (the first try and three retries).
const NR_OF_QUERY_TRIES = 4;

// More than the seven seconds that the retries take.
const AFTER_THE_RETRIES = { timeout: 15000 };

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
  }
});

test('a failed delete keeps the blog posts in the list', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have a blog with two blog posts. The next delete will
  // fail with BLOG_POSTS_NOT_FOUND, and the refetch that follows will fail too, so
  // that the list shows what the cache holds.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      await env.addBlogPost(JUDO.slug, O_SOTO_GARI),
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      env.backend.failNext(
        'deleteBlogPosts',
        validationError('BLOG_POSTS_NOT_FOUND')
      ),
      await env.failBlogPostQueries()
    )
  ) {
  }

  // We press the delete-blog-posts button.
  //
  // It should keep both blog posts in the cache, and so in the list.
  if (
    env.step(
      //
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect
      .poll(
        () => env.backend.requestsOf('getBlogPosts').length,
        AFTER_THE_RETRIES
      )
      .toBe(1 + NR_OF_QUERY_TRIES);
    await expect(env.blogPostListItems()).toHaveText([
      new RegExp(BREAKFALLS.title),
      new RegExp(O_SOTO_GARI.title),
    ]);
  }
});

test('a delete fails unexpectedly', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, we have a blog post, and the next delete will fail.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      env.backend.failNext('deleteBlogPosts', { status: 500, json: {} })
    )
  ) {
  }

  // We select the blog post, and press the delete-blog-posts button.
  //
  // The blog post should stay in the list, and we should be able to try again.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect
      .poll(() => env.backend.requestsOf('deleteBlogPosts').length)
      .toBe(1);
    await expect(env.blogPostListItems()).toHaveText([
      new RegExp(BREAKFALLS.title),
    ]);
    await expect(env.button('Delete selected blog posts')).toBeEnabled();
  }

  // We press the delete-blog-posts button again.
  //
  // It should delete the blog post.
  if (
    env.step(
      //
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect(env.blogPostListItems()).toHaveCount(0);
  }
});

class Env extends BlogPostsTestEnv {
  /** Removes the blog post from the backend, without the app knowing about it. */
  async removeBlogPostFromBackend(title: string) {
    this.backend.data.blogPosts = this.backend.data.blogPosts.filter(
      (x) => x.title !== title
    );
  }

  /** Makes the next query of the blog posts fail, including its retries. */
  async failBlogPostQueries() {
    for (let i = 0; i < NR_OF_QUERY_TRIES; i++) {
      this.backend.failNext('getBlogPosts', { status: 500, json: {} });
    }
  }
}
