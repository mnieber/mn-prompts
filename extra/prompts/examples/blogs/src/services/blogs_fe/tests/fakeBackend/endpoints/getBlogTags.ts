import type { EndpointT } from '/tests/fakeBackend/types';

export const getBlogTags: EndpointT = {
  name: 'getBlogTags',
  method: 'GET',
  path: '/blogs/tags/',
  handle: (backend) => {
    return { status: 200, json: { tags: backend.data.blogTags } };
  },
};
