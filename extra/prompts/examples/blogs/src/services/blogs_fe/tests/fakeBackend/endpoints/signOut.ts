import { authUrl, signedOutResponse } from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const signOut: EndpointT = {
  name: 'signOut',
  method: 'DELETE',
  path: `${authUrl}/session`,
  handle: (backend) => {
    backend.data.userId = undefined;
    return signedOutResponse();
  },
};
