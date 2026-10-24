import type { EndpointT } from '/tests/fakeBackend/FakeBackend';

export const loadUserId: EndpointT = {
  name: 'loadUserId',
  method: 'GET',
  path: '/users/user-id/',
  handle: (backend) => {
    return { status: 200, json: { user_id: backend.data.userId ?? null } };
  },
};
