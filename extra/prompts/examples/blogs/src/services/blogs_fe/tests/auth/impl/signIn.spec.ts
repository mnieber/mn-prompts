import { expect } from '@playwright/test';
import {
  authErrorResponse,
  signedOutResponse,
} from '/tests/fakeBackend/authResponses';
import { WRONG_PASSWORD } from '/tests/fakeBackend/endpoints/signInUser';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { baseURL } from '/tests/testEnv/urls';
import { TestEnv } from '/tests/testEnv/TestEnv';

const EMAIL = 'maarten@example.com';
const PASSWORD = 'secret';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a user signs in and signs out', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the sign-in page, enter our credentials, and press Sign In.
  //
  // It should send the credentials, leave the sign-in page, and store nothing in the
  // browser: the session cookie keeps us signed in.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect(env.page).not.toHaveURL('/sign-in');
    expect(env.backend.lastRequest('signInUser')?.body).toEqual({
      email: EMAIL,
      password: PASSWORD,
    });
    expect(await env.localStorageKeys()).toEqual([]);
  }

  // We open the account menu, and sign out.
  //
  // It should end the session in the backend, and go to the sign-in page.
  if (
    env.step(
      //
      await env.clickButton('Account'),
      await env.page.getByRole('menuitem', { name: 'Sign Out' }).click()
    )
  ) {
    await expect(env.page).toHaveURL('/sign-in');
    await expect.poll(() => env.backend.requestsOf('signOut').length).toBe(1);
    expect(env.backend.data.userId).toBeUndefined();
  }
});

test('the sign-in form shows why signing in failed', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the sign-in page, enter the wrong password, and press Sign In.
  //
  // It should show the error, and stay on the sign-in page.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.submitCredentials(EMAIL, WRONG_PASSWORD)
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Sign in failed. Please check your email and password'
    );
    await expect(env.page).toHaveURL('/sign-in');
  }

  // We sign in, but we have not verified our email address yet.
  //
  // It should ask us to verify our email address.
  if (
    env.step(
      //
      env.backend.failNext('signInUser', signedOutResponse('verify_email')),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Please verify your email address first. Check your email for the link.'
    );
  }

  // We sign in, but our account is not active.
  //
  // It should say so.
  if (
    env.step(
      //
      env.backend.failNext('signInUser', signedOutResponse()),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Your account is not active'
    );
  }

  // We sign in, after too many failed attempts.
  //
  // It should ask us to try again later.
  if (
    env.step(
      //
      env.backend.failNext(
        'signInUser',
        authErrorResponse(
          'too_many_login_attempts',
          'Too many failed login attempts.'
        )
      ),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect(env.view('GlobalError')).toHaveText(
      'Too many failed attempts. Please try again later.'
    );
  }
});

test('a user signs in while already signed in elsewhere', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We open the sign-in page, and meanwhile we sign in in another tab. Then we press
  // Sign In.
  //
  // It should leave the sign-in page, because the session in the backend is valid.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.signIn(EMAIL),
      env.backend.failNext('signInUser', {
        status: 409,
        json: { status: 409 },
      }),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect(env.page).not.toHaveURL('/sign-in');
  }
});

test('a write sends the csrf token', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // The backend has set the csrf cookie, and we sign in.
  //
  // It should send the value of the cookie in the csrf header.
  if (
    env.step(
      //
      await env.setCsrfCookie('the-csrf-token'),
      await env.visit('/sign-in'),
      await env.submitCredentials(EMAIL, PASSWORD)
    )
  ) {
    await expect
      .poll(() => env.backend.lastRequest('signInUser')?.headers['x-csrftoken'])
      .toBe('the-csrf-token');
  }
});

class Env extends TestEnv {
  //
  // Actions
  //

  async submitCredentials(email: string, password: string) {
    await this.page.getByPlaceholder('Email').fill(email);
    await this.page.getByPlaceholder('Password').fill(password);
    await this.clickButton('Sign In');
  }

  async setCsrfCookie(value: string) {
    await this.page
      .context()
      .addCookies([{ name: 'csrftoken', value, url: baseURL }]);
  }

  //
  // Queries
  //

  localStorageKeys() {
    return this.page.evaluate(() => Object.keys(localStorage));
  }
}
