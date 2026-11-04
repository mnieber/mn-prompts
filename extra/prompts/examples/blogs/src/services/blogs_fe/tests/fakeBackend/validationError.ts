import type { ResponseT } from '/tests/fakeBackend/types';

/** The response of the real backend when a request fails with this error code. */
export const validationError = (code: string): ResponseT => {
  return {
    status: 400,
    json: {
      type: 'validation_error',
      errors: [{ code, detail: 'Invalid input.', attr: null }],
    },
  };
};
