import {
  authUrl,
  signedInResponse,
  signedOutResponse,
} from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const loadUserId: EndpointT = {
  name: 'loadUserId',
  method: 'GET',
  path: `${authUrl}/session`,
  handle: (backend) => {
    return backend.data.userId
      ? signedInResponse(backend.data.userId)
      : signedOutResponse();
  },
};
