import {
  authErrorResponse,
  authUrl,
  signedInResponse,
} from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const WRONG_PASSWORD = 'wrong-password';

export const signInUser: EndpointT = {
  name: 'signInUser',
  method: 'POST',
  path: `${authUrl}/login`,
  handle: (backend, request) => {
    const { email, password } = request.body;
    if (password === WRONG_PASSWORD) {
      return authErrorResponse(
        'email_password_mismatch',
        'The email address and/or password you specified are not correct.',
        'password'
      );
    }
    backend.data.userId = email;
    return signedInResponse(email);
  },
};
