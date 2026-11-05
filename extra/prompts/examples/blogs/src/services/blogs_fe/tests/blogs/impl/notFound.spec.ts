import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user opens a url of a blog post that does not exist', async ({
  ctx,
}) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We have the blog Judo with a blog post, and we open the url of another blog
  // post.
  //
  // It should say that the blog post doesn't exist, and list the blog posts.
  if (
    env.step(
      //
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      await env.visit('/blogs/judo/blog-posts/ukemi')
    )
  ) {
    await expect(env.view('NotFoundMessage')).toHaveText(
      "This blog post doesn't exist"
    );
    await expect(env.blogPostListItem(BREAKFALLS.title)).toBeVisible();
  }

  // We click the blog post.
  //
  // The message should go away.
  if (
    env.step(
      //
      await env.clickBlogPost(BREAKFALLS.title)
    )
  ) {
    await expect(env.view('NotFoundMessage')).toHaveCount(0);
  }
});

class Env extends BlogPostsTestEnv {}
