import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import {
  BREAKFALLS,
  JUJI_GATAME,
  O_SOTO_GARI,
} from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const NEW_TITLE = 'O-soto-gari, the major outer reap';
const NEW_CONTENT = 'Break the balance to the back corner first.';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

// The scenario has two goals (editing and deleting), and so there are two
// workflows, each in its own test.

test('a user edits a blog post', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo with two blog posts.
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

  // We visit the blog Judo and select the blog post O-soto-gari.
  //
  // It should open the blog post, and the edit-blog-post button should be
  // enabled.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost('O-soto-gari')
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/o-soto-gari');
    await expect(env.blogPostListItem('O-soto-gari')).toHaveClass(
      /BlogPostListViewItem--highlighted/
    );
    await expect(env.button('Edit selected blog post')).toBeEnabled();
  }

  // We press the edit-blog-post button.
  //
  // It should open the BlogPostFormView with the values of the blog post.
  if (
    env.step(
      //
      await env.clickButton('Edit selected blog post')
    )
  ) {
    await expect(env.view('BlogPostFormView')).toBeVisible();
    await expect(env.page.getByLabel('TITLE', { exact: true })).toHaveValue(
      'O-soto-gari'
    );
  }

  // We change the title and the content, and press Save.
  //
  // It should call UpdateBlogPost with the form data, and show the new title
  // in the BlogPostListView.
  if (
    env.step(
      //
      await env.fillField('TITLE', NEW_TITLE),
      await env.fillField('CONTENT', NEW_CONTENT),
      await env.clickButton('Save')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('updateBlogPost'))
      .toMatchObject({
        // The blog and the blog post are identified by their ids
        path: '/blogs/blog-1/blog-posts/blog-post-2/update/',
      });
    // The form data has exactly these fields
    await expect
      .poll(() => env.backend.lastRequest('updateBlogPost')?.body)
      .toEqual({
        update_blog_post_form: {
          title: NEW_TITLE,
          // The slug does not change when the title changes
          slug: 'o-soto-gari',
          content: NEW_CONTENT,
          level: 'medium',
          tags: null,
        },
        blog_id: 'blog-1',
        blog_post_id: 'blog-post-2',
      });
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/o-soto-gari');
    await expect(env.blogPostListItems()).toHaveText([
      /^Breakfalls/,
      NEW_TITLE,
    ]);
  }
});

test('a user deletes blog posts', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo with three blog posts.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      await env.addBlogPost(JUDO.slug, BREAKFALLS),
      await env.addBlogPost(JUDO.slug, O_SOTO_GARI),
      await env.addBlogPost(JUDO.slug, JUJI_GATAME)
    )
  ) {
  }

  // We visit the blog Judo, select Breakfalls, and add Juji-gatame to the
  // selection.
  //
  // Both blog posts should be selected, and the delete-blog-posts button
  // should be enabled.
  if (
    env.step(
      //
      await env.visit('/blogs/judo'),
      await env.clickBlogPost('Breakfalls'),
      await env.ctrlClickBlogPost('Juji-gatame')
    )
  ) {
    await expect(env.blogPostListItem('Breakfalls')).toHaveClass(
      /BlogPostListViewItem--selected/
    );
    await expect(env.blogPostListItem('Juji-gatame')).toHaveClass(
      /BlogPostListViewItem--selected/
    );
    await expect(env.blogPostListItem('O-soto-gari')).not.toHaveClass(
      /BlogPostListViewItem--selected/
    );
    await expect(env.button('Delete selected blog posts')).toBeEnabled();
  }

  // We press the delete-blog-posts button.
  //
  // It should call DeleteBlogPosts with the selected blog posts, and the
  // BlogPostListView should only list O-soto-gari.
  if (
    env.step(
      //
      await env.clickButton('Delete selected blog posts')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('deleteBlogPosts'))
      .toMatchObject({
        path: '/blogs/blog-1/blog-posts/delete/',
        body: {
          // The ids of Breakfalls and Juji-gatame
          delete_blog_posts_form: {
            blog_post_ids: ['blog-post-1', 'blog-post-3'],
          },
        },
      });
    await expect(env.blogPostListItems()).toHaveText(['O-soto-gari']);
  }
});

class Env extends BlogPostsTestEnv {}
