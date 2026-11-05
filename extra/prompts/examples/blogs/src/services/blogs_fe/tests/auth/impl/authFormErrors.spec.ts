import { expect } from '@playwright/test';
import {
  COMMON_PASSWORD,
  COMMON_PASSWORD_MESSAGE,
} from '/tests/fakeBackend/endpoints/signUp';
import { INVALID_TOKEN_MESSAGE } from '/tests/fakeBackend/endpoints/resetPassword';
import {
  EXPIRED_KEY,
  EXPIRED_KEY_MESSAGE,
} from '/tests/fakeBackend/endpoints/verifyEmail';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { TestEnv } from '/tests/testEnv/TestEnv';

const EMAIL = 'maarten@example.com';
const PASSWORD = 'correct horse battery staple';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('the sign-up form shows its errors', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We enter two different passwords, and press Sign Up.
  //
  // It should show the error, and not call the backend.
  if (
    env.step(
      //
      await env.visit('/sign-up'),
      await env.fillSignUpForm(EMAIL, PASSWORD, 'something else'),
      await env.clickButton('Sign Up')
    )
  ) {
    await expect(env.view('SignUpForm')).toContainText(
      'The passwords do not match'
    );
    expect(env.backend.requestsOf('signUp')).toHaveLength(0);
  }

  // We enter a password that is too common, and press Sign Up.
  //
  // It should show the message of the backend on the password field.
  if (
    env.step(
      //
      await env.fillSignUpForm(EMAIL, COMMON_PASSWORD, COMMON_PASSWORD),
      await env.clickButton('Sign Up')
    )
  ) {
    await expect(env.view('SignUpForm')).toContainText(COMMON_PASSWORD_MESSAGE);
    await expect(env.view('SignUpCard__Done')).toHaveCount(0);
  }
});

test('an expired link shows an error', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open an expired verification link, and press the button.
  //
  // It should show the message of the backend.
  if (
    env.step(
      //
      await env.visit(`/account/verify-email/${EXPIRED_KEY}`),
      await env.clickButton('Verify Email Address')
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(EXPIRED_KEY_MESSAGE);
    await expect(env.view('VerifyEmailCard__Done')).toHaveCount(0);
  }

  // We open an expired password reset link, enter a password, and press the button.
  //
  // It should show the message of the backend.
  if (
    env.step(
      //
      await env.visit(`/account/password/reset/${EXPIRED_KEY}`),
      await env.page
        .getByPlaceholder('New password', { exact: true })
        .fill(PASSWORD),
      await env.page.getByPlaceholder('Confirm new password').fill(PASSWORD),
      await env.clickButton('Change Password')
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(INVALID_TOKEN_MESSAGE);
    await expect(env.view('ResetPasswordCard__Done')).toHaveCount(0);
  }
});

class Env extends TestEnv {
  //
  // Actions
  //

  async fillSignUpForm(email: string, password: string, confirmation: string) {
    await this.page.getByPlaceholder('Email').fill(email);
    await this.page
      .getByPlaceholder('Password', { exact: true })
      .fill(password);
    await this.page.getByPlaceholder('Confirm password').fill(confirmation);
  }
}
