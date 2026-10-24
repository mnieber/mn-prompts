import { expect } from '@playwright/test';
import { BlogPostsTestEnv } from '/tests/blogPosts/BlogPostsTestEnv';
import { BREAKFALLS } from '/tests/blogPosts/exampleData';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const TITLE = 'O-goshi for beginners';
const SLUG = 'o-goshi-for-beginners-';
const CONTENT = 'Turn your hips in deeply.';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user creates a blog post', async ({ ctx }) => {
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

  // We visit the blogs page and click on the blog Judo.
  //
  // It should open the blog, and the BlogPostListView should list Breakfalls.
  // The create-blog-post button should be enabled.
  if (
    env.step(
      //
      await env.visit('/blogs'),
      await env.clickBlog('Judo')
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/judo');
    await expect(env.blogPostListItems()).toHaveText([/^Breakfalls/]);
    await expect(env.button('Create blog post')).toBeEnabled();
  }

  // We press the create-blog-post button.
  //
  // It should open the BlogPostFormView on the create route.
  if (
    env.step(
      //
      await env.clickButton('Create blog post')
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/judo/blog-posts/create/_');
    await expect(env.view('BlogPostFormView')).toBeVisible();
  }

  // We fill out the title and the content, and press Save.
  //
  // It should call CreateBlogPost with the form data, open the new blog post,
  // and list it in the BlogPostListView.
  if (
    env.step(
      //
      await env.fillField('TITLE', TITLE),
      await env.fillField('CONTENT', CONTENT),
      await env.clickButton('Save')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('createBlogPost'))
      .toMatchObject({
        // The blog is identified by its id
        path: '/blogs/blog-1/blog-posts/create/',
      });
    // The form data has exactly these fields
    await expect
      .poll(() => env.backend.lastRequest('createBlogPost')?.body)
      .toEqual({
        create_blog_post_form: {
          title: TITLE,
          slug: SLUG,
          content: CONTENT,
          level: 'medium',
          tags: null,
        },
        blog_id: 'blog-1',
      });
    // The slug is derived from the title (with a trailing dash).
    await expect(env.page).toHaveURL(`/blogs/judo/blog-posts/${SLUG}`);
    await expect(env.blogPostListItems()).toHaveText([/^Breakfalls/, TITLE]);
    await expect(env.blogPostListItem(TITLE)).toHaveClass(
      /BlogPostListViewItem--highlighted/
    );
  }
});

class Env extends BlogPostsTestEnv {}
