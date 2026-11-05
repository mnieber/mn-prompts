import {
  authErrorResponse,
  authUrl,
  signedOutResponse,
} from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const COMMON_PASSWORD = 'password123';
export const COMMON_PASSWORD_MESSAGE = 'This password is too common.';

export const signUp: EndpointT = {
  name: 'signUp',
  method: 'POST',
  path: `${authUrl}/signup`,
  handle: (backend, request) => {
    if (request.body.password === COMMON_PASSWORD) {
      return authErrorResponse(
        'password_too_common',
        COMMON_PASSWORD_MESSAGE,
        'password'
      );
    }
    return signedOutResponse('verify_email');
  },
};
