import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS, O_SOTO_GARI } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const KARATE = { name: 'Karate', slug: 'karate', description: 'Punches.' };

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('the lists ignore clicks while the edit form is open', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, we have two blogs, and we edit Breakfalls.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlog(KARATE),
      await env.addBlogPost(JUDO.slug, { ...BREAKFALLS, is_published: false }),
      await env.addBlogPost(JUDO.slug, O_SOTO_GARI),
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Edit selected blog post'),
      await env.fillField('CONTENT', 'What I typed')
    )
  ) {
    await expect(env.button('Create blog post')).toBeDisabled();
    await expect(env.button('Delete selected blog posts')).toBeDisabled();
    await expect(env.button('Mark as Published')).toBeDisabled();
  }

  // We click another blog post, and another blog.
  //
  // Nothing should change, and what we typed should still be there.
  if (
    env.step(
      //
      await env.clickBlogPost(O_SOTO_GARI.title),
      await env.clickBlog(KARATE.name)
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/breakfalls');
    await expect(env.blogPostListItem(BREAKFALLS.title)).toHaveClass(
      /--highlighted/
    );
    await expect(env.page.getByLabel('CONTENT', { exact: true })).toHaveValue(
      'What I typed'
    );
  }

  // We press Cancel, and click another blog post.
  //
  // The list should work again.
  if (
    env.step(
      //
      await env.clickButton('Cancel'),
      await env.clickBlogPost(O_SOTO_GARI.title)
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/o-soto-gari');
    await expect(env.button('Delete selected blog posts')).toBeEnabled();
  }
});

class Env extends BlogPostsTestEnv {}
