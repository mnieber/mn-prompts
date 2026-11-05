import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

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
  // It should say that the blog post is gone, refetch the list, and keep the form open
  // with the new title.
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
      'This blog post no longer exists'
    );
    await expect(env.blogPostListItems()).toHaveCount(0);
    await expect(env.view('BlogPostFormView')).toBeVisible();
    await expect(env.page.getByLabel('TITLE', { exact: true })).toHaveValue(
      'New title'
    );
  }

  // We press Save again.
  //
  // It should show the same error, without sending a request.
  if (
    env.step(
      //
      await env.clickButton('Save')
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'This blog post no longer exists'
    );
    expect(env.backend.requestsOf('updateBlogPost')).toHaveLength(1);
  }

  // We press Cancel.
  //
  // It should close the form, and navigate to the blog.
  if (
    env.step(
      //
      await env.clickButton('Cancel')
    )
  ) {
    await expect(env.view('BlogPostFormView')).toBeHidden();
    await expect(env.page).toHaveURL('/blogs/judo');
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
}
