import type { EndpointT } from '/tests/fakeBackend/FakeBackend';

export const getBlogs: EndpointT = {
  name: 'getBlogs',
  method: 'GET',
  path: '/blogs/list/',
  handle: (backend) => {
    return { status: 200, json: backend.data.blogs };
  },
};
