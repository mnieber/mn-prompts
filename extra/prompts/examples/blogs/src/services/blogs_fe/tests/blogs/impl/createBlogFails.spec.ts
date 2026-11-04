import { expect } from '@playwright/test';
import { BlogsTestEnv } from '/tests/blogs/BlogsTestEnv';
import { JUDO } from '/tests/blogs/exampleData';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user creates a blog with a name that already exists', async ({
  ctx,
}) => {
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

  // We open the create-blog form, use the name Judo, and press Save.
  //
  // It should show the error on the name field, stay on the create route, and
  // keep what the user typed.
  if (
    env.step(
      //
      await env.visit('/blogs/create/_'),
      await env.fillField('NAME', 'Judo'),
      await env.fillField('DESCRIPTION', 'Throws and pins.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.view('FormFieldError')).toHaveText(
      'A blog with this name already exists'
    );
    await expect(env.page).toHaveURL('/blogs/create/_');
    await expect(env.field('NAME')).toHaveValue('Judo');
    await expect(env.field('DESCRIPTION')).toHaveValue('Throws and pins.');
    await expect(env.blogListItems()).toHaveText(['Judo']);
    await expect(env.button('Save')).toBeEnabled();
  }

  // We change the name, and press Save again.
  //
  // It should create the blog and open it.
  if (
    env.step(
      //
      await env.fillField('NAME', 'Karate'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/karate-');
    await expect(env.blogListItems()).toHaveText(['Judo', 'Karate']);
  }
});

test('a user creates a blog with forbidden words', async ({ ctx }) => {
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

  // We open the create-blog form, use a forbidden word in the name, and press Save.
  //
  // It should show the error on the name field, and keep the form open.
  if (
    env.step(
      //
      await env.visit('/blogs/create/_'),
      await env.fillField('NAME', 'Forbidden techniques'),
      await env.fillField('DESCRIPTION', 'Throws and pins.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('NAME')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('DESCRIPTION')).toHaveCount(0);
    await expect(env.page).toHaveURL('/blogs/create/_');
    await expect(env.field('NAME')).toHaveValue('Forbidden techniques');
  }

  // We fix the name, use a forbidden word in the description, and press Save.
  //
  // It should show the error on the description field.
  if (
    env.step(
      //
      await env.fillField('NAME', 'Karate'),
      await env.fillField('DESCRIPTION', 'Forbidden punches.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.fieldError('DESCRIPTION')).toHaveText(
      'This field contains forbidden words'
    );
    await expect(env.fieldError('NAME')).toHaveCount(0);
    await expect(env.page).toHaveURL('/blogs/create/_');
  }

  // We fix the description, and press Save.
  //
  // It should create the blog and open it.
  if (
    env.step(
      //
      await env.fillField('DESCRIPTION', 'Punches and kicks.'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.page).toHaveURL('/blogs/karate-');
    await expect(env.blogListItems()).toHaveText(['Judo', 'Karate']);
  }
});

test('creating a blog fails unexpectedly', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are signed in, and the next request to create a blog will fail.
  if (
    env.step(
      //
      await env.signIn('maarten'),
      await env.addBlog(JUDO),
      env.backend.failNext('createBlog', { status: 500, json: {} })
    )
  ) {
  }

  // We open the create-blog form, and press Save.
  //
  // It should show the global error, and keep the form open.
  if (
    env.step(
      //
      await env.visit('/blogs/create/_'),
      await env.fillField('NAME', 'Karate'),
      await env.clickButton('Save')
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Oops, something went wrong, please try again later'
    );
    await expect(env.page).toHaveURL('/blogs/create/_');
    await expect(env.field('NAME')).toHaveValue('Karate');
  }

  // We press Cancel.
  //
  // It should close the form, because the form is still in edit mode.
  if (
    env.step(
      //
      await env.clickButton('Cancel')
    )
  ) {
    await expect(env.view('BlogFormView')).toBeHidden();
    await expect(env.blogListItems()).toHaveText(['Judo']);
  }
});

class Env extends BlogsTestEnv {
  field(label: string) {
    return this.page.getByLabel(label, { exact: true });
  }
}
