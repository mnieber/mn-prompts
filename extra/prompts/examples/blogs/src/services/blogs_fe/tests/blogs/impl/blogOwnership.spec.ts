import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const OTHER_USERS_BLOG = { ...JUDO, owner_id: 'someone-else' };

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user looks at the blog of someone else', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we open a blog post in the blog of someone else.
  //
  // We can read it, but all buttons that change it should be disabled.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(OTHER_USERS_BLOG),
      await env.addBlogPost(JUDO.slug, { ...BREAKFALLS, is_published: false }),
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title)
    )
  ) {
    await expect(env.blogPostListItem(BREAKFALLS.title)).toHaveClass(
      /--highlighted/
    );
    await expect(env.button('Create blog post')).toBeDisabled();
    await expect(env.button('Edit selected blog post')).toBeDisabled();
    await expect(env.button('Delete selected blog posts')).toBeDisabled();
    await expect(env.button('Mark as Published')).toBeDisabled();
  }
});

class Env extends BlogPostsTestEnv {}
