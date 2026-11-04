import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const CREATE_URL = '/blogs/judo/blog-posts/create/_';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user creates a blog post with a title that already exists', async ({
  ctx,
}) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo with the blog post Breakfalls.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS)
    )
  ) {
  }

  // We open the create-blog-post form, use the title Breakfalls, and press Save.
  //
  // It should show the error on the title field, stay on the create route, and
  // keep what the user typed.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickButton('Create blog post'),
      await env.fillField('TITLE', BREAKFALLS.title),
      await env.fillField('CONTENT', 'Slap the mat.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('TITLE')).toHaveText(
      'A blog post with this title already exists'
    );
    await expect(env.view('GlobalError')).toHaveCount(0);
    await expect(env.page).toHaveURL(CREATE_URL);
    await expect(env.page.getByLabel('CONTENT', { exact: true })).toHaveValue(
      'Slap the mat.'
    );
  }

  // We change the title, and press Save again.
  //
  // It should create the blog post and open it.
  if (
    env.step(
      //
      await env.fillField('TITLE', 'Rolling breakfalls'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.page).toHaveURL(
      '/blogs/judo/blog-posts/rolling-breakfalls-'
    );
    await expect(env.blogPostListItems()).toHaveCount(2);
  }
});

test('a user creates a blog post with forbidden words', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO)
    )
  ) {
  }

  // We open the create-blog-post form, use a forbidden word in the title, and
  // press Save.
  //
  // It should show the error on the title field.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickButton('Create blog post'),
      await env.fillField('TITLE', 'Forbidden throws'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('TITLE')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('CONTENT')).toHaveCount(0);
    await expect(env.page).toHaveURL(CREATE_URL);
  }

  // We fix the title, use a forbidden word in the content, and press Save.
  //
  // It should show the error on the content field.
  if (
    env.step(
      //
      await env.fillField('TITLE', 'Throws'),
      await env.fillField('CONTENT', 'Forbidden in competition.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('CONTENT')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('TITLE')).toHaveCount(0);
    await expect(env.page).toHaveURL(CREATE_URL);
  }
});

class Env extends BlogPostsTestEnv {}
