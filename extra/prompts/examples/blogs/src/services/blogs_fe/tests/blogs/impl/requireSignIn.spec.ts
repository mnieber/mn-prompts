import { expect } from '@playwright/test';
import { BlogsTestEnv } from '/tests/blogs/BlogsTestEnv';
import { test, type Ctx } from '/tests/testEnv/fixtures';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a signed-out user opens the create-blog url directly', async ({
  ctx,
}) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the create-blog url without being signed in.
  //
  // It should redirect to the sign-in page, with the create-blog url as the
  // next url.
  if (
    env.step(
      //
      await env.visit('/blogs/create/_')
    )
  ) {
    await expect(env.page).toHaveURL(
      `/sign-in?nextUrl=${encodeURIComponent('/blogs/create/_')}`
    );
  }
});

class Env extends BlogsTestEnv {}
