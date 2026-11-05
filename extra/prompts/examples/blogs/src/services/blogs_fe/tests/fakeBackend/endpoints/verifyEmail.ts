import {
  authErrorResponse,
  authUrl,
  signedOutResponse,
} from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const EXPIRED_KEY = 'expired-key';
export const EXPIRED_KEY_MESSAGE = 'Invalid or expired key.';

export const verifyEmail: EndpointT = {
  name: 'verifyEmail',
  method: 'POST',
  path: `${authUrl}/email/verify`,
  handle: (backend, request) => {
    if (request.body.key === EXPIRED_KEY) {
      return authErrorResponse(
        'invalid_or_expired_key',
        EXPIRED_KEY_MESSAGE,
        'key'
      );
    }
    return signedOutResponse();
  },
};
