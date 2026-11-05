import type { ResponseT } from '/tests/fakeBackend/types';

export const authUrl = '/_allauth/browser/v1/auth';

/** The response of allauth when the user is signed in. */
export const signedInResponse = (userId: string): ResponseT => {
  return {
    status: 200,
    json: {
      status: 200,
      data: {
        user: { id: userId, email: userId, display: userId },
        methods: [],
      },
      meta: { is_authenticated: true },
    },
  };
};

/** The response of allauth when nobody is signed in. */
export const signedOutResponse = (pendingFlow?: string): ResponseT => {
  return {
    status: 401,
    json: {
      status: 401,
      data: {
        flows: [
          { id: 'login' },
          { id: 'signup' },
          ...(pendingFlow ? [{ id: pendingFlow, is_pending: true }] : []),
        ],
      },
      meta: { is_authenticated: false },
    },
  };
};

/** The response of allauth when the input is not valid. */
export const authErrorResponse = (
  code: string,
  message: string,
  param?: string
): ResponseT => {
  return {
    status: 400,
    json: { status: 400, errors: [{ code, message, param }] },
  };
};
