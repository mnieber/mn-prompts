import {
  authErrorResponse,
  authUrl,
  signedOutResponse,
} from '/tests/fakeBackend/authResponses';
import { EXPIRED_KEY } from '/tests/fakeBackend/endpoints/verifyEmail';
import type { EndpointT } from '/tests/fakeBackend/types';

export const INVALID_TOKEN_MESSAGE = 'The password reset token was invalid.';

export const resetPassword: EndpointT = {
  name: 'resetPassword',
  method: 'POST',
  path: `${authUrl}/password/reset`,
  handle: (backend, request) => {
    if (request.body.key === EXPIRED_KEY) {
      return authErrorResponse('token_invalid', INVALID_TOKEN_MESSAGE, 'key');
    }
    return signedOutResponse();
  },
};
