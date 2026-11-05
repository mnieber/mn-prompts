import { expect } from '@playwright/test';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { TestEnv } from '/tests/testEnv/TestEnv';

const EMAIL = 'maarten@example.com';
const PASSWORD = 'correct horse battery staple';
// The key in the emailed link is url encoded
const ENCODED_KEY = 'MQ%3Athe-key';
const KEY = 'MQ:the-key';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user signs up and verifies their email address', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the sign-in page, and follow the link to create an account.
  //
  // It should open the sign-up page.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.page.getByRole('link', { name: 'Create an account' }).click()
    )
  ) {
    await expect(env.page).toHaveURL('/sign-up');
    await expect(env.view('SignUpForm')).toBeVisible();
  }

  // We fill out the form, and press Sign Up.
  //
  // It should create the account, and ask us to check our email.
  if (
    env.step(
      //
      await env.page.getByPlaceholder('Email').fill(EMAIL),
      await env.page
        .getByPlaceholder('Password', { exact: true })
        .fill(PASSWORD),
      await env.page.getByPlaceholder('Confirm password').fill(PASSWORD),
      await env.clickButton('Sign Up')
    )
  ) {
    await expect(env.view('SignUpCard__Done')).toContainText(
      'We sent you an email'
    );
    expect(env.backend.lastRequest('signUp')?.body).toEqual({
      email: EMAIL,
      password: PASSWORD,
    });
  }

  // We open the link in the email.
  //
  // It should not verify the address until we press the button, so that an email
  // scanner that opens the link doesn't verify it.
  if (
    env.step(
      //
      await env.visit(`/account/verify-email/${ENCODED_KEY}`)
    )
  ) {
    await expect(env.button('Verify Email Address')).toBeVisible();
    expect(env.backend.requestsOf('verifyEmail')).toHaveLength(0);
  }

  // We press the button.
  //
  // It should send the decoded key, and say that we can now sign in.
  if (
    env.step(
      //
      await env.clickButton('Verify Email Address')
    )
  ) {
    await expect(env.view('VerifyEmailCard__Done')).toContainText(
      'You can now sign in'
    );
    expect(env.backend.lastRequest('verifyEmail')?.body).toEqual({ key: KEY });
  }
});

class Env extends TestEnv {}
