import { expect } from '@playwright/test';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { TestEnv } from '/tests/testEnv/TestEnv';

const EMAIL = 'maarten@example.com';
const NEW_PASSWORD = 'an even better passphrase';
// The key in the emailed link is url encoded
const ENCODED_KEY = 'abc-the%3Akey';
const KEY = 'abc-the:key';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user resets their password', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the sign-in page, and follow the link for a forgotten password.
  //
  // It should open the page where we request a reset link.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.page
        .getByRole('link', { name: 'Did you forget your password?' })
        .click()
    )
  ) {
    await expect(env.page).toHaveURL('/account/password/reset');
    await expect(env.view('RequestPasswordResetForm')).toBeVisible();
  }

  // We enter our email address, and press the button.
  //
  // It should request the link, and ask us to check our email.
  if (
    env.step(
      //
      await env.page.getByPlaceholder('Email').fill(EMAIL),
      await env.clickButton('Send Reset Link')
    )
  ) {
    await expect(env.view('RequestPasswordResetCard__Done')).toContainText(
      'we sent it a link'
    );
    expect(env.backend.lastRequest('requestPasswordReset')?.body).toEqual({
      email: EMAIL,
    });
  }

  // We open the link in the email, enter a new password, and press the button.
  //
  // It should send the decoded key and the password, and say that we can now sign in.
  if (
    env.step(
      //
      await env.visit(`/account/password/reset/${ENCODED_KEY}`),
      await env.page
        .getByPlaceholder('New password', { exact: true })
        .fill(NEW_PASSWORD),
      await env.page
        .getByPlaceholder('Confirm new password')
        .fill(NEW_PASSWORD),
      await env.clickButton('Change Password')
    )
  ) {
    await expect(env.view('ResetPasswordCard__Done')).toContainText(
      'You can now sign in'
    );
    expect(env.backend.lastRequest('resetPassword')?.body).toEqual({
      key: KEY,
      password: NEW_PASSWORD,
    });
  }
});

class Env extends TestEnv {}
