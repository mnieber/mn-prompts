import { expect } from '@playwright/test';
import { test, type Ctx } from '/tests/testEnv/fixtures';
import { TestEnv } from '/tests/testEnv/TestEnv';

const GENERIC_MESSAGE = 'Oops, something went wrong, please try again later';

const createEnv = (ctx: Ctx) => {
  return new Env(ctx);
};

test('a thrown error shows the error banner', async ({ ctx }) => {
  // Create the test environment
  const env = createEnv(ctx);

  // We are on the sign-in page, and some code throws an error.
  //
  // It should show the generic message in the banner, and report the uncaught error.
  if (
    env.step(
      //
      await env.visit('/sign-in'),
      await env.throwError('some bug')
    )
  ) {
    await expect(env.view('ErrorBanner')).toContainText(GENERIC_MESSAGE);
    await env.expectUncaughtError(/some bug/);
  }
});

class Env extends TestEnv {
  /** Throws an error that no code handles. */
  async throwError(message: string) {
    await this.page.evaluate((message) => {
      setTimeout(() => {
        throw new Error(message);
      });
    }, message);
  }

  /** Checks the uncaught error, and removes it so that the fixture accepts it. */
  async expectUncaughtError(pattern: RegExp) {
    await expect
      .poll(() => this.pageErrors.map(String).join())
      .toMatch(pattern);
    this.pageErrors.length = 0;
  }
}
