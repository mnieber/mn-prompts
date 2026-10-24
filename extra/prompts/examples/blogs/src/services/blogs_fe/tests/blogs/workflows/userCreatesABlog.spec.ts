import { expect } from '@playwright/test';
import { BlogsTestEnv } from '/tests/blogs/BlogsTestEnv';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { JUDO } from '/tests/blogs/fixtures';

const NAME = 'Brazilian jiu-jitsu';
const SLUG = 'brazilian-jiu-jitsu';
const DESCRIPTION = 'Ground fighting, step by step.';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user creates a blog', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and we have the blog Judo.
  if (env.step(await env.signIn('maarten'), await env.addBlog(JUDO))) {
  }

  // We visit the blogs page.
  //
  // The BlogListView should list Judo, and the create-blog button should be
  // enabled.
  if (env.step(await env.visit('/blogs'))) {
    await expect(env.blogListItems()).toHaveText(['Judo']);
    await expect(env.button('Create blog')).toBeEnabled();
  }

  // We press the create-blog button.
  //
  // It should open the BlogFormView on the create route.
  if (env.step(await env.clickButton('Create blog'))) {
    await expect(env.page).toHaveURL('/blogs/create/_');
    await expect(env.view('BlogFormView')).toBeVisible();
  }

  // We fill out the name and the description, and press Save.
  //
  // It should call CreateBlog with the form data, open the new blog, and list
  // it in the BlogListView.
  if (
    env.step(
      await env.fillField('NAME', NAME),
      await env.fillField('DESCRIPTION', DESCRIPTION),
      await env.clickButton('Save')
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('createBlog')?.body)
      .toMatchObject({
        create_blog_form: { name: NAME, slug: SLUG, description: DESCRIPTION },
      });
    // The slug is derived from the name.
    await expect(env.page).toHaveURL(`/blogs/${SLUG}`);
    await expect(env.blogListItems()).toHaveText(['Judo', NAME]);
    await expect(env.blogListItem(NAME)).toHaveClass(
      /BlogListViewItem--highlighted/
    );
  }
});

class Env extends BlogsTestEnv {}
