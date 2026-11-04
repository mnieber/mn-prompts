import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS, O_SOTO_GARI } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user gives a blog post the title of another blog post', async ({
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

  // We edit O-soto-gari, use the title Breakfalls, and press Save.
  //
  // It should show the error on the title field, and keep the form open.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(O_SOTO_GARI.title),
      await env.clickButton('Edit selected blog post'),
      await env.fillField('TITLE', BREAKFALLS.title),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('TITLE')).toHaveText(
      'A blog post with this title already exists'
    );
    await expect(env.view('GlobalError')).toHaveCount(0);
    await expect(env.view('BlogPostFormView')).toBeVisible();
  }

  // We change the title, and press Save again.
  //
  // It should save the blog post and close the form.
  if (
    env.step(
      //
      await env.fillField('TITLE', 'Major outer reap'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.view('BlogPostFormView')).toBeHidden();
    await expect(env.blogPostListItem('Major outer reap')).toBeVisible();
  }
});

test('a user saves a blog post with forbidden words', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have a blog post.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS)
    )
  ) {
  }

  // We edit the blog post, use a forbidden word in the title, and press Save.
  //
  // It should show the error on the title field.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Edit selected blog post'),
      await env.fillField('TITLE', 'Forbidden breakfalls'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('TITLE')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('CONTENT')).toHaveCount(0);
    await expect(env.view('BlogPostFormView')).toBeVisible();
  }

  // We fix the title, use a forbidden word in the content, and press Save.
  //
  // It should show the error on the content field.
  if (
    env.step(
      //
      await env.fillField('TITLE', 'Safe breakfalls'),
      await env.fillField('CONTENT', 'Forbidden on concrete.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('CONTENT')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('TITLE')).toHaveCount(0);
    await expect(env.view('BlogPostFormView')).toBeVisible();
  }
});

test('a user saves a blog post that no longer exists', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have a blog post.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS)
    )
  ) {
  }

  // We edit the blog post. Then it is deleted behind our back, and we press Save.
  //
  // It should show the global error, and keep the form open with the new title.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost(BREAKFALLS.title),
      await env.clickButton('Edit selected blog post'),
      await env.fillField('TITLE', 'New title'),
      await env.removeBlogPostFromBackend(BREAKFALLS.title),
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

  // We press Cancel.
  //
  // It should close the form.
  if (
    env.step(
      //
      await env.clickButton('Cancel')
    )
  ) {
    await expect(env.view('BlogPostFormView')).toBeHidden();
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
