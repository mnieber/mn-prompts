import type { ResponseT } from '/tests/fakeBackend/types';

/** The response of the real backend when the session is no longer valid. */
export const authenticationError = (): ResponseT => {
  return { status: 401, json: { detail: 'Not authenticated' } };
};
