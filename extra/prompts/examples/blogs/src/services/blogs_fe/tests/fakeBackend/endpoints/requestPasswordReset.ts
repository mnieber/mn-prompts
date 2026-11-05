import { authUrl } from '/tests/fakeBackend/authResponses';
import type { EndpointT } from '/tests/fakeBackend/types';

export const requestPasswordReset: EndpointT = {
  name: 'requestPasswordReset',
  method: 'POST',
  path: `${authUrl}/password/request`,
  handle: () => {
    return { status: 200, json: { status: 200 } };
  },
};
